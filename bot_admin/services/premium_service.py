# bot_admin/services/premium_service.py

from core.database import db
from core.utils.time_utils import now
from datetime import timedelta


class PremiumService:

    # ---------------------------------------------------
    # ACTIVATE PREMIUM (NEW OR EXTENDED)
    # ---------------------------------------------------
    @staticmethod
    def activate_premium(user_id: int, plan_days: int, plan_id: str):
        """
        Activates premium membership for the user.

        If user already has an active premium plan:
        → extend expiry (stacking time).

        If user is new:
        → assign new expiry.
        """

        current_time = now()
        user = db.users.find_one({"user_id": user_id})

        if user and "premium_expiry" in user and user["premium_expiry"] > current_time:
            # Extend existing premium (stacking)
            new_expiry = user["premium_expiry"] + timedelta(days=plan_days)
        else:
            # New premium activation
            new_expiry = current_time + timedelta(days=plan_days)

        db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_premium": True,
                    "premium_expiry": new_expiry,
                    "premium_plan": plan_id,
                }
            },
            upsert=True
        )

        return new_expiry

    # ---------------------------------------------------
    # REMOVE PREMIUM STATUS (Used by CRON job)
    # ---------------------------------------------------
    @staticmethod
    def remove_expired_premium():
        """
        Deactivate premium for all users whose expiry has passed.
        Called by cron job every 1 hour.
        """
        current_time = now()

        db.users.update_many(
            {"premium_expiry": {"$lte": current_time}},
            {
                "$set": {"is_premium": False},
                "$unset": {"premium_expiry": "", "premium_plan": ""}
            }
        )
        return True

    # ---------------------------------------------------
    # CHECK IF USER IS CURRENTLY PREMIUM
    # ---------------------------------------------------
    @staticmethod
    def is_premium(user_id: int) -> bool:
        """
        Returns True if user has valid premium.
        """
        current_time = now()

        user = db.users.find_one(
            {
                "user_id": user_id,
                "is_premium": True,
                "premium_expiry": {"$gt": current_time}
            }
        )

        return user is not None

    # ---------------------------------------------------
    # GET PREMIUM EXPIRY
    # ---------------------------------------------------
    @staticmethod
    def get_expiry(user_id: int):
        user = db.users.find_one({"user_id": user_id})
        return user.get("premium_expiry") if user else None

    # ---------------------------------------------------
    # FORCE REMOVE PREMIUM (Admin action)
    # ---------------------------------------------------
    @staticmethod
    def revoke_premium(user_id: int):
        """
        Remove premium manually.
        """

        db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {"is_premium": False},
                "$unset": {"premium_expiry": "", "premium_plan": ""}
            }
        )

        return True

# bot_user/services/premium_service.py

from core.database import db
from core.utils.time_utils import now
from bot_admin.services.premium_service import PremiumService as AdminPremiumService


class UserPremiumService:

    # ---------------------------------------------------------
    # CHECK IF USER IS PREMIUM
    # ---------------------------------------------------------
    @staticmethod
    def is_premium(user_id: int) -> bool:
        """
        Safe read-only premium check for Bot B.
        """
        current = now()
        user = db.users.find_one({"user_id": user_id})

        if not user:
            return False

        if not user.get("is_premium"):
            return False

        expiry = user.get("premium_expiry")
        if not expiry:
            return False

        return expiry > current

    # ---------------------------------------------------------
    # GET PREMIUM EXPIRY DATE
    # ---------------------------------------------------------
    @staticmethod
    def get_expiry(user_id: int):
        """
        Returns datetime expiry of user's premium period.
        """
        user = db.users.find_one({"user_id": user_id})
        if not user:
            return None
        return user.get("premium_expiry")

    # ---------------------------------------------------------
    # GET PREMIUM PLAN ID
    # ---------------------------------------------------------
    @staticmethod
    def get_plan_id(user_id: int):
        """
        Returns plan_id of user's active premium.
        """
        user = db.users.find_one({"user_id": user_id})
        if not user:
            return None
        return user.get("premium_plan")

    # ---------------------------------------------------------
    # CHECK IF PREMIUM EXPIRED
    # ---------------------------------------------------------
    @staticmethod
    def is_expired(user_id: int) -> bool:
        current = now()
        user = db.users.find_one({"user_id": user_id})

        if not user:
            return True

        expiry = user.get("premium_expiry")
        if not expiry:
            return True

        return expiry <= current

    # ---------------------------------------------------------
    # REVOKE PREMIUM (Optionally used IF bot auto-expiry runs)
    # ---------------------------------------------------------
    @staticmethod
    def revoke_if_expired(user_id: int):
        """
        (Optional for user bot)
        Auto-removes expired premium.
        """
        if UserPremiumService.is_expired(user_id):
            AdminPremiumService.revoke_premium(user_id)
            return True
        return False

    # ---------------------------------------------------------
    # GET USER PREMIUM DETAILS (STATUS SUMMARY)
    # ---------------------------------------------------------
    @staticmethod
    def get_status(user_id: int) -> dict:
        """
        Returns a dict summarizing premium state:
            {
              "is_premium": True/False,
              "expiry": datetime,
              "plan_id": "PLAN-.."
            }
        """
        current = now()
        user = db.users.find_one({"user_id": user_id})

        if not user:
            return {
                "is_premium": False,
                "expiry": None,
                "plan_id": None
            }

        is_premium = (
            user.get("is_premium") and
            user.get("premium_expiry") and
            user["premium_expiry"] > current
        )

        return {
            "is_premium": is_premium,
            "expiry": user.get("premium_expiry"),
            "plan_id": user.get("premium_plan")
        }

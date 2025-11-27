# bot_user/services/verification_service.py

from datetime import timedelta
from core.database import db
from core.utils.time_utils import now
from core.security.token_encryptor import encode_payload, decode_payload


class VerificationService:

    # -----------------------------------------------------------------------
    # CREATE A NEW VERIFICATION TOKEN (FOR REDIRECT SERVER)
    # -----------------------------------------------------------------------
    @staticmethod
    def create_verification_token(user_id: int, file_id: str = None, post_no: int = None) -> str:
        """
        Creates an encoded verification token.
        This token is used by redirect server and returned through:
           /start verified_<token>
           /start bypass_<token>
        """
        payload = {
            "user_id": user_id,
            "file_id": file_id,
            "post_no": post_no,
        }
        return encode_payload(payload)

    # -----------------------------------------------------------------------
    # DECODE VERIFICATION TOKEN
    # -----------------------------------------------------------------------
    @staticmethod
    def decode_token(encoded: str):
        """
        Safely decode token. Returns dict or None.
        """
        return decode_payload(encoded)

    # -----------------------------------------------------------------------
    # MARK USER AS VERIFIED
    # -----------------------------------------------------------------------
    @staticmethod
    def apply_verification(user_id: int) -> int:
        """
        Applies verification time as configured by admin.
        Returns number of hours of verification.
        """

        doc = db.settings.find_one({"key": "free_access_hours"})
        hours = doc["value"] if doc else 1

        expiry = now() + timedelta(hours=hours)

        db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_verified": True,
                    "verified_until": expiry
                }
            },
            upsert=True
        )

        # Log verification
        db.verification.insert_one({
            "user_id": user_id,
            "timestamp": now(),
            "hours": hours,
            "expires": expiry
        })

        return hours

    # -----------------------------------------------------------------------
    # CHECK IF USER IS STILL VERIFIED
    # -----------------------------------------------------------------------
    @staticmethod
    def is_verified(user_id: int) -> bool:
        user = db.users.find_one({"user_id": user_id})
        if not user:
            return False

        expiry = user.get("verified_until")
        if not expiry:
            return False

        return expiry > now()

    # -----------------------------------------------------------------------
    # GET VERIFICATION EXPIRY DATE
    # -----------------------------------------------------------------------
    @staticmethod
    def get_expiry(user_id: int):
        user = db.users.find_one({"user_id": user_id})
        if not user:
            return None
        return user.get("verified_until")

    # -----------------------------------------------------------------------
    # REVOKE VERIFICATION (optional)
    # -----------------------------------------------------------------------
    @staticmethod
    def revoke(user_id: int):
        """
        Forces verification expiry immediately.
        """
        db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {"is_verified": False},
                "$unset": {"verified_until": ""}
            }
        )
        return True

    # -----------------------------------------------------------------------
    # CLEAN EXPIRED VERIFICATIONS (used by cron job)
    # -----------------------------------------------------------------------
    @staticmethod
    def cleanup_expired():
        """
        Removes verification status for all expired users.
        Called by jobs/cleanup_verification.py
        """
        db.users.update_many(
            {"verified_until": {"$lt": now()}},
            {
                "$set": {"is_verified": False},
                "$unset": {"verified_until": ""}
            }
        )
        return True

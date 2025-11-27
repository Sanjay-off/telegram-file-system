# bot_admin/services/admin_service.py

from core.database import db


class AdminService:

    # -----------------------------------------------
    # INTERNAL KEYS USED IN MONGODB
    # -----------------------------------------------
    ADMIN_LIST_KEY = "admins"
    ADMIN_CONTACT_KEY = "admin_contact"

    # -----------------------------------------------
    # ADMIN MANAGEMENT
    # -----------------------------------------------

    @staticmethod
    def add_admin(user_id: int):
        """Add a new admin user ID to the admin list."""
        db.settings.update_one(
            {"key": AdminService.ADMIN_LIST_KEY},
            {"$addToSet": {"value": user_id}},
            upsert=True
        )
        return True

    @staticmethod
    def remove_admin(user_id: int):
        """Remove an admin user ID from the admin list."""
        db.settings.update_one(
            {"key": AdminService.ADMIN_LIST_KEY},
            {"$pull": {"value": user_id}}
        )
        return True

    @staticmethod
    def list_admins():
        """Return a list of admin user IDs."""
        doc = db.settings.find_one({"key": AdminService.ADMIN_LIST_KEY})
        return doc["value"] if doc else []

    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check whether user_id is in admin list."""
        doc = db.settings.find_one({"key": AdminService.ADMIN_LIST_KEY})
        if not doc or "value" not in doc:
            return False
        return user_id in doc["value"]

    # -----------------------------------------------
    # ADMIN CONTACT (Shown to users)
    # -----------------------------------------------

    @staticmethod
    def set_admin_contact(contact: str):
        """Set telegram username or ID for user support."""
        db.settings.update_one(
            {"key": AdminService.ADMIN_CONTACT_KEY},
            {"$set": {"value": contact}},
            upsert=True
        )
        return True

    @staticmethod
    def get_admin_contact() -> str:
        """Return the current admin contact for user support."""
        doc = db.settings.find_one({"key": AdminService.ADMIN_CONTACT_KEY})
        return doc["value"] if doc else None

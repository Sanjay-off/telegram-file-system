# bot_user/services/force_sub_service.py

from core.database import db


class ForceSubService:

    KEY = "force_sub"

    # ---------------------------------------------------------
    # GET ALL FORCE-SUB CHANNELS
    # ---------------------------------------------------------
    @staticmethod
    def get_channels():
        """
        Returns list of required channels:
        [
          {"channel": "@Backup", "button_text": "BACKUP"},
          {"channel": "@Movies", "button_text": "MOVIES"},
        ]
        """
        doc = db.settings.find_one({"key": ForceSubService.KEY})
        return doc["value"] if doc else []

    # ---------------------------------------------------------
    # ADD CHANNEL (Admin Bot Use)
    # ---------------------------------------------------------
    @staticmethod
    def add_channel(username: str, button_text: str):
        """
        Add a force-sub channel:
        username = "@Backup"
        button_text = "BACKUP"
        """
        db.settings.update_one(
            {"key": ForceSubService.KEY},
            {"$addToSet": {
                "value": {
                    "channel": username,
                    "button_text": button_text
                }
            }},
            upsert=True
        )
        return True

    # ---------------------------------------------------------
    # REMOVE CHANNEL (Admin Bot Use)
    # ---------------------------------------------------------
    @staticmethod
    def remove_channel(username: str):
        """
        Remove entry by channel username.
        """
        db.settings.update_one(
            {"key": ForceSubService.KEY},
            {"$pull": {"value": {"channel": username}}}
        )
        return True

    # ---------------------------------------------------------
    # CHECK BACKEND SUBSCRIPTION STATUS
    # (Does NOT send UI; only backend validation)
    # ---------------------------------------------------------
    @staticmethod
    def get_not_joined_channels(chat_member_results: dict):
        """
        chat_member_results = {
            "@Backup": True/False,
            "@Movies": True/False
        }

        Returns:
        [
           {"channel": "@Backup", "button_text": "BACKUP"}
        ]
        """
        missing = []
        all_channels = ForceSubService.get_channels()

        for item in all_channels:
            username = item["channel"]
            is_joined = chat_member_results.get(username, False)

            if not is_joined:
                missing.append(item)

        return missing

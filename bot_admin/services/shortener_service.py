# bot_admin/services/shortener_service.py

from core.database import db
import random


class ShortenerService:

    KEY = "shorteners"

    # ---------------------------------------------------
    # ADD SHORTENER
    # ---------------------------------------------------
    @staticmethod
    def add_shortener(domain: str, api_key: str):
        """
        Add a new shortener platform with API key.
        """
        entry = {
            "domain": domain.lower(),
            "api_key": api_key
        }

        db.settings.update_one(
            {"key": ShortenerService.KEY},
            {"$addToSet": {"value": entry}},
            upsert=True
        )

        return True

    # ---------------------------------------------------
    # REMOVE SHORTENER
    # ---------------------------------------------------
    @staticmethod
    def remove_shortener(domain: str):
        """
        Remove a shortener platform by domain.
        """
        db.settings.update_one(
            {"key": ShortenerService.KEY},
            {"$pull": {"value": {"domain": domain.lower()}}},
        )
        return True

    # ---------------------------------------------------
    # LIST ALL SHORTENERS
    # ---------------------------------------------------
    @staticmethod
    def list_shorteners():
        """
        Return all available shortener platforms.
        """
        doc = db.settings.find_one({"key": ShortenerService.KEY})
        return doc["value"] if doc else []

    # ---------------------------------------------------
    # GET RANDOM SHORTENER (Used by Bot B)
    # ---------------------------------------------------
    @staticmethod
    def get_random():
        """
        Pick a random shortener from DB.
        Returns: {"domain": "...", "api_key": "..."} or None
        """
        doc = db.settings.find_one({"key": ShortenerService.KEY})
        if not doc or "value" not in doc or len(doc["value"]) == 0:
            return None

        return random.choice(doc["value"])

    # ---------------------------------------------------
    # GET SHORTENER BY DOMAIN
    # ---------------------------------------------------
    @staticmethod
    def get_shortener(domain: str):
        """
        Return a shortener by domain.
        """
        doc = db.settings.find_one({"key": ShortenerService.KEY})
        if not doc:
            return None

        for item in doc["value"]:
            if item["domain"].lower() == domain.lower():
                return item

        return None

    # ---------------------------------------------------
    # COUNT PLATFORMS
    # ---------------------------------------------------
    @staticmethod
    def count():
        """
        Return number of available shorteners.
        """
        doc = db.settings.find_one({"key": ShortenerService.KEY})
        return len(doc["value"]) if doc else 0

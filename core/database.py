# core/database.py

import logging
import time
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from core.config import config

# Global database reference
db = None


def init_db(retries: int = 10, delay: int = 2):
    """
    Initialize MongoDB connection with retry logic.
    Creates required indexes for performance & consistency.
    """
    global db

    mongo_uri = config.MONGO_URI
    db_name = config.MONGO_DB_NAME

    logging.info(f"[DB] Connecting to MongoDB at {mongo_uri} (DB: {db_name})")

    for attempt in range(1, retries + 1):
        try:
            client = MongoClient(
                mongo_uri,
                maxPoolSize=50,
                serverSelectionTimeoutMS=5000
            )
            # Trigger connection check
            client.admin.command("ping")

            logging.info("[DB] MongoDB connection established.")

            db = client[db_name]

            _create_indexes()
            return db

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logging.error(f"[DB] Connection attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)

    raise Exception("❌ Could not connect to MongoDB after multiple attempts.")


# ---------------------------------------------------------------------------
# CREATE NECESSARY INDEXES — HIGH PERFORMANCE & CLEAN STORAGE
# ---------------------------------------------------------------------------
def _create_indexes():
    """
    Create all necessary MongoDB indexes (idempotent).
    This makes queries *much faster* and prevents duplicates.
    """

    # ---------------- USERS ----------------
    db.users.create_index([("user_id", ASCENDING)], unique=True)
    db.users.create_index([("premium_expiry", ASCENDING)])
    db.users.create_index([("verified_until", ASCENDING)])

    # ---------------- FILES ----------------
    db.files.create_index([("file_db_id", ASCENDING)], unique=True)
    db.files.create_index([("file_id", ASCENDING)], unique=True)
    db.files.create_index([("post_no", ASCENDING)], unique=True)

    # ---------------- ORDERS ----------------
    db.orders.create_index([("order_id", ASCENDING)], unique=True)
    db.orders.create_index([("user_id", ASCENDING)])
    db.orders.create_index([("status", ASCENDING)])
    db.orders.create_index([("expires_at", ASCENDING)])
    db.orders.create_index([("confirm_until", ASCENDING)])

    # ---------------- SETTINGS ----------------
    db.settings.create_index([("key", ASCENDING)], unique=True)

    # ---------------- VERIFICATION LOGS ----------------
    db.verification.create_index([("user_id", ASCENDING)])
    db.verification.create_index([("timestamp", ASCENDING)])

    # ---------------- TEMP DELIVERY (auto-delete jobs) ----------------
    db.temp_delivery.create_index([("delete_after", ASCENDING)])

    logging.info("[DB] All indexes initialized successfully.")

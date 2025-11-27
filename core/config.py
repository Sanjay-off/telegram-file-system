# core/config.py

import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()


class Config:
    """
    Global configuration object for the entire project.
    Loads values from environment (.env).
    """

    # ------------------------------------------------------
    # BOT TOKENS (Admin Bot A + User Bot B)
    # ------------------------------------------------------
    BOT_A_TOKEN = os.getenv("BOT_A_TOKEN", "")
    BOT_B_TOKEN = os.getenv("BOT_B_TOKEN", "")

    # Bot B username (without @)
    BOT_B_USERNAME = os.getenv("BOT_B_USERNAME", "")

    # ------------------------------------------------------
    # DATABASE CONFIG
    # ------------------------------------------------------
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/telegram_file_system")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telegram_file_system")

    # ------------------------------------------------------
    # REDIRECT SERVER CONFIG
    # ------------------------------------------------------
    # Example: "http://152.42.212.81:5000/redirect"
    REDIRECT_BASE = os.getenv("REDIRECT_BASE", "")

    # Secret key for token encryption
    # If not present, generate a secure default key
    TOKEN_SECRET = os.getenv("TOKEN_SECRET", "THIS_IS_NOT_SECURE_CHANGE_ME")

    # ------------------------------------------------------
    # VERIFICATION SETTINGS
    # ------------------------------------------------------
    # Default duration for verification if admin didn't set it
    FREE_ACCESS_HOURS_DEFAULT = int(os.getenv("FREE_ACCESS_HOURS_DEFAULT", 1))

    # ------------------------------------------------------
    # PAYMENT / UPI SETTINGS
    # ------------------------------------------------------
    UPI_ID = os.getenv("UPI_ID", "")         # upi_id@bank
    UPI_NAME = os.getenv("UPI_NAME", "ADMIN")

    # Unique paise mode: "on" / "off"
    UNIQUE_PAISE_MODE = os.getenv("UNIQUE_PAISE_MODE", "off")

    # QR expiry default (minutes)
    QR_EXPIRY_MINUTES_DEFAULT = int(os.getenv("QR_EXPIRY_MINUTES_DEFAULT", 10))

    # ------------------------------------------------------
    # ADMIN SETTINGS
    # ------------------------------------------------------
    # A default admin can be injected here if needed
    DEFAULT_ADMIN_IDS = os.getenv("DEFAULT_ADMIN_IDS", "")
    # Comma-separated → convert to list of ints
    if DEFAULT_ADMIN_IDS:
        DEFAULT_ADMIN_IDS = [int(x.strip()) for x in DEFAULT_ADMIN_IDS.split(",")]
    else:
        DEFAULT_ADMIN_IDS = []

    # ------------------------------------------------------
    # LOGGING
    # ------------------------------------------------------
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Export global config instance
config = Config()

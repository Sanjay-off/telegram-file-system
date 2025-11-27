

# core/utils/logger.py

"""
Centralized Logging System
--------------------------

Provides:
 - Unified logging format for all components
 - File logging (admin_bot.log, user_bot.log, redirect_server.log)
 - Console logging with optional colors
 - Rotating file logs to prevent infinite file growth

Used by:
  - bot_admin/admin_main.py
  - bot_user/user_main.py
  - redirect_server/redirect_main.py
  - jobs/*.py
"""

import logging
from logging.handlers import RotatingFileHandler
import os


class Logger:

    # ---------------------------------------------------------
    # CREATE PARENT LOG DIRECTORY
    # ---------------------------------------------------------
    @staticmethod
    def ensure_log_dir():
        if not os.path.exists("logs"):
            os.makedirs("logs")

    # ---------------------------------------------------------
    # BASE LOG CONFIG CREATOR
    # ---------------------------------------------------------
    @staticmethod
    def create_logger(
        name: str,
        log_file: str,
        level: str = "INFO",
        max_bytes: int = 5 * 1024 * 1024,     # 5MB per log file
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Creates a configured logger with:
          - Rotating file handler
          - Console stream
          - Clean formatting
        """

        Logger.ensure_log_dir()

        # Convert logging level
        level = level.upper()
        log_level = getattr(logging, level, logging.INFO)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.propagate = False  # avoid duplicate logs

        # -----------------------------------------------------
        # Rotating File Handler
        # -----------------------------------------------------
        file_handler = RotatingFileHandler(
            f"logs/{log_file}",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "%Y-%m-%d %H:%M:%S"
            )
        )

        # -----------------------------------------------------
        # Console Handler
        # -----------------------------------------------------
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            logging.Formatter(
                "[%(levelname)s] %(name)s: %(message)s"
            )
        )

        # Add handlers only if not already added
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger


# ---------------------------------------------------------
# PUBLIC HELPERS FOR SPECIFIC BOT SYSTEMS
# ---------------------------------------------------------

def get_admin_logger():
    return Logger.create_logger(
        name="ADMIN_BOT",
        log_file="admin_bot.log"
    )


def get_user_logger():
    return Logger.create_logger(
        name="USER_BOT",
        log_file="user_bot.log"
    )


def get_redirect_logger():
    return Logger.create_logger(
        name="REDIRECT_SERVER",
        log_file="redirect_server.log"
    )


def get_job_logger(job_name: str):
    return Logger.create_logger(
        name=f"JOB:{job_name}",
        log_file=f"{job_name}.log"
    )

# jobs/backup_db.py

"""
Backup Job: MongoDB Backups
---------------------------

This job:
 - Creates gzip-compressed backups of your MongoDB database
 - Stores them inside /backups/
 - Automatically deletes old backups (default: older than 7 days)

Prerequisites:
1) MongoDB tools installed:
   sudo apt install mongodb-database-tools

2) Cron example (run daily at 3 AM):
   0 3 * * * /usr/bin/python3 /home/ubuntu/telegram_file_system/jobs/backup_db.py
"""

import os
import sys
import logging
import subprocess
from datetime import datetime, timedelta

sys.path.append(".")

from core.config import config
from core.utils.logger import get_job_logger

logger = get_job_logger("backup_db")


def ensure_backup_dir():
    """Create backup directory if missing."""
    if not os.path.exists("backups"):
        os.makedirs("backups")


def backup_database():
    logger.info("---- Database Backup Job Started ----")

    ensure_backup_dir()

    db_name = config.MONGO_DB_NAME
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{db_name}_{timestamp}.gz"
    backup_path = os.path.join("backups", backup_filename)

    # ----------------------------------------------------------
    # RUN MONGODUMP
    # ----------------------------------------------------------
    try:
        logger.info("Running mongodump...")

        cmd = [
            "mongodump",
            f"--uri={config.MONGO_URI}",
            f"--db={db_name}",
            "--archive=" + backup_path,
            "--gzip"
        ]

        subprocess.run(cmd, check=True)
        logger.info(f"Backup created: {backup_filename}")

    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return

    # ----------------------------------------------------------
    # ROTATE OLD BACKUPS (default: delete > 7 days)
    # ----------------------------------------------------------
    delete_before = datetime.utcnow() - timedelta(days=7)
    removed = 0

    for filename in os.listdir("backups"):
        if filename.startswith(f"backup_{db_name}_") and filename.endswith(".gz"):
            file_path = os.path.join("backups", filename)
            file_time = datetime.utcfromtimestamp(os.path.getmtime(file_path))

            if file_time < delete_before:
                os.remove(file_path)
                removed += 1

    logger.info(f"Old backups removed: {removed}")
    logger.info("---- Database Backup Job Completed ✔ ----")


if __name__ == "__main__":
    backup_database()

# jobs/cleanup_verification.py

"""
Cleanup Job: Verification Expiry
--------------------------------

This script:
 - Removes verification status from users whose verification time expired
 - Deletes old verification logs (older than 7 days by default)

Run via:
    python jobs/cleanup_verification.py

Or set via cron:
    */5 * * * * /usr/bin/python3 /path/to/cleanup_verification.py
"""

import sys
sys.path.append(".")

from datetime import timedelta

from core.database import init_db, db
from core.utils.time_utils import now
from core.utils.logger import get_job_logger


logger = get_job_logger("cleanup_verification")


def cleanup_verification():
    logger.info("---- Cleanup Verification Job Started ----")

    current = now()

    # --------------------------------------------------------------
    # 1) REMOVE VERIFIED STATUS FROM EXPIRED USERS
    # --------------------------------------------------------------
    expired_users = db.users.find({
        "is_verified": True,
        "verified_until": {"$lt": current}
    })

    count_users = 0
    for user in expired_users:
        db.users.update_one(
            {"user_id": user["user_id"]},
            {
                "$set": {"is_verified": False},
                "$unset": {"verified_until": ""}
            }
        )
        count_users += 1

    logger.info(f"Verification expired for users: {count_users}")

    # --------------------------------------------------------------
    # 2) DELETE OLD VERIFICATION LOGS (> 7 DAYS)
    # --------------------------------------------------------------
    cutoff = current - timedelta(days=7)

    old_logs = db.verification.find({
        "expires": {"$lt": cutoff}
    })

    count_logs = 0
    for log in old_logs:
        db.verification.delete_one({"_id": log["_id"]})
        count_logs += 1

    logger.info(f"Old verification logs removed: {count_logs}")

    logger.info("---- Cleanup Verification Job Completed ✔ ----")


if __name__ == "__main__":
    init_db()
    cleanup_verification()

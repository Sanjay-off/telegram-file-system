# jobs/premium_expiry.py

"""
Cleanup Job: Premium Expiry
---------------------------

This job:
 - Removes premium status from users whose premium expiration time has passed.
 - Keeps the database clean and prevents users from retaining premium access.

Run via:
    python jobs/premium_expiry.py

Cron example (every 10 minutes):
    */10 * * * * /usr/bin/python3 /path/to/premium_expiry.py
"""

import sys
sys.path.append(".")

from core.database import init_db, db
from core.utils.time_utils import now
from core.utils.logger import get_job_logger


logger = get_job_logger("premium_expiry")


def cleanup_premium():
    logger.info("---- Premium Expiry Job Started ----")

    current = now()

    # -------------------------------------------------------
    # EXPIRE PREMIUM USERS
    # -------------------------------------------------------
    expired_premium_users = db.users.find({
        "is_premium": True,
        "premium_expiry": {"$lt": current}
    })

    expired_count = 0
    for user in expired_premium_users:
        db.users.update_one(
            {"user_id": user["user_id"]},
            {
                "$set": {"is_premium": False},
                "$unset": {"premium_expiry": "", "premium_plan": ""}
            }
        )
        expired_count += 1

    logger.info(f"Premium users expired: {expired_count}")

    logger.info("---- Premium Expiry Job Completed ✔ ----")


if __name__ == "__main__":
    init_db()
    cleanup_premium()

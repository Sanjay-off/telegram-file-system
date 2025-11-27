# jobs/cleanup_expired_orders.py

"""
Cleanup Job: Expire Old Orders
------------------------------

This script:
 - Marks orders with expired QR codes as "expired"
 - Marks orders with confirm window exceeded as "expired"
 - Removes extremely old expired orders (older than 7 days)

This ensures your orders collection stays clean and optimized.

Run via:
    python jobs/cleanup_expired_orders.py

Or schedule with cron:
    */10 * * * * /usr/bin/python3 /path/to/jobs/cleanup_expired_orders.py
"""

import sys
import logging
from datetime import timedelta

# Load core system
sys.path.append(".")

from core.database import init_db, db
from core.utils.time_utils import now
from core.utils.logger import get_job_logger
from bot_admin.services.order_service import OrderService


logger = get_job_logger("cleanup_expired_orders")


def cleanup_expired_orders():
    logger.info("---- Cleanup Expired Orders Job Started ----")

    current = now()

    # ----------------------------------------------------------
    # 1) EXPIRE QR-EXPIRED ORDERS
    # ----------------------------------------------------------
    qr_expired_orders = db.orders.find({
        "status": "pending",
        "expires_at": {"$lt": current}
    })

    count_qr = 0
    for order in qr_expired_orders:
        OrderService.mark_expired(order["order_id"])
        count_qr += 1

    logger.info(f"QR-expired orders marked as expired: {count_qr}")

    # ----------------------------------------------------------
    # 2) EXPIRE ORDERS BEYOND CONFIRM WINDOW (10 hours default)
    # ----------------------------------------------------------
    confirm_expired_orders = db.orders.find({
        "status": "pending",
        "confirm_until": {"$lt": current}
    })

    count_confirm = 0
    for order in confirm_expired_orders:
        OrderService.mark_expired(order["order_id"])
        count_confirm += 1

    logger.info(f"Confirm-window expired orders marked: {count_confirm}")

    # ----------------------------------------------------------
    # 3) HARD DELETE VERY OLD EXPIRED ORDERS (default: 7 days)
    # ----------------------------------------------------------
    old_expired_orders = db.orders.find({
        "status": "expired",
        "expires_at": {"$lt": current - timedelta(days=7)}
    })

    delete_count = 0
    for order in old_expired_orders:
        db.orders.delete_one({"order_id": order["order_id"]})
        delete_count += 1

    logger.info(f"Deleted old expired orders (>7 days): {delete_count}")

    logger.info("---- Cleanup Expired Orders Job Completed ✔ ----")


if __name__ == "__main__":
    init_db()
    cleanup_expired_orders()

# bot_admin/utils/helpers.py

import random
import string
from core.database import db


# ---------------------------------------------------
# CHECK IF USER IS ADMIN
# ---------------------------------------------------
async def is_admin(user_id: int) -> bool:
    """
    Check whether a user is an admin.
    """
    doc = db.settings.find_one({"key": "admins"})
    if not doc or "value" not in doc:
        return False

    return user_id in doc["value"]


# ---------------------------------------------------
# RANDOM STRING GENERATOR
# ---------------------------------------------------
def random_string(length=6):
    """
    Generate a secure random alphanumeric string.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# ---------------------------------------------------
# FILE DB ID GENERATOR
# Example: FILE-AB12CD
# ---------------------------------------------------
def generate_file_db_id():
    return f"FILE-{random_string(6)}"


# ---------------------------------------------------
# PLAN ID GENERATOR
# Example: PLAN-30-XY92ZQ
# ---------------------------------------------------
def generate_plan_id(days=None):
    """
    Generates unique plan ID.
    days may be passed for readability.
    """
    rnd = random_string(6)
    if days:
        return f"PLAN-{days}-{rnd}"
    return f"PLAN-{rnd}"


# ---------------------------------------------------
# ORDER ID GENERATOR
# Example: ORD-XYZ123
# ---------------------------------------------------
def generate_order_id():
    return f"ORD-{random_string(6)}"


# ---------------------------------------------------
# GENERAL TOKEN GENERATOR
# Example: TOKEN-X82JSJAS
# Used for verifying URL tokens, verification flows, etc.
# ---------------------------------------------------
def generate_token(length=32):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

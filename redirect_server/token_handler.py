# redirect_server/token_handler.py

"""
Redirect Server Token Handler
-----------------------------

This module securely handles:
 - Decoding encrypted verification tokens sent from Telegram Bot
 - Checking token validity
 - Detecting bypass attempts
 - Returning signed results for Bot B to process
 - Providing helpers used inside Flask/FastAPI routes

Flow:
1. Bot sends user to:
     /redirect?token=<encrypted>
2. User loads shortlink -> shortener -> your redirect server
3. This module:
     - decrypts token
     - logs verification start
4. After countdown is completed, it generates:
     /return?result=verified_<token>
   If bypass detected:
     /return?result=bypass_<token>
5. Bot B interprets the final deep-link.

SECURITY:
 - AES-256 token encryption via token_encryptor.py
 - Optional HMAC signature protection via signature_checker.py
"""

from datetime import datetime
from core.security.token_encryptor import decode_payload, encode_payload
from core.security.signature_checker import SignatureChecker
from core.utils.time_utils import now
from core.database import db


class RedirectTokenHandler:

    # ------------------------------------------------------------
    # DECODE TOKEN FROM USER BOT → PAYLOAD
    # ------------------------------------------------------------
    @staticmethod
    def decode_incoming_token(encoded_token: str) -> dict:
        """
        Decrypts token received via:
            /redirect?token=<encrypted>

        Returns dict or None if tampered/invalid.
        """
        if not encoded_token:
            return None

        payload = decode_payload(encoded_token)
        if not payload:
            return None

        # Token shape example:
        # {
        #   "user_id": 12345,
        #   "file_id": "...",
        #   "post_no": 7
        # }
        return payload

    # ------------------------------------------------------------
    # LOG VISIT (OPTIONAL)
    # ------------------------------------------------------------
    @staticmethod
    def log_visit(user_id: int, token: str):
        """
        Stores the timestamp of redirect server visit.
        Helps detect bypass (user must hit redirect before verifying).
        """
        db.redirect_logs.insert_one({
            "user_id": user_id,
            "token": token,
            "visited_at": now()
        })

    # ------------------------------------------------------------
    # BUILD VERIFIED RETURN TOKEN → bot deep-link
    # ------------------------------------------------------------
    @staticmethod
    def build_verified_token(user_id: int, file_id: str = None, post_no: int = None) -> str:
        """
        Called after verification countdown is completed successfully.
        """
        payload = {
            "user_id": user_id,
            "file_id": file_id,
            "post_no": post_no
        }

        encrypted = encode_payload(payload)

        # Add optional signature
        signed_packet = SignatureChecker.pack(encrypted)

        return f"verified_{signed_packet}"

    # ------------------------------------------------------------
    # BUILD BYPASS RETURN TOKEN → bot deep-link
    # ------------------------------------------------------------
    @staticmethod
    def build_bypass_token(user_id: int, file_id: str = None, post_no: int = None) -> str:
        """
        Called when bypass detected:
         - direct access without visiting countdown page
         - visiting /return without passing through short link
         - manually altering URLs
        """
        payload = {
            "user_id": user_id,
            "file_id": file_id,
            "post_no": post_no
        }

        encrypted = encode_payload(payload)
        signed_packet = SignatureChecker.pack(encrypted)

        return f"bypass_{signed_packet}"

    # ------------------------------------------------------------
    # CHECK IF USER VISITED REDIRECT PAGE (BYPASS DETECTION)
    # ------------------------------------------------------------
    @staticmethod
    def did_user_visit(user_id: int, encrypted_token: str) -> bool:
        """
        Returns True if the user visited the redirect page
        before redirecting back to the bot.

        This is your bypass detection.
        """
        entry = db.redirect_logs.find_one({
            "user_id": user_id,
            "token": encrypted_token
        })

        return entry is not None

    # ------------------------------------------------------------
    # CLEAN LOGS (OPTIONAL)
    # ------------------------------------------------------------
    @staticmethod
    def cleanup_old_logs(hours: int = 6):
        """
        Removes redirect logs older than X hours.
        Called by cron job.
        """
        cutoff = now() - timedelta(hours=hours)
        db.redirect_logs.delete_many({"visited_at": {"$lt": cutoff}})

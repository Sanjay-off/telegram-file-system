

# core/utils/hashing.py

"""
Hashing Utilities
-----------------

Provides secure and non-secure hashing methods for:
 - generating short IDs
 - verifying hashed strings
 - creating deterministic signatures
 - internal reference hashing for files, orders, tokens

NO external dependencies.
"""

import hashlib
import os


class HashUtils:

    # ---------------------------------------------------------
    # SHA256 (secure hashing)
    # ---------------------------------------------------------
    @staticmethod
    def sha256(text: str) -> str:
        """
        Returns hex SHA256 hash of the given text.
        """
        return hashlib.sha256(text.encode()).hexdigest()

    # ---------------------------------------------------------
    # SHA1 (short hash for identifiers / internal use)
    # ---------------------------------------------------------
    @staticmethod
    def sha1_short(text: str, length: int = 10) -> str:
        """
        Generates a short SHA1-based identifier (non-secure).
        Useful for naming files, deriving compact IDs, etc.
        Default length=10 chars.
        """
        h = hashlib.sha1(text.encode()).hexdigest()
        return h[:length]

    # ---------------------------------------------------------
    # RANDOM 16-BYTE HEX TOKEN
    # ---------------------------------------------------------
    @staticmethod
    def random_token(length: int = 32) -> str:
        """
        Generates a random token of `length` hex characters.
        Default = 32 hex chars (~128-bit).
        """
        return os.urandom(length // 2).hex()

    # ---------------------------------------------------------
    # HMAC-LIKE NON-SECRET CHECKSUM (NOT for security)
    # ---------------------------------------------------------
    @staticmethod
    def checksum(text: str) -> str:
        """
        Lightweight checksum for detecting accidental changes.
        NOT cryptographically secure.
        """
        return hashlib.md5(text.encode()).hexdigest()

    # ---------------------------------------------------------
    # VERIFY plain text against SHA256 hash
    # ---------------------------------------------------------
    @staticmethod
    def verify_sha256(text: str, hashed: str) -> bool:
        """
        Validate a SHA256 hash by recomputing.
        """
        return hashlib.sha256(text.encode()).hexdigest() == hashed

    # ---------------------------------------------------------
    # Deterministic HASH-BASED ID generator
    # ---------------------------------------------------------
    @staticmethod
    def build_id(prefix: str, value: str, length: int = 12) -> str:
        """
        Generate a readable ID:
          <prefix>-<short-hash>

        Example:
            plan_id = build_id("PLAN", "30_days_40rs")
        """
        short = HashUtils.sha1_short(value, length)
        return f"{prefix}-{short}"

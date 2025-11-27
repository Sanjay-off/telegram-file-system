# core/security/token_encryptor.py

"""
Token Encryptor
---------------
Secure encoding/decoding of payload dictionaries using Fernet (AES-256).

Used for:
 - Verification tokens     (/start verify_<token>)
 - Verified tokens         (/start verified_<token>)
 - Bypass tokens           (/start bypass_<token>)
 - Click-here tokens       (/start click_<token>)
 - File download tokens    (/start get_<token>)
 - Payment deep-link tokens
 - Redirect server communication

This prevents users from forging tokens or modifying payloads.
"""

import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from core.config import config


class TokenEncryptor:
    """
    Wrapper around Fernet encryption.
    """

    # -----------------------------------------------------------
    # ENSURE SECRET KEY IS A VALID 32-byte URL-safe base64 KEY
    # -----------------------------------------------------------
    @staticmethod
    def _prepare_key(secret: str) -> bytes:
        """
        Converts TOKEN_SECRET into a valid Fernet key.
        - Must be 32-byte key base64 encoded = 44 characters
        - If shorter, we stretch it deterministically
        """

        # Convert to bytes
        raw = secret.encode()

        # Pad / stretch to 32 bytes deterministically
        if len(raw) < 32:
            raw = (raw * (32 // len(raw) + 1))[:32]
        else:
            raw = raw[:32]

        # Convert to URL-safe base64 (Fernet key requirement)
        return base64.urlsafe_b64encode(raw)

    # Build Fernet instance
    _fernet = Fernet(_prepare_key(config.TOKEN_SECRET))

    # -----------------------------------------------------------
    # ENCODE PAYLOAD → TOKEN (string)
    # -----------------------------------------------------------
    @staticmethod
    def encode_payload(payload: dict) -> str:
        """
        Converts dict → JSON → Bytes → Fernet token (URL-safe base64 string).
        """
        try:
            json_bytes = json.dumps(payload, separators=(",", ":")).encode()
            token = TokenEncryptor._fernet.encrypt(json_bytes)
            return token.decode()
        except Exception:
            return None

    # -----------------------------------------------------------
    # DECODE TOKEN → PAYLOAD (dict)
    # -----------------------------------------------------------
    @staticmethod
    def decode_payload(token: str) -> dict:
        """
        Converts encrypted token back to dict.
        Returns None if tampered or invalid.
        """
        try:
            decrypted = TokenEncryptor._fernet.decrypt(token.encode())
            data = json.loads(decrypted.decode())
            return data
        except InvalidToken:
            return None
        except Exception:
            return None


# -----------------------------------------------------------
# EXPOSE SIMPLE FUNCTIONS USED IN ALL BOTS
# -----------------------------------------------------------
def encode_payload(payload: dict) -> str:
    return TokenEncryptor.encode_payload(payload)


def decode_payload(token: str) -> dict:
    return TokenEncryptor.decode_payload(token)

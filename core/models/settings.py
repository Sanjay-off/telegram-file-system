# core/models/settings.py

"""
Settings Model — stores all admin-configurable settings.

This includes:
 - Force-sub channels
 - Free access verification hours
 - UPI configuration
 - Unique paise mode
 - QR expiry duration
 - List of shortener platforms
 - Default admin list
 - Redirect server base URL

All settings are stored in a SINGLE collection: db.settings
Each setting is stored as:
{
    "key": "<setting_key>",
    "value": <any JSON-serializable data>
}

Used by:
 - Admin Bot handlers (force_sub, shortener_settings, admin_settings)
 - User Bot flows (verification, payment, premium)
 - Redirect Server configuration
"""

from dataclasses import dataclass, asdict
from typing import Any
from datetime import datetime


@dataclass
class SettingsModel:
    """
    A document representing ONE setting entry.
    e.g.,
      key="free_access_hours",
      value=1
    """

    key: str
    value: Any
    updated_at: datetime

    def to_dict(self):
        d = asdict(self)
        d["updated_at"] = self.updated_at
        return d

    @staticmethod
    def from_dict(data: dict):
        return SettingsModel(
            key=data.get("key"),
            value=data.get("value"),
            updated_at=data.get("updated_at", datetime.utcnow())
        )

    @staticmethod
    def validate(data: dict) -> bool:
        """
        A simple schema validator to ensure key/value exist.
        """
        return "key" in data and "value" in data

    @staticmethod
    def create(key: str, value: Any):
        """
        Helper to create a new setting entry.
        """
        return SettingsModel(
            key=key,
            value=value,
            updated_at=datetime.utcnow()
        )

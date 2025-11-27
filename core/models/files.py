# core/models/files.py

"""
Files Model — defines the document structure used by the `files` collection.

ZIP files are stored in your PRIVATE TELEGRAM CHANNEL.
This model stores metadata only — NOT the actual file data.

Referenced by:
 - bot_admin/services/file_service.py
 - bot_admin/handlers/file_upload.py
 - bot_user/services/file_service.py
 - download_flow, click_here_flow, verification flow
 - template generation

Each entry corresponds to ONE uploaded file.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class FileModel:
    """
    Represents a file entry stored in MongoDB.
    """

    file_db_id: str               # unique ID we generate
    file_id: str                  # Telegram API file_id
    post_no: int                  # unique post number for the file
    description: str              # description added by admin
    extra_message: str            # message footer added by admin
    channel_message_id: int       # msg id inside private channel
    created_at: datetime          # upload timestamp

    def to_dict(self):
        """Convert dataclass to MongoDB compatible dict."""
        d = asdict(self)
        d["created_at"] = self.created_at
        return d

    @staticmethod
    def from_dict(data: dict):
        """Convert MongoDB document to FileModel object."""
        return FileModel(
            file_db_id=data.get("file_db_id"),
            file_id=data.get("file_id"),
            post_no=data.get("post_no"),
            description=data.get("description", ""),
            extra_message=data.get("extra_message", ""),
            channel_message_id=data.get("channel_message_id"),
            created_at=data.get("created_at", datetime.utcnow())
        )

    @staticmethod
    def validate(data: dict) -> bool:
        """
        Basic validation check for required fields.
        """
        required = ["file_db_id", "file_id", "post_no", "channel_message_id"]
        for r in required:
            if r not in data:
                return False
        return True

    @staticmethod
    def create(
        file_db_id: str,
        file_id: str,
        post_no: int,
        description: str,
        extra_message: str,
        channel_message_id: int
    ):
        """
        Helper to create a new model instance.
        """
        return FileModel(
            file_db_id=file_db_id,
            file_id=file_id,
            post_no=post_no,
            description=description,
            extra_message=extra_message,
            channel_message_id=channel_message_id,
            created_at=datetime.utcnow()
        )

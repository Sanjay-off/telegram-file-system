# bot_user/services/file_service.py

from core.database import db
from core.security.token_encryptor import encode_payload


class UserFileService:

    # -------------------------------------------------------------
    # FETCH FILE METADATA (from Admin Bot's files collection)
    # -------------------------------------------------------------
    @staticmethod
    def get_file_by_id(file_db_id: str):
        """
        Returns a file metadata document:
        {
            "file_db_id": "...",
            "file_id": "BQACAgUAA...",
            "post_no": 39,
            "description": "...",
            "extra_message": "...",
            ...
        }
        """
        return db.files.find_one({"file_db_id": file_db_id})

    # -------------------------------------------------------------
    # FETCH FILE BY RAW file_id (very common in Bot B)
    # -------------------------------------------------------------
    @staticmethod
    def get_by_file_id(file_id: str):
        """
        Some flows store file_id directly into the token,
        so we also need to fetch by file_id.
        """
        return db.files.find_one({"file_id": file_id})

    # -------------------------------------------------------------
    # GENERATE GET LINK TOKEN
    # (Used by Click Here → /start get_<token>)
    # -------------------------------------------------------------
    @staticmethod
    def create_get_token(file_id: str, post_no: int):
        payload = {
            "action": "get",
            "file_id": file_id,
            "post_no": post_no
        }
        return encode_payload(payload)

    # -------------------------------------------------------------
    # GENERATE VERIFY TOKEN
    # (Used by VERIFY NOW → /start verify_<token>)
    # -------------------------------------------------------------
    @staticmethod
    def create_verify_token(user_id: int, file_id: str, post_no: int):
        payload = {
            "action": "verify",
            "user_id": user_id,
            "file_id": file_id,
            "post_no": post_no
        }
        return encode_payload(payload)

    # -------------------------------------------------------------
    # GENERATE CLICK TOKEN
    # (Used when files are auto-deleted → /start click_<token>)
    # -------------------------------------------------------------
    @staticmethod
    def create_click_token(file_id: str, post_no: int):
        payload = {
            "action": "click",
            "file_id": file_id,
            "post_no": post_no
        }
        return encode_payload(payload)

    # -------------------------------------------------------------
    # VALIDATE IF FILE EXISTS
    # -------------------------------------------------------------
    @staticmethod
    def file_exists(file_id: str):
        return db.files.count_documents({"file_id": file_id}) > 0

    # -------------------------------------------------------------
    # GET POST NUMBER FROM FILE
    # -------------------------------------------------------------
    @staticmethod
    def get_post_no(file_id: str):
        file = db.files.find_one({"file_id": file_id})
        return file["post_no"] if file else None

    # -------------------------------------------------------------
    # GET FILE CAPTION (Password caption is fixed per your design)
    # -------------------------------------------------------------
    @staticmethod
    def file_caption():
        """
        Caption appears exactly as:
        password - Legalstuff321
        """
        return "password - Legalstuff321"

# bot_admin/services/file_service.py

from core.database import db
from datetime import datetime


class FileService:

    # -----------------------------------------------
    # CREATE / INSERT FILE
    # -----------------------------------------------
    @staticmethod
    def add_file(file_db_id: str, file_id: str, post_no: int, description: str, extra_message: str):
        """
        Save file metadata in DB under 'files' collection.
        """
        file_data = {
            "file_db_id": file_db_id,
            "file_id": file_id,
            "post_no": post_no,
            "description": description,
            "extra_message": extra_message,
            "uploaded_at": datetime.utcnow()
        }

        db.files.insert_one(file_data)
        return True

    # -----------------------------------------------
    # FETCH FILE BY ID
    # -----------------------------------------------
    @staticmethod
    def get_file(file_db_id: str):
        """
        Return the file document using file_db_id.
        """
        return db.files.find_one({"file_db_id": file_db_id})

    # -----------------------------------------------
    # LIST ALL FILES
    # -----------------------------------------------
    @staticmethod
    def list_files(limit: int = 50):
        """
        Return list of latest files.
        """
        return list(db.files.find().sort("uploaded_at", -1).limit(limit))

    # -----------------------------------------------
    # DELETE FILE BY DB ID
    # -----------------------------------------------
    @staticmethod
    def delete_file(file_db_id: str):
        """
        Delete a file entry from MongoDB.
        """
        result = db.files.delete_one({"file_db_id": file_db_id})
        return result.deleted_count > 0

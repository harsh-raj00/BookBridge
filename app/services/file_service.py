"""
File service — handles file upload and storage operations.
Provides a centralized interface for file management.
"""

import os
import shutil
import uuid
from fastapi import UploadFile

from ..config import get_settings

settings = get_settings()


def ensure_upload_dir() -> str:
    """Create the upload directory if it doesn't exist."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    return settings.UPLOAD_DIR


def save_upload_file(file: UploadFile, subfolder: str = "") -> tuple[str, str]:
    """
    Save an uploaded file to disk with a unique filename.

    Args:
        file: The uploaded file from FastAPI.
        subfolder: Optional subfolder within the upload directory.

    Returns:
        Tuple of (saved_filename, file_path).
    """
    upload_dir = ensure_upload_dir()

    if subfolder:
        upload_dir = os.path.join(upload_dir, subfolder)
        os.makedirs(upload_dir, exist_ok=True)

    # Generate a unique filename to avoid collisions
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return unique_name, file_path


def delete_file(file_path: str) -> bool:
    """
    Delete a file from disk.

    Returns:
        True if deleted, False if file didn't exist.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0

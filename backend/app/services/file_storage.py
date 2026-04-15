"""
File storage service — handles saving and deleting uploaded files on disk.
Files are stored under a configurable base directory with UUID filenames.
"""

import uuid
from pathlib import Path

from fastapi import UploadFile

# Default upload directory (relative to project root)
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "resumes"


def get_upload_dir() -> Path:
    """Get the upload directory, creating it if necessary."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOAD_DIR


def generate_filename(original_filename: str) -> str:
    """
    Generate a unique filename preserving the original extension.
    Format: <uuid>.<ext>
    """
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"


async def save_file(file: UploadFile, filename: str) -> Path:
    """
    Save an uploaded file to disk and return its absolute path.
    """
    upload_dir = get_upload_dir()
    file_path = upload_dir / filename
    contents = await file.read()
    file_path.write_bytes(contents)
    return file_path


def delete_file(file_path: str | Path) -> bool:
    """
    Delete a file from disk. Returns False if the file doesn't exist.
    """
    path = Path(file_path)
    if path.exists():
        path.unlink()
        return True
    return False


def get_file_size(file_path: str | Path) -> int:
    """Return file size in bytes."""
    return Path(file_path).stat().st_size

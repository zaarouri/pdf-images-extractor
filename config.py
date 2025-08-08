"""
Configuration settings for the PDF Image Extractor application.
"""
import os
from pathlib import Path
from typing import List

# Application settings
APP_TITLE = "📄 PDF Image Extractor"
APP_LAYOUT = "centered"
AUTHOR = "Zaarouri Abdelmounime"

# File settings
ALLOWED_EXTENSIONS = ["pdf"]
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "extracted_images"
TEMP_FOLDER = "temp"

# Image extraction settings
SUPPORTED_IMAGE_FORMATS = ["jpeg", "jpg", "png", "gif", "bmp", "tiff"]
DEFAULT_IMAGE_QUALITY = 95
MIN_IMAGE_SIZE_KB = 1  # Minimum image size to save (in KB)

# UI settings
IFRAME_HEIGHT = 500
SPINNER_TEXT = "⏳ Extracting images..."
SUCCESS_MESSAGE = "✅ {count} image(s) extracted successfully."
WARNING_MESSAGE = "⚠️ No images found in this PDF."
ERROR_MESSAGE = "❌ An error occurred while processing the PDF."

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "app.log"

# Create necessary directories
def create_directories():
    """Create all necessary directories for the application."""
    directories = [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

# File validation
def is_valid_file_type(filename: str) -> bool:
    """Check if the uploaded file has a valid extension."""
    return any(filename.lower().endswith(f".{ext}") for ext in ALLOWED_EXTENSIONS)

def is_valid_file_size(file_size_bytes: int) -> bool:
    """Check if the uploaded file size is within limits."""
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    return file_size_bytes <= max_size_bytes

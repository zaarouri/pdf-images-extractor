"""
Utility functions for file operations and data processing.
"""
import os
import zipfile
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
import streamlit as st
from logger import get_logger
from exceptions import FileOperationError, FileValidationError
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, MAX_FILE_SIZE_MB, is_valid_file_type, is_valid_file_size

logger = get_logger(__name__)

def save_uploaded_file(uploaded_file) -> str:
    """
    Save an uploaded file to the uploads directory.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to the saved file
        
    Raises:
        FileValidationError: If file validation fails
        FileOperationError: If file saving fails
    """
    try:
        # Validate file
        if not is_valid_file_type(uploaded_file.name):
            raise FileValidationError(f"Invalid file type. Only PDF files are allowed.")
        
        if not is_valid_file_size(uploaded_file.size):
            raise FileValidationError(f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB.")
        
        # Create upload directory
        upload_path = Path(UPLOAD_FOLDER)
        upload_path.mkdir(exist_ok=True)
        
        # Save file
        file_path = upload_path / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        logger.info(f"File saved successfully: {file_path}")
        return str(file_path)
        
    except Exception as e:
        logger.error(f"Error saving uploaded file: {e}")
        raise FileOperationError(f"Failed to save uploaded file: {e}")

def clear_output_folder(folder: str) -> None:
    """
    Clear all files from the output folder.
    
    Args:
        folder: Path to the folder to clear
    """
    try:
        folder_path = Path(folder)
        if folder_path.exists():
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    logger.debug(f"Deleted file: {file_path}")
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created folder: {folder_path}")
    except Exception as e:
        logger.error(f"Error clearing output folder: {e}")
        raise FileOperationError(f"Failed to clear output folder: {e}")

def zip_images(folder_path: str, zip_name: str = "extracted_images.zip") -> str:
    """
    Create a ZIP file containing all images from the specified folder.
    
    Args:
        folder_path: Path to the folder containing images
        zip_name: Name of the ZIP file
        
    Returns:
        Path to the created ZIP file
    """
    try:
        folder = Path(folder_path)
        zip_path = folder.parent / zip_name
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder.iterdir():
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)
        
        logger.info(f"ZIP file created: {zip_path}")
        return str(zip_path)
        
    except Exception as e:
        logger.error(f"Error creating ZIP file: {e}")
        raise FileOperationError(f"Failed to create ZIP file: {e}")

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    try:
        size_bytes = Path(file_path).stat().st_size
        return size_bytes / (1024 * 1024)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return 0.0

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def cleanup_temp_files() -> None:
    """
    Clean up temporary files and folders.
    """
    try:
        temp_dirs = [UPLOAD_FOLDER, OUTPUT_FOLDER]
        for temp_dir in temp_dirs:
            temp_path = Path(temp_dir)
            if temp_path.exists():
                shutil.rmtree(temp_path)
                logger.info(f"Cleaned up temporary directory: {temp_path}")
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")

def validate_pdf_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if a file is a valid PDF.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        import fitz  # PyMuPDF
        
        # Check if file exists
        if not Path(file_path).exists():
            return False, "File does not exist"
        
        # Try to open as PDF
        with fitz.open(file_path) as pdf:
            if len(pdf) == 0:
                return False, "PDF file is empty"
            
            # Check if PDF is corrupted
            if not pdf.is_pdf:
                return False, "File is not a valid PDF"
        
        return True, ""
        
    except Exception as e:
        logger.error(f"Error validating PDF file: {e}")
        return False, f"Error validating PDF: {str(e)}"

def get_image_info(image_path: str) -> dict:
    """
    Get information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing image information
    """
    try:
        from PIL import Image
        
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "file_size": format_file_size(Path(image_path).stat().st_size)
            }
    except Exception as e:
        logger.error(f"Error getting image info: {e}")
        return {}

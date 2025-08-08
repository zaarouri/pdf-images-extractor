"""
Main Streamlit application for PDF Image Extractor.
"""
import streamlit as st
from pathlib import Path
from typing import Optional, Dict, List
import traceback

# Import our modules
from config import create_directories, OUTPUT_FOLDER
from logger import setup_logger
from exceptions import PDFExtractorError, FileValidationError, FileOperationError
from utils import save_uploaded_file, clear_output_folder, zip_images, validate_pdf_file
from extract import extract_images_with_progress
from ui_components import (
    render_header, render_file_uploader, render_progress_bar, 
    render_extraction_results, render_error_message,
    render_info_section, render_footer, render_sidebar
)

# Setup logging
logger = setup_logger()

def main():
    """Main application function."""
    try:
        # Initialize directories
        create_directories()
        
        # Render header
        render_header()
        
        # Render sidebar and get settings
        settings = render_sidebar()
        
        # File upload
        uploaded_file = render_file_uploader()
        
        if uploaded_file:
            # Process the uploaded file
            process_uploaded_file(uploaded_file, settings)
        
        # Render info section and footer
        render_info_section()
        render_footer()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        logger.error(traceback.format_exc())
        st.error("An unexpected error occurred. Please try again.")

def process_uploaded_file(uploaded_file, settings: Dict):
    """
    Process the uploaded PDF file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        settings: Dictionary containing user settings
    """
    try:
        # Save uploaded file
        file_path = save_uploaded_file(uploaded_file)
        
        # Validate PDF file
        is_valid, error_message = validate_pdf_file(file_path)
        if not is_valid:
            render_error_message(error_message)
            return
        
        # Clear output folder
        clear_output_folder(OUTPUT_FOLDER)
        
        # Extract images with progress
        with st.spinner("⏳ Extracting images..."):
            # Create progress callback
            progress_placeholder = st.empty()
            
            def progress_callback(current: int, total: int):
                progress_placeholder.progress(current / total)
                progress_placeholder.caption(f"Processing page {current} of {total}")
            
            # Extract images with logo filtering
            image_paths, stats = extract_images_with_progress(
                pdf_path=file_path,
                output_folder=OUTPUT_FOLDER,
                progress_callback=progress_callback,
                filter_logos=settings.get('filter_logos', True)
            )
            
            # Clear progress
            progress_placeholder.empty()
        
        # Render results
        render_extraction_results(image_paths, stats)
        
        # Apply settings if needed
        apply_user_settings(image_paths, settings)
        
    except FileValidationError as e:
        render_error_message(str(e))
    except FileOperationError as e:
        render_error_message(str(e))
    except PDFExtractorError as e:
        render_error_message(str(e))
    except Exception as e:
        logger.error(f"Error processing uploaded file: {e}")
        logger.error(traceback.format_exc())
        render_error_message("An unexpected error occurred during processing.")

def apply_user_settings(image_paths: List[str], settings: Dict):
    """
    Apply user settings to the extracted images.
    
    Args:
        image_paths: List of extracted image paths
        settings: User settings dictionary
    """
    if not image_paths or not settings.get("optimize_images"):
        return
    
    try:
        with st.spinner("🔄 Optimizing images..."):
            # This would implement image optimization based on settings
            # For now, just show a placeholder
            st.info("Image optimization feature coming soon!")
            
    except Exception as e:
        logger.error(f"Error applying user settings: {e}")

if __name__ == "__main__":
    main()

"""
UI components for the PDF Image Extractor application.
"""
import streamlit as st
from typing import List, Dict, Optional
from pathlib import Path
import base64
from logger import get_logger
from config import IFRAME_HEIGHT, SPINNER_TEXT, SUCCESS_MESSAGE, WARNING_MESSAGE, ERROR_MESSAGE
from utils import get_image_info, format_file_size

logger = get_logger(__name__)

def render_header():
    """Render the application header."""
    st.set_page_config(
        page_title="📄 PDF Image Extractor",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
    <style>
    /* Modern styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Subheader styling */
    h2 {
        color: white !important;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: white !important;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    /* Container styling */
    .stContainer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #764ba2, #667eea);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #667eea;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* Success message styling */
    .stAlert {
        background: rgba(76, 175, 80, 0.9);
        border-radius: 10px;
        border: none;
    }
    
    /* Warning message styling */
    .stAlert[data-baseweb="notification"] {
        background: rgba(255, 193, 7, 0.9);
        border-radius: 10px;
        border: none;
    }
    
    /* Error message styling */
    .stAlert[data-baseweb="toast"] {
        background: rgba(244, 67, 54, 0.9);
        border-radius: 10px;
        border: none;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        margin: 10px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #333;
        font-weight: 500;
    }
    
    /* Image caption styling */
    .caption {
        color: #666;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 5px;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        margin: 20px 0;
        border-radius: 1px;
    }
    
    /* Info box styling */
    .stAlert[data-baseweb="notification"] {
        background: rgba(33, 150, 243, 0.9);
        border-radius: 10px;
        border: none;
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📄 PDF Image Extractor")
    st.markdown("Extract images from PDF files with ease!")

def render_file_uploader():
    """Render the file uploader component."""
    return st.file_uploader(
        "Drag & drop or browse a PDF file",
        type=["pdf"],
        accept_multiple_files=False,
        help="Upload a PDF file to extract images from it"
    )

def render_progress_bar(current: int, total: int, text: str = "Processing..."):
    """Render a progress bar."""
    progress = current / total if total > 0 else 0
    st.progress(progress)
    st.caption(f"{text} ({current}/{total})")

def render_extraction_results(image_paths: List[str], stats: Optional[Dict] = None):
    """Render the extraction results with photo selection."""
    if not image_paths:
        st.warning(WARNING_MESSAGE)
        return
    
    # Success message
    count = len(image_paths)
    st.success(SUCCESS_MESSAGE.format(count=count))
    
    # Display statistics if available
    if stats:
        render_extraction_stats(stats)
    
    # Display images with selection
    render_image_selection_gallery(image_paths)

def render_extraction_stats(stats: Dict):
    """Render extraction statistics."""
    st.subheader("📊 Extraction Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pages", stats.get("total_pages", 0))
    
    with col2:
        st.metric("Images Found", stats.get("total_images", 0))
    
    with col3:
        st.metric("Successfully Extracted", stats.get("successful_extractions", 0))
    
    with col4:
        failed = stats.get("failed_extractions", 0)
        st.metric("Failed Extractions", failed, delta=None if failed == 0 else f"-{failed}")
    
    # Total size
    total_size = stats.get("total_size_mb", 0.0)
    if total_size > 0:
        st.info(f"📦 Total extracted size: {total_size:.2f} MB")

def render_image_selection_gallery(image_paths: List[str]):
    """Render image gallery with selection for downloads."""
    st.subheader("🖼️ Extracted Images")
    
    # Initialize session state for selected images and custom names
    if 'selected_images' not in st.session_state:
        st.session_state.selected_images = set()
    if 'custom_names' not in st.session_state:
        st.session_state.custom_names = {}
    
    # Selection controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Select All", key="select_all", use_container_width=True):
            st.session_state.selected_images = set(range(len(image_paths)))
            st.rerun()
    
    with col2:
        if st.button("Clear Selection", key="clear_selection", use_container_width=True):
            st.session_state.selected_images = set()
            st.rerun()
    
    with col3:
        selected_count = len(st.session_state.selected_images)
        st.info(f"Selected: {selected_count}/{len(image_paths)}")
    
    with col4:
        if selected_count > 0:
            # Download button for selected images
            if st.button("📦 Download Selected", key="download_selected_btn", use_container_width=True):
                download_selected_images_quick(image_paths, st.session_state.selected_images)
    
    # Image grid with selection
    cols = st.columns(3)
    for i, image_path in enumerate(image_paths):
        col_idx = i % 3
        
        with cols[col_idx]:
            # Create a container for each image
            with st.container():
                # Image display
                st.image(image_path, use_column_width=True, caption=f"Image {i+1}")
                
                # Selection checkbox
                is_selected = i in st.session_state.selected_images
                if st.checkbox(f"Select Image {i+1}", value=is_selected, key=f"select_{i}"):
                    st.session_state.selected_images.add(i)
                else:
                    st.session_state.selected_images.discard(i)
                
                # Optional name input field
                default_name = st.session_state.custom_names.get(i, f"image_{i+1}")
                custom_name = st.text_input(
                    f"Name for Image {i+1}",
                    value=default_name,
                    key=f"name_{i}",
                    placeholder="Enter custom name (optional)"
                )
                if custom_name:
                    st.session_state.custom_names[i] = custom_name
                
                # Individual download button
                with open(image_path, "rb") as f:
                    image_data = f.read()
                    file_name = f"{st.session_state.custom_names.get(i, f'image_{i+1}')}.{Path(image_path).suffix}"
                    st.download_button(
                        f"📥 Download Image {i+1}",
                        image_data,
                        file_name=file_name,
                        mime="image/jpeg",
                        use_container_width=True
                    )
                
                st.divider()

def render_download_section(image_paths: List[str]):
    """Render the download section with selected images."""
    if not image_paths:
        return
    
    st.subheader("📦 Download Options")
    
    # Check if any images are selected
    selected_images = st.session_state.get('selected_images', set())
    
    if selected_images:
        # Download selected images
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Download Selected Images**")
            st.markdown(f"Download {len(selected_images)} selected images.")
            
            # Create ZIP of selected images
            if st.button("📦 Download Selected as ZIP", key="download_selected_main", use_container_width=True):
                download_selected_images(image_paths, selected_images)
        
        with col2:
            st.markdown("**Download All Images**")
            st.markdown("Download all extracted images in a ZIP file.")
            
            # Create ZIP of all images
            if st.button("📦 Download All as ZIP", key="download_all_main", use_container_width=True):
                download_all_images(image_paths)
    else:
        # No selection - show all download option
        st.markdown("**Download All Images**")
        st.markdown("Download all extracted images in a ZIP file.")
        
        if st.button("📦 Download All as ZIP", key="download_all_single", use_container_width=True):
            download_all_images(image_paths)

def download_selected_images(image_paths: List[str], selected_indices: set):
    """Download selected images as ZIP."""
    try:
        import zipfile
        import tempfile
        
        # Create temporary ZIP file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for idx in selected_indices:
                    if idx < len(image_paths):
                        image_path = image_paths[idx]
                        # Use custom name if available, otherwise use default
                        custom_name = st.session_state.custom_names.get(idx, f"image_{idx+1}")
                        arcname = f"{custom_name}.{Path(image_path).suffix}"
                        zipf.write(image_path, arcname=arcname)
            
            # Read the ZIP file
            with open(tmp_file.name, 'rb') as f:
                zip_data = f.read()
            
            # Clean up
            import os
            os.unlink(tmp_file.name)
            
            # Create download button
            st.download_button(
                "📥 Download Selected Images",
                zip_data,
                file_name="selected_images.zip",
                mime="application/zip",
                key="download_selected_zip",
                use_container_width=True
            )
            
    except Exception as e:
        logger.error(f"Error creating selected images ZIP: {e}")
        st.error("Error creating ZIP file for selected images")

def download_all_images(image_paths: List[str]):
    """Download all images as ZIP."""
    try:
        import zipfile
        import tempfile
        
        # Create temporary ZIP file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for i, image_path in enumerate(image_paths):
                    # Use custom name if available, otherwise use default
                    custom_name = st.session_state.custom_names.get(i, f"image_{i+1}")
                    arcname = f"{custom_name}.{Path(image_path).suffix}"
                    zipf.write(image_path, arcname=arcname)
            
            # Read the ZIP file
            with open(tmp_file.name, 'rb') as f:
                zip_data = f.read()
            
            # Clean up
            import os
            os.unlink(tmp_file.name)
            
            # Create download button
            st.download_button(
                "📥 Download All Images",
                zip_data,
                file_name="all_images.zip",
                mime="application/zip",
                key="download_all_zip",
                use_container_width=True
            )
            
    except Exception as e:
        logger.error(f"Error creating all images ZIP: {e}")
        st.error("Error creating ZIP file for all images")

def render_error_message(error: str):
    """Render error message."""
    st.error(f"{ERROR_MESSAGE} {error}")

def render_info_section():
    """Render information section."""
    st.markdown("---")
    # Removed the "How it works" and "Supported Formats" sections as requested

def render_footer():
    """Render the application footer."""
    st.markdown("---")
    st.markdown("### 👨‍💻 Designed by **Zaarouri Abdelmounime**")
    st.markdown("Built with ❤️ using Streamlit and PyMuPDF")

def create_download_button(file_path: str, button_text: str, file_name: str):
    """Create a download button for a file."""
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            return st.download_button(
                button_text,
                file_data,
                file_name=file_name,
                mime="application/zip"
            )
    except Exception as e:
        logger.error(f"Error creating download button: {e}")
        st.error("Error creating download button")
        return None

def render_sidebar():
    """Render sidebar with additional options."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Image quality setting
        quality = st.slider(
            "Image Quality",
            min_value=1,
            max_value=100,
            value=95,
            help="Higher quality = larger file size",
            key="quality_slider"
        )
        
        # Minimum image size filter
        min_size = st.number_input(
            "Minimum Image Size (KB)",
            min_value=0,
            value=1,
            help="Skip images smaller than this size",
            key="min_size_input"
        )
        
        # Logo filtering
        filter_logos = st.checkbox(
            "Filter Logos",
            value=True,
            help="Automatically filter out logo-like images",
            key="filter_logos_checkbox"
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            optimize_images = st.checkbox("Optimize Images", value=False, key="optimize_checkbox")
            preserve_metadata = st.checkbox("Preserve Metadata", value=True, key="metadata_checkbox")
        
        return {
            "quality": quality,
            "min_size": min_size,
            "filter_logos": filter_logos,
            "optimize_images": optimize_images,
            "preserve_metadata": preserve_metadata
        }

def download_selected_images_quick(image_paths: List[str], selected_indices: set):
    """Quick download selected images as ZIP."""
    try:
        import zipfile
        import tempfile
        
        # Create temporary ZIP file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
                for idx in selected_indices:
                    if idx < len(image_paths):
                        image_path = image_paths[idx]
                        # Use custom name if available, otherwise use default
                        custom_name = st.session_state.custom_names.get(idx, f"image_{idx+1}")
                        arcname = f"{custom_name}.{Path(image_path).suffix}"
                        zipf.write(image_path, arcname=arcname)
            
            # Read the ZIP file
            with open(tmp_file.name, 'rb') as f:
                zip_data = f.read()
            
            # Clean up
            import os
            os.unlink(tmp_file.name)
            
            # Create download button
            st.download_button(
                "📥 Download Selected Images",
                zip_data,
                file_name="selected_images.zip",
                mime="application/zip",
                key="quick_download_selected_zip",
                use_container_width=True
            )
            
    except Exception as e:
        logger.error(f"Error creating selected images ZIP: {e}")
        st.error("Error creating ZIP file for selected images")

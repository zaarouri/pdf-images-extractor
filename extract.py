"""
PDF image extraction functionality.
"""
import fitz  # PyMuPDF
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PIL import Image
import io
from logger import get_logger
from exceptions import PDFProcessingError, ImageExtractionError
from config import OUTPUT_FOLDER, SUPPORTED_IMAGE_FORMATS, MIN_IMAGE_SIZE_KB, DEFAULT_IMAGE_QUALITY

logger = get_logger(__name__)

class PDFImageExtractor:
    """
    A class to handle PDF image extraction with enhanced features.
    """
    
    def __init__(self, output_folder: str = OUTPUT_FOLDER):
        """
        Initialize the PDF image extractor.
        
        Args:
            output_folder: Directory to save extracted images
        """
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        self.extracted_images = []
        self.stats = {
            "total_pages": 0,
            "total_images": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_size_mb": 0.0,
            "filtered_logos": 0
        }
    
    def extract_images_from_pdf(self, pdf_path: str, progress_callback=None, filter_logos: bool = True) -> List[str]:
        """
        Extract all images from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            progress_callback: Optional callback function for progress updates
            filter_logos: Whether to filter out logo-like images
            
        Returns:
            List of paths to extracted images
            
        Raises:
            PDFProcessingError: If PDF processing fails
            ImageExtractionError: If image extraction fails
        """
        try:
            logger.info(f"Starting image extraction from: {pdf_path}")
            
            # Validate PDF file
            if not Path(pdf_path).exists():
                raise PDFProcessingError(f"PDF file not found: {pdf_path}")
            
            # Open PDF
            with fitz.open(pdf_path) as pdf:
                self.stats["total_pages"] = len(pdf)
                logger.info(f"Processing PDF with {self.stats['total_pages']} pages")
                
                # Process each page
                for page_index in range(len(pdf)):
                    if progress_callback:
                        progress_callback(page_index + 1, len(pdf))
                    
                    page = pdf[page_index]
                    self._extract_images_from_page(page, page_index, pdf, filter_logos)
                
                logger.info(f"Extraction completed. Stats: {self.stats}")
                return self.extracted_images
                
        except Exception as e:
            logger.error(f"Error during PDF processing: {e}")
            raise PDFProcessingError(f"Failed to process PDF: {e}")
    
    def _extract_images_from_page(self, page, page_index: int, pdf, filter_logos: bool = True) -> None:
        """
        Extract images from a single page.
        
        Args:
            page: PDF page object
            page_index: Index of the page
            pdf: PDF document object
            filter_logos: Whether to filter out logo-like images
        """
        try:
            # Get images from page
            images = page.get_images(full=True)
            
            if not images:
                logger.debug(f"No images found on page {page_index + 1}")
                return
            
            logger.debug(f"Found {len(images)} images on page {page_index + 1}")
            
            # Process each image
            for img_index, img in enumerate(images):
                try:
                    self._extract_single_image(img, page_index, img_index, pdf, filter_logos)
                except Exception as e:
                    logger.error(f"Failed to extract image {img_index + 1} from page {page_index + 1}: {e}")
                    self.stats["failed_extractions"] += 1
                    
        except Exception as e:
            logger.error(f"Error processing page {page_index + 1}: {e}")
    
    def _extract_single_image(self, img, page_index: int, img_index: int, pdf, filter_logos: bool = True) -> None:
        """
        Extract a single image from the PDF.
        
        Args:
            img: Image object from PyMuPDF
            page_index: Page index
            img_index: Image index on the page
            pdf: PDF document object
            filter_logos: Whether to filter out logo-like images
        """
        try:
            xref = img[0]
            base_image = pdf.extract_image(xref)
            
            if not base_image:
                logger.warning(f"Could not extract image data for image {img_index + 1} on page {page_index + 1}")
                return
            
            image_bytes = base_image["image"]
            image_ext = base_image["ext"].lower()
            
            # Check if image format is supported
            if image_ext not in SUPPORTED_IMAGE_FORMATS:
                logger.warning(f"Unsupported image format: {image_ext}")
                return
            
            # Check minimum image size
            image_size_kb = len(image_bytes) / 1024
            if image_size_kb < MIN_IMAGE_SIZE_KB:
                logger.debug(f"Image too small ({image_size_kb:.1f}KB), skipping")
                return
            
            # Logo filtering
            if filter_logos and self._is_logo_like(image_bytes):
                logger.debug(f"Filtered out logo-like image {img_index + 1} from page {page_index + 1}")
                self.stats["filtered_logos"] += 1
                return
            
            # Generate filename
            image_filename = f"page{page_index+1}_img{img_index+1}.{image_ext}"
            full_path = self.output_folder / image_filename
            
            # Save image
            with open(full_path, "wb") as f:
                f.write(image_bytes)
            
            # Update stats
            self.extracted_images.append(str(full_path))
            self.stats["successful_extractions"] += 1
            self.stats["total_images"] += 1
            self.stats["total_size_mb"] += len(image_bytes) / (1024 * 1024)
            
            logger.debug(f"Successfully extracted: {full_path}")
            
        except Exception as e:
            logger.error(f"Error extracting single image: {e}")
            raise ImageExtractionError(f"Failed to extract image: {e}")
    
    def _is_logo_like(self, image_bytes: bytes) -> bool:
        """
        Check if an image is logo-like based on various criteria.
        
        Args:
            image_bytes: Image data in bytes
            
        Returns:
            True if the image appears to be a logo
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get image dimensions
            width, height = image.size
            
            # Check if image is very small (likely a logo)
            if width < 100 or height < 100:
                return True
            
            # Check aspect ratio (logos are often square or have specific ratios)
            aspect_ratio = width / height
            if 0.8 <= aspect_ratio <= 1.2:  # Square-ish
                return True
            
            # Check if image has transparency (common in logos)
            if image.mode in ('RGBA', 'LA', 'P'):
                return True
            
            # Check file size (logos are often small)
            if len(image_bytes) < 10 * 1024:  # Less than 10KB
                return True
            
            # Additional checks could be added here:
            # - Color analysis (logos often have limited colors)
            # - Edge detection (logos often have sharp edges)
            # - Pattern recognition
            
            return False
            
        except Exception as e:
            logger.error(f"Error analyzing image for logo detection: {e}")
            return False
    
    def get_extraction_stats(self) -> Dict:
        """
        Get statistics about the extraction process.
        
        Returns:
            Dictionary containing extraction statistics
        """
        return self.stats.copy()
    
    def optimize_images(self, quality: int = DEFAULT_IMAGE_QUALITY) -> List[str]:
        """
        Optimize extracted images for better quality and size.
        
        Args:
            quality: JPEG quality (1-100)
            
        Returns:
            List of optimized image paths
        """
        optimized_images = []
        
        for image_path in self.extracted_images:
            try:
                optimized_path = self._optimize_single_image(image_path, quality)
                if optimized_path:
                    optimized_images.append(optimized_path)
            except Exception as e:
                logger.error(f"Error optimizing image {image_path}: {e}")
        
        return optimized_images
    
    def _optimize_single_image(self, image_path: str, quality: int) -> Optional[str]:
        """
        Optimize a single image.
        
        Args:
            image_path: Path to the image
            quality: JPEG quality
            
        Returns:
            Path to optimized image or None if optimization failed
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Create optimized filename
                path = Path(image_path)
                optimized_path = path.parent / f"{path.stem}_optimized{path.suffix}"
                
                # Save optimized image
                img.save(optimized_path, quality=quality, optimize=True)
                
                logger.debug(f"Optimized image saved: {optimized_path}")
                return str(optimized_path)
                
        except Exception as e:
            logger.error(f"Error optimizing image {image_path}: {e}")
            return None

def extract_images_from_pdf(pdf_path: str, output_folder: str = OUTPUT_FOLDER) -> List[str]:
    """
    Convenience function to extract images from a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        output_folder: Directory to save extracted images
        
    Returns:
        List of paths to extracted images
    """
    extractor = PDFImageExtractor(output_folder)
    return extractor.extract_images_from_pdf(pdf_path)

def extract_images_with_progress(pdf_path: str, output_folder: str = OUTPUT_FOLDER, 
                               progress_callback=None, filter_logos: bool = True) -> Tuple[List[str], Dict]:
    """
    Extract images with progress tracking and statistics.
    
    Args:
        pdf_path: Path to the PDF file
        output_folder: Directory to save extracted images
        progress_callback: Optional callback function for progress updates
        filter_logos: Whether to filter out logo-like images
        
    Returns:
        Tuple of (image_paths, statistics)
    """
    extractor = PDFImageExtractor(output_folder)
    image_paths = extractor.extract_images_from_pdf(pdf_path, progress_callback, filter_logos)
    stats = extractor.get_extraction_stats()
    return image_paths, stats

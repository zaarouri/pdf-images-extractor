"""
Custom exceptions for the PDF Image Extractor application.
"""

class PDFExtractorError(Exception):
    """Base exception for PDF extractor errors."""
    pass

class FileValidationError(PDFExtractorError):
    """Raised when file validation fails."""
    pass

class PDFProcessingError(PDFExtractorError):
    """Raised when PDF processing fails."""
    pass

class ImageExtractionError(PDFExtractorError):
    """Raised when image extraction fails."""
    pass

class FileOperationError(PDFExtractorError):
    """Raised when file operations fail."""
    pass

class ConfigurationError(PDFExtractorError):
    """Raised when configuration is invalid."""
    pass

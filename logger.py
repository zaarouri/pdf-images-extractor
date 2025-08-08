"""
Logging configuration for the PDF Image Extractor application.
"""
import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name: str = "pdf_extractor") -> logging.Logger:
    """
    Set up and configure the logger for the application.
    
    Args:
        name: The name of the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError:
        # If we can't write to the log file, just use console logging
        logger.warning(f"Could not create log file {LOG_FILE}. Using console logging only.")
    
    return logger

def get_logger(name: str = "pdf_extractor") -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: The name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

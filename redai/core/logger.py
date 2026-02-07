"""
Centralized Logging Configuration for RedAI
Provides consistent logging across all modules.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file with date
LOG_FILE = LOGS_DIR / f"redai_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = "redai", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and return a configured logger.
    
    Args:
        name: Logger name (usually module name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # File handler - logs everything to file
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Console handler - only warnings and above (to not clutter UI)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Default logger instance
logger = setup_logger("redai")


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Usage:
        from redai.core.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Something happened")
    """
    return setup_logger(f"redai.{module_name}")

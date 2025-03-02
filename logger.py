import logging
import os

# Define a common log file
LOG_FILE = os.path.join(os.path.dirname(__file__), "file-converter.log")

def setup_logger(script_name):
    """Sets up a reusable logger that includes the script name in logs."""
    logger = logging.getLogger(script_name)
    if not logger.hasHandlers():  # Avoid duplicate handlers
        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
    return logger

import logging
import os

# Define a common log file
LOG_FILE = os.path.join(os.path.dirname(__file__), "file-converter.log")

def setup_logger(script_name):
    """Sets up a reusable logger that includes the script name in logs."""
    logger = logging.getLogger(script_name)
    if not logger.hasHandlers():  # Avoid duplicate handlers
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

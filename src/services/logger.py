"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from typing import Optional

from src.services.config import config


def setup_logger(name: str, log_file: Optional[Path] = None) -> logging.Logger:
    """Set up a logger with console and optional file handlers.

    Args:
        name: Name of the logger
        log_file: Optional path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level))

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


app_logger = setup_logger("youtube_download", Path("./logs/app.log"))

"""
Application logging configuration.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import Settings


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name:
            Logger name.

    Returns:
        Configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(Settings.LOG_LEVEL)

    Path(Settings.LOG_DIR).mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(Settings.LOG_FORMAT)

    file_handler = RotatingFileHandler(
        Settings.LOG_FILE,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger
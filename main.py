"""
Main entry point for the Password Strength Checker application.
"""

from __future__ import annotations

from app.ui import AppUI
from app.utils.logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting Password Strength Checker application...")
    app = AppUI()
    app.mainloop()
    logger.info("Application closed.")
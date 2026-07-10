"""
Application Settings

This module stores all application-wide configuration values.
Keeping settings in one place makes the application easier to
maintain, test, and extend.
"""

from pathlib import Path


class Settings:
    """
    Central application configuration.
    """

    # ==========================================================
    # Application Information
    # ==========================================================

    APP_NAME: str = "Password Strength Checker"
    APP_VERSION: str = "1.0.0"

    # ==========================================================
    # Directory Structure
    # ==========================================================

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent

    APP_DIR: Path = PROJECT_ROOT / "app"

    ASSETS_DIR: Path = PROJECT_ROOT / "assets"

    IMAGE_DIR: Path = ASSETS_DIR / "image"

    DATA_DIR: Path = PROJECT_ROOT / "data"

    DOCS_DIR: Path = PROJECT_ROOT / "docs"

    LOG_DIR: Path = APP_DIR / "logs"

    REPORT_DIR: Path = PROJECT_ROOT / "reports"

    BUILD_DIR: Path = PROJECT_ROOT / "build"

    DIST_DIR: Path = PROJECT_ROOT / "dist"

    # ==========================================================
    # Data Files
    # ==========================================================

    IMAGE_BACKGROUND: Path = IMAGE_DIR / "images.jpg"

    COMMON_PASSWORD_FILE: Path = DATA_DIR / "common_passwords.txt"

    BREACHED_PASSWORD_FILE: Path = DATA_DIR / "breached_passwords.txt"

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_FILE: Path = LOG_DIR / "app.log"

    LOG_LEVEL: str = "INFO"

    LOG_FORMAT: str = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ==========================================================
    # Password Rules
    # ==========================================================

    MIN_PASSWORD_LENGTH: int = 8

    MAX_PASSWORD_LENGTH: int = 128

    MIN_UPPERCASE: int = 1

    MIN_LOWERCASE: int = 1

    MIN_DIGITS: int = 1

    MIN_SPECIAL_CHARACTERS: int = 1

    # ==========================================================
    # Strength Score
    # ==========================================================

    SCORE_WEAK: int = 30

    SCORE_MEDIUM: int = 60

    SCORE_STRONG: int = 80

    SCORE_VERY_STRONG: int = 100

    # ==========================================================
    # Theme
    # ==========================================================

    DEFAULT_THEME: str = "dark"

    # ==========================================================
    # Report Settings
    # ==========================================================

    REPORT_FILE_NAME: str = "password_report.pdf"

    # ==========================================================
    # Security
    # ==========================================================

    MAX_PASSWORD_INPUT_LENGTH: int = 1024

    ENABLE_LOGGING: bool = True

    ENABLE_REPORT_EXPORT: bool = True

    ENABLE_PASSWORD_HISTORY: bool = False

    # ==========================================================
    # Helper Methods
    # ==========================================================

    @classmethod
    def create_required_directories(cls) -> None:
        """
        Create required application directories if they do not exist.
        """

        directories = [
            cls.LOG_DIR,
            cls.REPORT_DIR,
            cls.BUILD_DIR,
            cls.DIST_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def as_dict(cls) -> dict:
        """
        Return all configuration values as a dictionary.
        """

        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_")
            and not callable(value)
        }


# Automatically create required folders when imported.
Settings.create_required_directories()
"""
Password validation engine.

This module validates password rules such as:

- Length
- Uppercase letters
- Lowercase letters
- Digits
- Special characters
- Whitespace
- Common passwords

It returns a PasswordCheckResult object.
"""

from __future__ import annotations

from pathlib import Path

from app.config import Settings
from app.models import PasswordCheckResult
from app.utils.constants import (
    MESSAGE_PASSWORD_EMPTY,
    MESSAGE_PASSWORD_TOO_LONG,
    MESSAGE_PASSWORD_TOO_SHORT,
    MESSAGE_PASSWORD_VALID,
)
from app.utils.helper import (
    contains_whitespace,
    count_unique_characters,
    has_digit,
    has_lowercase,
    has_special_character,
    has_uppercase,
    is_empty,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


class PasswordChecker:
    """
    Validate password against application rules.
    """

    def __init__(self) -> None:
        self._common_passwords = self._load_common_passwords()

    def _load_common_passwords(self) -> set[str]:
        """
        Load common passwords from the data file.
        """

        password_file = Settings.COMMON_PASSWORD_FILE

        if not Path(password_file).exists():
            logger.warning("Common password file not found: %s", password_file)
            return set()

        try:
            with open(password_file, "r", encoding="utf-8") as file:
                return {
                    line.strip().lower()
                    for line in file
                    if line.strip()
                }

        except Exception as error:
            logger.exception("Unable to load common passwords: %s", error)
            return set()

    def check(self, password: str) -> PasswordCheckResult:
        """
        Validate a password.

        Args:
            password:
                Password entered by the user.

        Returns:
            PasswordCheckResult
        """

        result = PasswordCheckResult(password=password)

        if is_empty(password):
            result.validation_message = MESSAGE_PASSWORD_EMPTY
            logger.info("Empty password supplied.")
            return result

        if len(password) < Settings.MIN_PASSWORD_LENGTH:
            result.validation_message = MESSAGE_PASSWORD_TOO_SHORT

        elif len(password) > Settings.MAX_PASSWORD_LENGTH:
            result.validation_message = MESSAGE_PASSWORD_TOO_LONG

        else:
            result.length_valid = True
            result.validation_message = MESSAGE_PASSWORD_VALID

        result.uppercase_valid = has_uppercase(password)

        result.lowercase_valid = has_lowercase(password)

        result.digit_valid = has_digit(password)

        result.special_character_valid = has_special_character(password)

        result.contains_whitespace = contains_whitespace(password)

        result.unique_characters = count_unique_characters(password)

        result.is_common_password = (
            password.lower() in self._common_passwords
        )

        logger.info(
            "Password validation completed."
        )

        return result
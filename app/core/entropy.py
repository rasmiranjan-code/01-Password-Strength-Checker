"""
Password entropy calculation engine.

This module estimates the strength of a password by calculating its
entropy in bits. Entropy is a measure of a password's unpredictability.

The calculation is based on the formula:

    E = L * log2(N)

Where:
- E is the entropy in bits.
- L is the password length.
- N is the size of the character pool (e.g., lowercase, uppercase,
  digits, special characters).

The module also provides a classification of the entropy level.
"""

from __future__ import annotations

import math

from app.utils.constants import (
    DIGITS,
    HIGH_ENTROPY,
    LOWERCASE_LETTERS,
    LOW_ENTROPY,
    MEDIUM_ENTROPY,
    SPECIAL_CHARACTERS,
    UPPERCASE_LETTERS,
    VERY_HIGH_ENTROPY,
)
from app.utils.helper import (
    has_digit,
    has_lowercase,
    has_special_character,
    has_uppercase,
    is_empty,
)


class PasswordEntropy:
    """
    Calculates password entropy and provides a strength classification.
    """

    def _get_character_set_size(self, password: str) -> int:
        """
        Determine the size of the character pool used in the password.

        Args:
            password: The password string.

        Returns:
            The total number of unique characters possible.
        """
        size = 0

        if has_lowercase(password):
            size += len(LOWERCASE_LETTERS)

        if has_uppercase(password):
            size += len(UPPERCASE_LETTERS)

        if has_digit(password):
            size += len(DIGITS)

        if has_special_character(password):
            size += len(SPECIAL_CHARACTERS)

        return size

    def calculate_entropy(self, password: str) -> float:
        """
        Calculate the entropy of a password in bits.

        Args:
            password: The password to analyze.

        Returns:
            The calculated entropy value, or 0.0 if invalid.
        """
        if is_empty(password):
            return 0.0

        character_set_size = self._get_character_set_size(password)

        if character_set_size <= 1:
            return 0.0

        entropy = len(password) * math.log2(character_set_size)
        return round(entropy, 2)

    def get_entropy_level(self, entropy: float) -> str:
        """
        Classify the entropy into a descriptive level.
        """
        if entropy >= 120:
            return VERY_HIGH_ENTROPY
        if entropy >= 60:
            return HIGH_ENTROPY
        if entropy >= 30:
            return MEDIUM_ENTROPY
        return LOW_ENTROPY
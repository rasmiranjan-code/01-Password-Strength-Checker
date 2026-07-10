"""
Password strength scoring engine.

This module calculates a password strength score based on various
criteria, including:

- Length
- Presence of uppercase and lowercase letters
- Presence of digits
- Presence of special characters
- Uniqueness of characters

The final score is used to classify the password's strength into
categories such as "Weak", "Medium", or "Strong".
"""

from __future__ import annotations

from app.config import Settings
from app.models import PasswordCheckResult
from app.utils.constants import (
    LENGTH_WEIGHT,
    LOWERCASE_WEIGHT,
    MEDIUM,
    MEDIUM_SCORE,
    NUMBER_WEIGHT,
    SPECIAL_CHARACTER_WEIGHT,
    STRONG,
    STRONG_SCORE,
    UNIQUENESS_WEIGHT,
    UPPERCASE_WEIGHT,
    VERY_STRONG,
    VERY_WEAK,
    WEAK,
    WEAK_SCORE,
)
from app.utils.helper import clamp


class PasswordScorer:
    """
    Calculates password strength score.
    """

    def calculate_score(self, result: PasswordCheckResult) -> int:
        """
        Calculate password strength score based on validation results.

        Args:
            result:
                A PasswordCheckResult object containing validation details.

        Returns:
            An integer score from 0 to 100.
        """
        score = 0

        if result.length_valid:
            score += LENGTH_WEIGHT

        if result.uppercase_valid:
            score += UPPERCASE_WEIGHT

        if result.lowercase_valid:
            score += LOWERCASE_WEIGHT

        if result.digit_valid:
            score += NUMBER_WEIGHT

        if result.special_character_valid:
            score += SPECIAL_CHARACTER_WEIGHT

        # Bonus for character uniqueness
        uniqueness_ratio = result.unique_characters / len(result.password) if result.password else 0
        uniqueness_bonus = int(uniqueness_ratio * UNIQUENESS_WEIGHT)
        score += uniqueness_bonus

        # Penalize common and whitespace-containing passwords
        if result.is_common_password:
            score = 0
        elif result.contains_whitespace:
            score = max(0, score - 20)

        return clamp(score, 0, 100)

    def get_strength_label(self, score: int) -> str:
        """
        Get the strength label for a given score.

        Args:
            score: The password strength score.

        Returns:
            A string label like "Weak", "Medium", "Strong".
        """
        if score >= Settings.SCORE_STRONG:
            return VERY_STRONG
        if score >= Settings.SCORE_MEDIUM:
            return STRONG
        if score >= Settings.SCORE_WEAK:
            return MEDIUM
        return WEAK
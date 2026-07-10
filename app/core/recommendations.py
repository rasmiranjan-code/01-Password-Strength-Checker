"""
Password security recommendation engine.

This module generates actionable tips to improve password strength based
on the results of the password validation checks.

Recommendations are generated for weaknesses such as:
- Insufficient length
- Missing character types (uppercase, lowercase, digits, special)
- Use of common passwords

If a password meets all criteria, a confirmation message is provided.
"""

from __future__ import annotations

from app.models import PasswordCheckResult
from app.utils.constants import (
    TIP_ADD_LOWERCASE,
    TIP_ADD_NUMBER,
    TIP_ADD_SPECIAL_CHARACTER,
    TIP_ADD_UPPERCASE,
    TIP_INCREASE_LENGTH,
    TIP_PASSWORD_EXCELLENT,
    TIP_REMOVE_COMMON_PATTERN,
    TIP_AVOID_PWNED,
)


class RecommendationEngine:
    """
    Generates password improvement recommendations.
    """

    def generate_recommendations(
        self, result: PasswordCheckResult
    ) -> list[str]:
        """
        Generate a list of recommendations based on validation results.

        Args:
            result: A PasswordCheckResult object.

        Returns:
            A list of recommendation strings.
        """
        recommendations = []

        if not result.length_valid:
            recommendations.append(TIP_INCREASE_LENGTH)
        if not result.uppercase_valid:
            recommendations.append(TIP_ADD_UPPERCASE)
        if not result.lowercase_valid:
            recommendations.append(TIP_ADD_LOWERCASE)
        if not result.digit_valid:
            recommendations.append(TIP_ADD_NUMBER)
        if not result.special_character_valid:
            recommendations.append(TIP_ADD_SPECIAL_CHARACTER)
        if result.is_common_password:
            recommendations.append(TIP_REMOVE_COMMON_PATTERN)
        if result.is_pwned:
            recommendations.append(TIP_AVOID_PWNED)

        if not recommendations and result.passed_all_checks():
            recommendations.append(TIP_PASSWORD_EXCELLENT)

        return recommendations
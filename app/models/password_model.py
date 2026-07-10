"""
Password data models.

This module contains the data structures used throughout the
Password Strength Checker application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class PasswordCheckResult:
    """
    Stores the result of password rule validation.
    """

    password: str

    length_valid: bool = False
    uppercase_valid: bool = False
    lowercase_valid: bool = False
    digit_valid: bool = False
    special_character_valid: bool = False

    is_common_password: bool = False
    is_pwned: bool = False
    contains_whitespace: bool = False

    unique_characters: int = 0

    validation_message: str = ""

    def passed_all_checks(self) -> bool:
        """
        Return True if all validation rules are satisfied.
        """

        return (
            self.length_valid
            and self.uppercase_valid
            and self.lowercase_valid
            and self.digit_valid
            and self.special_character_valid
            and not self.is_common_password
            and not self.is_pwned
            and not self.contains_whitespace
        )


@dataclass(slots=True)
class PasswordAnalysisResult:
    """
    Final password analysis result.
    """

    password: str

    score: int = 0

    strength: str = "Unknown"

    entropy: float = 0.0

    entropy_level: str = "Unknown"

    estimated_crack_time: str = "Unknown"

    validation: PasswordCheckResult | None = None

    recommendations: List[str] = field(default_factory=list)

    analysed_successfully: bool = False

    def add_recommendation(self, message: str) -> None:
        """
        Add a recommendation if it does not already exist.
        """

        if message not in self.recommendations:
            self.recommendations.append(message)

    def clear_recommendations(self) -> None:
        """
        Remove every recommendation.
        """

        self.recommendations.clear()

    @property
    def recommendation_count(self) -> int:
        """
        Total recommendation count.
        """

        return len(self.recommendations)

    @property
    def is_secure(self) -> bool:
        """
        Return True if the password is considered secure.
        """

        return (
            self.validation is not None
            and self.validation.passed_all_checks()
            and self.score >= 80
        )

    def to_dict(self) -> dict:
        """
        Convert analysis result into a dictionary.
        """

        return {
            "password": self.password,
            "score": self.score,
            "strength": self.strength,
            "entropy": self.entropy,
            "entropy_level": self.entropy_level,
            "estimated_crack_time": self.estimated_crack_time,
            "recommendations": self.recommendations,
            "recommendation_count": self.recommendation_count,
            "analysed_successfully": self.analysed_successfully,
            "is_secure": self.is_secure,
        }
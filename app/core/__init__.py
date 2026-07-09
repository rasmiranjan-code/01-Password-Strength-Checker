"""
Core package for the Password Strength Checker application.

The core package contains the business logic responsible for
password analysis, validation, scoring, entropy calculation,
and security recommendations.

Modules
-------
checker
    Performs password rule validation.

scorer
    Calculates password strength score.

entropy
    Estimates password entropy.

recommendations
    Generates security recommendations.

analyzer
    Coordinates the complete password analysis workflow.
"""

from .checker import PasswordChecker
from .scorer import PasswordScorer
from .entropy import PasswordEntropy
from .recommendations import RecommendationEngine
from .analyzer import PasswordAnalyzer

__all__ = [
    "PasswordChecker",
    "PasswordScorer",
    "PasswordEntropy",
    "RecommendationEngine",
    "PasswordAnalyzer",
]
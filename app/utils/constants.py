"""
Application Constants

This module stores all reusable constants used throughout
the Password Strength Checker application.

Keeping constants in a single location improves maintainability,
consistency, and reduces hard-coded values.
"""

from __future__ import annotations

import string
from typing import Final


# ==========================================================
# Application Information
# ==========================================================

APP_AUTHOR: Final[str] = ""
APP_LICENSE: Final[str] = "MIT"


# ==========================================================
# Password Character Sets
# ==========================================================

LOWERCASE_LETTERS: Final[str] = string.ascii_lowercase

UPPERCASE_LETTERS: Final[str] = string.ascii_uppercase

DIGITS: Final[str] = string.digits

SPECIAL_CHARACTERS: Final[str] = string.punctuation

ALL_CHARACTERS: Final[str] = (
    LOWERCASE_LETTERS
    + UPPERCASE_LETTERS
    + DIGITS
    + SPECIAL_CHARACTERS
)


# ==========================================================
# Password Strength Labels
# ==========================================================

VERY_WEAK: Final[str] = "Very Weak"

WEAK: Final[str] = "Weak"

MEDIUM: Final[str] = "Medium"

STRONG: Final[str] = "Strong"

VERY_STRONG: Final[str] = "Very Strong"


# ==========================================================
# Password Score Ranges
# ==========================================================

VERY_WEAK_SCORE: Final[int] = 20

WEAK_SCORE: Final[int] = 40

MEDIUM_SCORE: Final[int] = 60

STRONG_SCORE: Final[int] = 80

VERY_STRONG_SCORE: Final[int] = 100


# ==========================================================
# Password Length
# ==========================================================

MIN_PASSWORD_LENGTH: Final[int] = 8

RECOMMENDED_PASSWORD_LENGTH: Final[int] = 12

MAX_PASSWORD_LENGTH: Final[int] = 128


# ==========================================================
# Password Rule Weights
# ==========================================================

LENGTH_WEIGHT: Final[int] = 30

UPPERCASE_WEIGHT: Final[int] = 15

LOWERCASE_WEIGHT: Final[int] = 15

NUMBER_WEIGHT: Final[int] = 15

SPECIAL_CHARACTER_WEIGHT: Final[int] = 20

UNIQUENESS_WEIGHT: Final[int] = 5


# ==========================================================
# Regular Expression Patterns
# ==========================================================

REGEX_UPPERCASE: Final[str] = r"[A-Z]"

REGEX_LOWERCASE: Final[str] = r"[a-z]"

REGEX_DIGIT: Final[str] = r"\d"

REGEX_SPECIAL_CHARACTER: Final[str] = (
    r"[!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]"
)


# ==========================================================
# Common Password Messages
# ==========================================================

MESSAGE_PASSWORD_EMPTY: Final[str] = "Password cannot be empty."

MESSAGE_PASSWORD_TOO_SHORT: Final[str] = (
    "Password length is too short."
)

MESSAGE_PASSWORD_TOO_LONG: Final[str] = (
    "Password exceeds the allowed length."
)

MESSAGE_PASSWORD_VALID: Final[str] = (
    "Password is valid."
)


# ==========================================================
# Recommendation Messages
# ==========================================================

TIP_ADD_UPPERCASE: Final[str] = (
    "Add at least one uppercase letter."
)

TIP_ADD_LOWERCASE: Final[str] = (
    "Add at least one lowercase letter."
)

TIP_ADD_NUMBER: Final[str] = (
    "Include at least one numeric digit."
)

TIP_ADD_SPECIAL_CHARACTER: Final[str] = (
    "Use at least one special character."
)

TIP_INCREASE_LENGTH: Final[str] = (
    "Increase password length."
)

TIP_REMOVE_COMMON_PATTERN: Final[str] = (
    "Avoid common words or predictable patterns."
)

TIP_AVOID_PWNED: Final[str] = (
    "This password has appeared in a data breach. Do not use it."
)

TIP_PASSWORD_EXCELLENT: Final[str] = (
    "Excellent password. No obvious weaknesses detected."
)


# ==========================================================
# Password Status
# ==========================================================

STATUS_PASS: Final[str] = "PASS"

STATUS_FAIL: Final[str] = "FAIL"

STATUS_WARNING: Final[str] = "WARNING"


# ==========================================================
# Entropy Levels
# ==========================================================

LOW_ENTROPY: Final[str] = "Low"

MEDIUM_ENTROPY: Final[str] = "Medium"

HIGH_ENTROPY: Final[str] = "High"

VERY_HIGH_ENTROPY: Final[str] = "Very High"


# ==========================================================
# Crack Time Labels
# ==========================================================

CRACK_INSTANT: Final[str] = "Instantly"

CRACK_SECONDS: Final[str] = "Seconds"

CRACK_MINUTES: Final[str] = "Minutes"

CRACK_HOURS: Final[str] = "Hours"

CRACK_DAYS: Final[str] = "Days"

CRACK_MONTHS: Final[str] = "Months"

CRACK_YEARS: Final[str] = "Years"

CRACK_CENTURIES: Final[str] = "Centuries"


# ==========================================================
# File Names
# ==========================================================

COMMON_PASSWORD_FILE: Final[str] = "common_passwords.txt"

BREACHED_PASSWORD_FILE: Final[str] = "breached_passwords.txt"


# ==========================================================
# UI Colors (Future GUI)
# ==========================================================

COLOR_SUCCESS: Final[str] = "#16A34A"

COLOR_WARNING: Final[str] = "#F59E0B"

COLOR_DANGER: Final[str] = "#DC2626"

COLOR_INFO: Final[str] = "#2563EB"


# ==========================================================
# Theme
# ==========================================================

THEME_DARK: Final[str] = "dark"

THEME_LIGHT: Final[str] = "light"
"""
General helper functions used across the application.
"""

from __future__ import annotations

import re
from typing import Iterable


def is_empty(value: str | None) -> bool:
    """
    Check whether the given string is empty.

    Args:
        value: Input string.

    Returns:
        True if empty or only whitespace.
    """
    return value is None or value.strip() == ""


def has_uppercase(password: str) -> bool:
    """
    Return True if password contains an uppercase letter.
    """
    return bool(re.search(r"[A-Z]", password))


def has_lowercase(password: str) -> bool:
    """
    Return True if password contains a lowercase letter.
    """
    return bool(re.search(r"[a-z]", password))


def has_digit(password: str) -> bool:
    """
    Return True if password contains a numeric digit.
    """
    return bool(re.search(r"\d", password))


def has_special_character(password: str) -> bool:
    """
    Return True if password contains a special character.
    """
    return bool(re.search(r"[!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]", password))


def count_unique_characters(password: str) -> int:
    """
    Count unique characters in a password.
    """
    return len(set(password))


def contains_whitespace(password: str) -> bool:
    """
    Check whether password contains whitespace.
    """
    return any(character.isspace() for character in password)


def percentage(value: int | float, maximum: int | float) -> float:
    """
    Calculate percentage safely.
    """
    if maximum <= 0:
        return 0.0

    return round((value / maximum) * 100, 2)


def clamp(value: int, minimum: int, maximum: int) -> int:
    """
    Restrict value between minimum and maximum.
    """
    return max(minimum, min(value, maximum))


def remove_duplicates(items: Iterable[str]) -> list[str]:
    """
    Remove duplicate values while preserving order.
    """
    return list(dict.fromkeys(items))
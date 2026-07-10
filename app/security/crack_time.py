"""
Password crack time estimation.

This module estimates how long it would take to crack a password
based on its entropy and assumed cracking speeds.
"""

from __future__ import annotations

from app.utils.constants import (
    CRACK_CENTURIES,
    CRACK_DAYS,
    CRACK_HOURS,
    CRACK_INSTANT,
    CRACK_MINUTES,
    CRACK_MONTHS,
    CRACK_SECONDS,
    CRACK_YEARS,
)


class CrackTimeEstimator:
    """
    Estimates password crack time.
    """

    # Assumptions for cracking speed (guesses per second)
    OFFLINE_ATTACK_SPEED = 10_000_000_000  # 10 billion guesses per second

    def estimate_crack_time(self, entropy: float) -> str:
        """
        Estimate the time to crack a password based on its entropy.

        Args:
            entropy: The password's entropy in bits.

        Returns:
            A human-readable string representing the estimated crack time.
        """
        if entropy <= 0:
            return CRACK_INSTANT

        # Number of possible combinations = 2^entropy
        combinations = 2**entropy

        # Time in seconds for an offline attack
        seconds_to_crack = combinations / self.OFFLINE_ATTACK_SPEED

        return self._format_time(seconds_to_crack)

    def _format_time(self, seconds: float) -> str:
        """
        Convert seconds into a human-readable format.
        """
        if seconds < 1:
            return CRACK_INSTANT
        if seconds < 60:
            return f"{int(seconds)} {CRACK_SECONDS}"

        minutes = seconds / 60
        if minutes < 60:
            return f"{int(minutes)} {CRACK_MINUTES}"

        hours = minutes / 60
        if hours < 24:
            return f"{int(hours)} {CRACK_HOURS}"

        days = hours / 24
        if days < 30:
            return f"{int(days)} {CRACK_DAYS}"

        months = days / 30
        if months < 12:
            return f"{int(months)} {CRACK_MONTHS}"

        years = days / 365
        if years < 100:
            return f"{int(years)} {CRACK_YEARS}"

        return f"Thousands of {CRACK_CENTURIES}"
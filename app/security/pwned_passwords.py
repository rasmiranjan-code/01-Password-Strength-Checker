"""
Pwned Passwords Checker.

This module checks if a password has been exposed in a data breach
by using the 'Have I Been Pwned' (HIBP) Pwned Passwords API.

It uses the k-Anonymity model, where only the first 5 characters
of a SHA-1 hash of the password are sent to the API.
"""

from __future__ import annotations

import hashlib

import requests

from app.utils.logger import get_logger


logger = get_logger(__name__)


class PwnedPasswordChecker:
    """
    Checks passwords against the HIBP Pwned Passwords database.
    """

    API_URL = "https://api.pwnedpasswords.com/range/"

    def check_password(self, password: str) -> int:
        """
        Check if a password is pwned and return its breach count.

        Args:
            password: The password to check.

        Returns:
            The number of times the password has been found in breaches,
            or 0 if it's not found or an error occurs.
        """
        if not password:
            return 0

        try:
            # 1. Hash the password with SHA-1
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
            prefix, suffix = sha1_hash[:5], sha1_hash[5:]

            # 2. Query the HIBP API with the hash prefix
            response = requests.get(f"{self.API_URL}{prefix}", timeout=5)
            response.raise_for_status()

            # 3. Check the response for the hash suffix
            hashes = (line.split(":") for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    logger.warning(
                        "Password found in a data breach %s times.", count
                    )
                    return int(count)

            logger.info("Password not found in any known data breaches.")
            return 0

        except requests.RequestException as e:
            logger.error("Error checking pwned password API: %s", e)
            # Fail safely: assume not pwned if the service is down
            return 0
        except Exception as e:
            logger.exception("An unexpected error occurred in PwnedPasswordChecker: %s", e)
            return 0
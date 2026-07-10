"""
Security analysis package.

This package provides modules for advanced security checks, such as:
- Estimating password crack time.
- Checking against known data breaches (pwned passwords).
"""

from .crack_time import CrackTimeEstimator
from .pwned_passwords import PwnedPasswordChecker

__all__ = ["CrackTimeEstimator", "PwnedPasswordChecker"]
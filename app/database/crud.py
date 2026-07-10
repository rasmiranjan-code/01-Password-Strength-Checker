"""
CRUD (Create, Read, Update, Delete) operations for database models.
"""

from __future__ import annotations

import hashlib

from sqlalchemy.orm import Session

from app.models import PasswordAnalysisResult

from . import models


def _hash_password(password: str) -> str:
    """
    Create a SHA-256 hash of the password for storage.
    Note: For a real-world application, use a stronger, salted hash
          like one from passlib.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_analysis_entry(
    db: Session, analysis_result: PasswordAnalysisResult
) -> models.AnalysisHistory:
    """
    Create and store a new password analysis history entry.

    Args:
        db: The database session.
        analysis_result: The result from the PasswordAnalyzer.

    Returns:
        The created AnalysisHistory object.
    """
    password_hash = _hash_password(analysis_result.password)

    db_entry = models.AnalysisHistory(
        password_hash=password_hash,
        score=analysis_result.score,
        strength=analysis_result.strength,
        entropy=analysis_result.entropy,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_analysis_history(db: Session, skip: int = 0, limit: int = 100) -> list[models.AnalysisHistory]:
    """Retrieve all analysis history records."""
    return db.query(models.AnalysisHistory).offset(skip).limit(limit).all()
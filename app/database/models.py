"""
Database ORM models.

This module defines the SQLAlchemy models that map to database tables.
"""

from __future__ import annotations

import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from .database import Base


class AnalysisHistory(Base):
    """
    Represents a single password analysis record in the database.
    """

    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    strength = Column(String, nullable=False)
    entropy = Column(Float, nullable=False)
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )
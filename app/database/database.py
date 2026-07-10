"""
Database connection and session management.

This module sets up the SQLAlchemy engine and session for the
application's database. It uses SQLite for simplicity.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.utils.logger import get_logger


logger = get_logger(__name__)

# Define the database file path within the project's data directory
DATABASE_FILE = Settings.DATA_DIR / "password_analysis.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database and create tables."""
    logger.info("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
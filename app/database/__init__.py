"""
Database package for the Password Strength Checker application.

This package handles all database interactions, including:
- Connection management
- Session handling
- Data models (schema)
- CRUD (Create, Read, Update, Delete) operations
"""

from .crud import create_analysis_entry, get_analysis_history
from .database import Base, SessionLocal, engine, get_db, init_db

__all__ = ["Base", "SessionLocal", "engine", "get_db", "init_db", "create_analysis_entry", "get_analysis_history"]
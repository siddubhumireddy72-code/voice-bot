"""Database initialization and management"""
from flask import current_app
from database.models import db, Call, Transcript, BotResponse


def init_db():
    """Initialize database tables"""
    try:
        db.create_all()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise


def drop_db():
    """Drop all database tables (use with caution!)"""
    try:
        db.drop_all()
        print("Database dropped successfully")
    except Exception as e:
        print(f"Error dropping database: {str(e)}")
        raise


def reset_db():
    """Reset database (drop and recreate)"""
    drop_db()
    init_db()

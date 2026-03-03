"""Database management for Flask AI Workshop.

This module handles all database operations including:
- Database initialization
- User management (create, read)
- Connection management with proper cleanup
"""

import sqlite3
from contextlib import contextmanager
from config import config


@contextmanager
def get_db():
    """Get a database connection with automatic cleanup.
    
    This is a context manager that ensures the database connection
    is properly closed even if an error occurs.
    
    Usage:
        with get_db() as db:
            db.execute('SELECT * FROM users')
    
    Yields:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(config.DATABASE)
    # Return rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables.
    
    Creates the users table if it doesn't exist.
    Safe to call multiple times - won't recreate existing tables.
    """
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                google_id TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                profile_picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Database initialized successfully!")


def get_user_by_email(email):
    """Fetch a user from the database by email.
    
    Args:
        email (str): User's email address
    
    Returns:
        dict: User data as dictionary, or None if not found
    """
    with get_db() as db:
        cursor = db.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None


def get_user_by_google_id(google_id):
    """Fetch a user from the database by Google ID.
    
    Args:
        google_id (str): User's Google ID
    
    Returns:
        dict: User data as dictionary, or None if not found
    """
    with get_db() as db:
        cursor = db.execute(
            'SELECT * FROM users WHERE google_id = ?',
            (google_id,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None


def create_user(google_id, email, name, profile_picture=None):
    """Create a new user in the database.
    
    Args:
        google_id (str): User's Google ID
        email (str): User's email address
        name (str): User's full name
        profile_picture (str, optional): URL to user's profile picture
    
    Returns:
        int: The ID of the newly created user
    """
    with get_db() as db:
        cursor = db.execute(
            '''
            INSERT INTO users (google_id, email, name, profile_picture)
            VALUES (?, ?, ?, ?)
            ''',
            (google_id, email, name, profile_picture)
        )
        return cursor.lastrowid


def update_user(google_id, email, name, profile_picture=None):
    """Update an existing user's information.
    
    Args:
        google_id (str): User's Google ID
        email (str): User's email address
        name (str): User's full name
        profile_picture (str, optional): URL to user's profile picture
    
    Returns:
        bool: True if user was updated, False otherwise
    """
    with get_db() as db:
        cursor = db.execute(
            '''
            UPDATE users 
            SET email = ?, name = ?, profile_picture = ?
            WHERE google_id = ?
            ''',
            (email, name, profile_picture, google_id)
        )
        return cursor.rowcount > 0

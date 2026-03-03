"""PostgreSQL-compatible database layer for production deployment.

This file provides PostgreSQL support while maintaining SQLite compatibility
for local development. The app automatically detects the database type.
"""

import os
from contextlib import contextmanager
from datetime import datetime
import json

# Detect database type from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database.db')

# Normalize PostgreSQL URL (Render/Heroku use different formats)
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

IS_POSTGRESQL = DATABASE_URL.startswith('postgresql://')

if IS_POSTGRESQL:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    print(f"[DB] Using PostgreSQL")
else:
    import sqlite3
    print(f"[DB] Using SQLite")


@contextmanager
def get_db():
    """Context manager for database connections.
    Works with both PostgreSQL and SQLite.
    """
    if IS_POSTGRESQL:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        try:
            yield conn
        finally:
            conn.commit()
            conn.close()
    else:
        conn = sqlite3.connect('database.db', timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.commit()
            conn.close()


def init_db():
    """Initialize database with required tables.
    
    Handles both PostgreSQL and SQLite syntax differences.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        if IS_POSTGRESQL:
            # PostgreSQL syntax
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    google_id VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    picture TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title TEXT DEFAULT 'New Chat',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INTEGER NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    has_attachment INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            ''')
            
            # Attachments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attachments (
                    id SERIAL PRIMARY KEY,
                    message_id INTEGER NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    original_filename VARCHAR(255) NOT NULL,
                    file_type VARCHAR(50) NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_attachments_message_id ON attachments(message_id)')
            
        else:
            # SQLite syntax (existing)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    google_id TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    picture TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT DEFAULT 'New Chat',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    has_attachment INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_attachments_message_id ON attachments(message_id)')
        
        conn.commit()
        print(f"[DB] Database initialized successfully! (Type: {'PostgreSQL' if IS_POSTGRESQL else 'SQLite'})")


# ============================================================================
# QUERY HELPERS - Handle PostgreSQL vs SQLite differences
# ============================================================================

def execute_query(cursor, query, params=None, fetch_one=False, fetch_all=False):
    """Execute query with proper parameter binding for PostgreSQL/SQLite."""
    if IS_POSTGRESQL:
        # PostgreSQL uses %s placeholders
        query = query.replace('?', '%s')
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if fetch_one:
        result = cursor.fetchone()
        return dict(result) if result else None
    elif fetch_all:
        return [dict(row) for row in cursor.fetchall()]
    else:
        return cursor.lastrowid


# ============================================================================
# USER OPERATIONS
# ============================================================================

def get_user_by_google_id(google_id):
    """Get user by their Google ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        result = execute_query(cursor, 'SELECT * FROM users WHERE google_id = ?', (google_id,), fetch_one=True)
        print(f"[DB] get_user_by_google_id({google_id}): {'Found' if result else 'Not found'}")
        return result


def create_user(google_id, email, name, picture=None):
    """Create a new user."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'INSERT INTO users (google_id, email, name, picture) VALUES (?, ?, ?, ?)'
        user_id = execute_query(cursor, query, (google_id, email, name, picture))
        conn.commit()
        print(f"[DB] create_user({email}): Created with ID {user_id}")
        return user_id


def update_user(google_id, email, name, picture=None):
    """Update user information and last login time."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'UPDATE users SET email = ?, name = ?, picture = ?, last_login = CURRENT_TIMESTAMP WHERE google_id = ?'
        execute_query(cursor, query, (email, name, picture, google_id))
        conn.commit()
        print(f"[DB] update_user({email}): Updated")


def get_user_id_by_google_id(google_id):
    """Get user's database ID by their Google ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        result = execute_query(cursor, 'SELECT id FROM users WHERE google_id = ?', (google_id,), fetch_one=True)
        user_id = result['id'] if result else None
        print(f"[DB] get_user_id_by_google_id({google_id}): {user_id}")
        return user_id


# ============================================================================
# CONVERSATION OPERATIONS
# ============================================================================

def create_conversation(user_id, title='New Chat'):
    """Create a new conversation for a user."""
    print(f"[DB] create_conversation: user_id={user_id}, title='{title}'")
    
    if user_id is None:
        print(f"[DB ERROR] create_conversation: user_id is None!")
        raise ValueError("user_id cannot be None")
    
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'INSERT INTO conversations (user_id, title) VALUES (?, ?)'
        conv_id = execute_query(cursor, query, (user_id, title))
        conn.commit()
        print(f"[DB] create_conversation: Created conversation ID {conv_id}")
        return conv_id


def get_user_conversations(user_id, limit=20):
    """Get all conversations for a user."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT 
                c.id,
                c.title,
                c.created_at,
                c.updated_at,
                COUNT(m.id) as message_count,
                MAX(m.created_at) as last_message_at
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.user_id = ?
            GROUP BY c.id
            ORDER BY c.updated_at DESC
            LIMIT ?
        '''
        conversations = execute_query(cursor, query, (user_id, limit), fetch_all=True)
        print(f"[DB] get_user_conversations({user_id}): Found {len(conversations)} conversations")
        return conversations


def get_conversation(conversation_id, user_id):
    """Get a specific conversation."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM conversations WHERE id = ? AND user_id = ?'
        result = execute_query(cursor, query, (conversation_id, user_id), fetch_one=True)
        print(f"[DB] get_conversation({conversation_id}, {user_id}): {'Found' if result else 'Not found'}")
        return result


def delete_conversation(conversation_id, user_id):
    """Delete a conversation."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'DELETE FROM conversations WHERE id = ? AND user_id = ?'
        execute_query(cursor, query, (conversation_id, user_id))
        conn.commit()
        success = cursor.rowcount > 0
        print(f"[DB] delete_conversation({conversation_id}): {'Success' if success else 'Failed'}")
        return success


def update_conversation_title(conversation_id, title, user_id):
    """Update conversation title."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?'
        execute_query(cursor, query, (title, conversation_id, user_id))
        conn.commit()
        success = cursor.rowcount > 0
        print(f"[DB] update_conversation_title({conversation_id}): {'Success' if success else 'Failed'}")
        return success


# ============================================================================
# MESSAGE OPERATIONS
# ============================================================================

def add_message(conversation_id, role, content, has_attachment=False):
    """Add a message to a conversation."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'INSERT INTO messages (conversation_id, role, content, has_attachment) VALUES (?, ?, ?, ?)'
        message_id = execute_query(cursor, query, (conversation_id, role, content, 1 if has_attachment else 0))
        
        # Update conversation timestamp
        update_query = 'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?'
        execute_query(cursor, update_query, (conversation_id,))
        
        conn.commit()
        print(f"[DB] add_message({conversation_id}, {role}): Created message ID {message_id}")
        return message_id


def get_conversation_messages(conversation_id, user_id, include_attachments=True):
    """Get all messages in a conversation."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify ownership
        verify_query = 'SELECT 1 FROM conversations WHERE id = ? AND user_id = ?'
        if not execute_query(cursor, verify_query, (conversation_id, user_id), fetch_one=True):
            print(f"[DB] get_conversation_messages: User {user_id} doesn't own conversation {conversation_id}")
            return []
        
        # Get messages
        query = 'SELECT id, role, content, has_attachment, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC'
        messages = execute_query(cursor, query, (conversation_id,), fetch_all=True)
        
        print(f"[DB] get_conversation_messages({conversation_id}): Found {len(messages)} messages")
        return messages


# ============================================================================
# ATTACHMENT OPERATIONS
# ============================================================================

def add_attachment(message_id, filename, original_filename, file_type, file_size, file_path):
    """Add an attachment record."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'INSERT INTO attachments (message_id, filename, original_filename, file_type, file_size, file_path) VALUES (?, ?, ?, ?, ?, ?)'
        attachment_id = execute_query(cursor, query, (message_id, filename, original_filename, file_type, file_size, file_path))
        conn.commit()
        print(f"[DB] add_attachment({message_id}): Created attachment ID {attachment_id}")
        return attachment_id


def get_message_attachments(message_id):
    """Get all attachments for a message."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'SELECT id, filename, original_filename, file_type, file_size, file_path, created_at FROM attachments WHERE message_id = ?'
        return execute_query(cursor, query, (message_id,), fetch_all=True)


def generate_conversation_title(first_message):
    """Generate a title from the first message."""
    title = first_message[:50]
    if len(first_message) > 50:
        title += '...'
    return title


# Alias for backwards compatibility
DATABASE_FILE = 'database.db' if not IS_POSTGRESQL else 'PostgreSQL'

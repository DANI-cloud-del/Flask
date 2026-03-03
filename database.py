"""Database operations for the Flask AI application.

Handles SQLite database initialization and CRUD operations for:
- User management
- Chat conversation storage
- Message history
- File attachments
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
import json

DATABASE_FILE = 'database.db'


@contextmanager
def get_db():
    """Context manager for database connections.
    
    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
    """
    conn = sqlite3.connect(DATABASE_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    conn.isolation_level = None  # Autocommit mode
    try:
        yield conn
    except Exception as e:
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with required tables."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Users table
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
        
        # Conversations table
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
        
        # Messages table (updated with attachment support)
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
        
        # Attachments table (NEW)
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
        
        # Create indexes for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
            ON conversations(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
            ON messages(conversation_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_attachments_message_id 
            ON attachments(message_id)
        ''')
        
        print("Database initialized successfully!")


# ============================================================================
# USER OPERATIONS
# ============================================================================

def get_user_by_google_id(google_id):
    """Get user by their Google ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
        return cursor.fetchone()


def create_user(google_id, email, name, picture=None):
    """Create a new user."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (google_id, email, name, picture)
            VALUES (?, ?, ?, ?)
        ''', (google_id, email, name, picture))
        return cursor.lastrowid


def update_user(google_id, email, name, picture=None):
    """Update user information and last login time."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET email = ?, name = ?, picture = ?, last_login = CURRENT_TIMESTAMP
            WHERE google_id = ?
        ''', (email, name, picture, google_id))


def get_user_id_by_google_id(google_id):
    """Get user's database ID by their Google ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE google_id = ?', (google_id,))
        result = cursor.fetchone()
        return result['id'] if result else None


# ============================================================================
# CONVERSATION OPERATIONS
# ============================================================================

def create_conversation(user_id, title='New Chat'):
    """Create a new conversation for a user."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, title)
            VALUES (?, ?)
        ''', (user_id, title))
        return cursor.lastrowid


def get_user_conversations(user_id, limit=20):
    """Get all conversations for a user, ordered by most recent."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
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
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]


def get_conversation(conversation_id, user_id):
    """Get a specific conversation (with ownership check)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM conversations 
            WHERE id = ? AND user_id = ?
        ''', (conversation_id, user_id))
        result = cursor.fetchone()
        return dict(result) if result else None


def update_conversation_title(conversation_id, title, user_id):
    """Update conversation title."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations 
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (title, conversation_id, user_id))
        return cursor.rowcount > 0


def delete_conversation(conversation_id, user_id):
    """Delete a conversation (with ownership check)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM conversations 
            WHERE id = ? AND user_id = ?
        ''', (conversation_id, user_id))
        return cursor.rowcount > 0


def update_conversation_timestamp(conversation_id):
    """Update the conversation's updated_at timestamp."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))


# ============================================================================
# MESSAGE OPERATIONS
# ============================================================================

def add_message(conversation_id, role, content, has_attachment=False):
    """Add a message to a conversation.
    
    Args:
        conversation_id: ID of the conversation
        role: 'user' or 'assistant'
        content: Message text
        has_attachment: Boolean indicating if message has attachments
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Insert message
        cursor.execute('''
            INSERT INTO messages (conversation_id, role, content, has_attachment)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, role, content, 1 if has_attachment else 0))
        message_id = cursor.lastrowid
        
        # Update conversation timestamp
        cursor.execute('''
            UPDATE conversations 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))
        
        return message_id


def get_conversation_messages(conversation_id, user_id, include_attachments=True):
    """Get all messages in a conversation (with ownership check)."""
    with get_db() as conn:
        cursor = conn.cursor()
        # First verify user owns this conversation
        cursor.execute('''
            SELECT 1 FROM conversations 
            WHERE id = ? AND user_id = ?
        ''', (conversation_id, user_id))
        
        if not cursor.fetchone():
            return None
        
        # Get messages
        cursor.execute('''
            SELECT id, role, content, has_attachment, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
        ''', (conversation_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
        
        # Get attachments if requested
        if include_attachments:
            for message in messages:
                if message['has_attachment']:
                    message['attachments'] = get_message_attachments(message['id'])
        
        return messages


# ============================================================================
# ATTACHMENT OPERATIONS (NEW)
# ============================================================================

def add_attachment(message_id, filename, original_filename, file_type, file_size, file_path):
    """Add an attachment record."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attachments (message_id, filename, original_filename, file_type, file_size, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (message_id, filename, original_filename, file_type, file_size, file_path))
        return cursor.lastrowid


def get_message_attachments(message_id):
    """Get all attachments for a message."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, original_filename, file_type, file_size, file_path, created_at
            FROM attachments
            WHERE message_id = ?
        ''', (message_id,))
        return [dict(row) for row in cursor.fetchall()]


def generate_conversation_title(first_message):
    """Generate a title from the first message (simple version)."""
    title = first_message[:50]
    if len(first_message) > 50:
        title += '...'
    return title

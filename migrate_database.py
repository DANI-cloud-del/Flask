#!/usr/bin/env python3
"""Database migration script to add attachments support.

Run this to update your existing database without losing data.
"""

import sqlite3
import os

DATABASE_FILE = 'database.db'

def migrate():
    """Add new columns and tables for attachments support."""
    
    if not os.path.exists(DATABASE_FILE):
        print("No database found. Run app.py to create a fresh database.")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if has_attachment column exists
        cursor.execute("PRAGMA table_info(messages)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'has_attachment' not in columns:
            print("Adding has_attachment column to messages table...")
            cursor.execute('''
                ALTER TABLE messages 
                ADD COLUMN has_attachment INTEGER DEFAULT 0
            ''')
            print("✓ Added has_attachment column")
        else:
            print("✓ has_attachment column already exists")
        
        # Create attachments table if it doesn't exist
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
        print("✓ Created/verified attachments table")
        
        # Create index
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_attachments_message_id 
            ON attachments(message_id)
        ''')
        print("✓ Created attachments index")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        print("You can now use file uploads and all new features.\n")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}\n")
    finally:
        conn.close()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Database Migration Script")
    print("="*60 + "\n")
    migrate()

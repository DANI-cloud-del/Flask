#!/usr/bin/env python3
"""View SQLite database contents with nice formatting.

Usage:
    python view_database.py
    python view_database.py --export
"""

import sqlite3
import sys
import json
from pathlib import Path

def view_database(db_path='database.db', export=False):
    """View and optionally export database contents."""
    
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        print(f"   Make sure you're in the Flask directory.")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("📊 FLASK AI CHAT - DATABASE OVERVIEW")
    print("="*70)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row['name'] for row in cursor.fetchall()]
    
    # Table counts
    print("\n📈 Table Statistics:")
    print("-" * 70)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"   {table.ljust(20)} {count:>5} records")
    
    # Detailed views
    print("\n" + "="*70)
    print("🔍 DETAILED DATA")
    print("="*70)
    
    # Users
    print("\n👥 USERS:")
    print("-" * 70)
    cursor.execute("SELECT id, email, name, created_at, last_login FROM users")
    users = cursor.fetchall()
    
    if users:
        for row in users:
            print(f"\n   ID: {row['id']}")
            print(f"   Name: {row['name']}")
            print(f"   Email: {row['email']}")
            print(f"   Created: {row['created_at']}")
            print(f"   Last Login: {row['last_login']}")
    else:
        print("   No users yet.")
    
    # Conversations with stats
    print("\n\n💬 CONVERSATIONS:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            c.id,
            c.title,
            c.created_at,
            c.updated_at,
            u.name as user_name,
            COUNT(m.id) as message_count
        FROM conversations c
        JOIN users u ON c.user_id = u.id
        LEFT JOIN messages m ON c.id = m.conversation_id
        GROUP BY c.id
        ORDER BY c.updated_at DESC
    """)
    conversations = cursor.fetchall()
    
    if conversations:
        for row in conversations:
            print(f"\n   [{row['id']}] {row['title']}")
            print(f"   User: {row['user_name']}")
            print(f"   Messages: {row['message_count']}")
            print(f"   Created: {row['created_at']}")
            print(f"   Updated: {row['updated_at']}")
    else:
        print("   No conversations yet.")
    
    # Recent messages
    print("\n\n📨 RECENT MESSAGES (Last 10):")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            m.id,
            m.role,
            m.content,
            m.created_at,
            c.title as conversation_title
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        ORDER BY m.created_at DESC
        LIMIT 10
    """)
    messages = cursor.fetchall()
    
    if messages:
        for row in messages:
            content_preview = row['content'][:80] + "..." if len(row['content']) > 80 else row['content']
            role_emoji = "👤" if row['role'] == 'user' else "🤖"
            print(f"\n   {role_emoji} [{row['role'].upper()}] {content_preview}")
            print(f"      Conversation: {row['conversation_title']}")
            print(f"      Time: {row['created_at']}")
    else:
        print("   No messages yet.")
    
    # Attachments
    print("\n\n📎 ATTACHMENTS:")
    print("-" * 70)
    cursor.execute("""
        SELECT 
            a.id,
            a.original_filename,
            a.file_type,
            a.file_size,
            a.created_at,
            m.conversation_id
        FROM attachments a
        JOIN messages m ON a.message_id = m.id
        ORDER BY a.created_at DESC
    """)
    attachments = cursor.fetchall()
    
    if attachments:
        for row in attachments:
            size_kb = row['file_size'] / 1024
            print(f"\n   📄 {row['original_filename']}")
            print(f"      Type: {row['file_type']}")
            print(f"      Size: {size_kb:.2f} KB")
            print(f"      Conversation: {row['conversation_id']}")
            print(f"      Uploaded: {row['created_at']}")
    else:
        print("   No attachments yet.")
    
    print("\n" + "="*70 + "\n")
    
    # Export if requested
    if export:
        print("📤 Exporting data to JSON...")
        export_data = {}
        
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            export_data[table] = [dict(row) for row in cursor.fetchall()]
        
        output_file = f"{db_path.replace('.db', '')}_export.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported to: {output_file}\n")
    
    conn.close()

if __name__ == '__main__':
    export_mode = '--export' in sys.argv or '-e' in sys.argv
    view_database(export=export_mode)

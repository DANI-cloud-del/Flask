# 🔍 How to View Your SQLite Database Contents

## Quick Methods (Choose One)

### Method 1: Command Line (Fastest) ⚡
### Method 2: GUI Tool (Most Visual) 🎨
### Method 3: Python Script (Programmable) 🐍
### Method 4: VS Code Extension (In Editor) 💻

---

## Method 1: Command Line (SQLite3) ⚡

### Install SQLite3 CLI:

```bash
# Check if already installed
sqlite3 --version

# If not installed:
sudo apt install sqlite3  # Ubuntu/Debian
# or
brew install sqlite3      # macOS
```

### Open Your Database:

```bash
cd ~/Desktop/Flask
sqlite3 database.db
```

### Essential Commands:

```sql
-- Show all tables
.tables
-- Output: attachments  conversations  messages  users

-- Show table structure
.schema users
-- Shows CREATE TABLE statement

-- View all users
SELECT * FROM users;

-- View with nice formatting
.mode column
.headers on
SELECT * FROM users;

-- Count records
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM conversations;
SELECT COUNT(*) FROM messages;

-- View recent conversations
SELECT id, title, created_at 
FROM conversations 
ORDER BY created_at DESC 
LIMIT 5;

-- View messages in a conversation
SELECT role, content, created_at 
FROM messages 
WHERE conversation_id = 1;

-- Export to CSV
.mode csv
.output users.csv
SELECT * FROM users;
.output stdout

-- Exit
.quit
```

### Quick View Script:

```bash
# Save as view_db.sh
#!/bin/bash
echo "=== Database Overview ==="
sqlite3 database.db <<EOF
.mode column
.headers on

SELECT 'Users:' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Conversations:', COUNT(*) FROM conversations
UNION ALL
SELECT 'Messages:', COUNT(*) FROM messages
UNION ALL
SELECT 'Attachments:', COUNT(*) FROM attachments;

EOF
```

Run it:
```bash
chmod +x view_db.sh
./view_db.sh
```

---

## Method 2: GUI Tool (DB Browser for SQLite) 🎨

### Install DB Browser:

```bash
# Ubuntu/Debian
sudo apt install sqlitebrowser

# macOS
brew install --cask db-browser-for-sqlite

# Or download from: https://sqlitebrowser.org
```

### Open Your Database:

```bash
cd ~/Desktop/Flask
sqlitebrowser database.db

# Or double-click database.db in file manager
```

### Features:

✅ **Browse Data** tab:
- See all tables
- Click any table to view rows
- Edit data directly
- Filter and search

✅ **Execute SQL** tab:
- Run custom queries
- Export results

✅ **Database Structure** tab:
- View table schemas
- See indexes
- View foreign keys

✅ **Export Data:**
- File → Export → Table to CSV
- File → Export → Database to SQL

### Screenshot:
```
┌─────────────────────────────────────────┐
│ DB Browser for SQLite                   │
├─────────────────────────────────────────┤
│ Tables:           Data View:            │
│ ├─ users          ┌──────────────────┐  │
│ ├─ conversations  │ id | email | ... │  │
│ ├─ messages       ├──────────────────┤  │
│ └─ attachments    │ 1  | dani@... |  │  │
│                   │ 2  | test@... |  │  │
│                   └──────────────────┘  │
└─────────────────────────────────────────┘
```

---

## Method 3: Python Script 🐍

### Quick View Script:

Create `view_database.py`:

```python
#!/usr/bin/env python3
"""View SQLite database contents."""

import sqlite3
from datetime import datetime

def view_database(db_path='database.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("DATABASE OVERVIEW")
    print("="*60)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row['name'] for row in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"\n📊 {table.upper()}: {count} records")
        
        # Show sample data
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        
        if rows:
            print("\n   Sample data:")
            for row in rows:
                print(f"   - {dict(row)}")
    
    print("\n" + "="*60)
    
    # Detailed views
    print("\n🔍 DETAILED VIEWS")
    print("="*60)
    
    # Users
    print("\n👥 USERS:")
    cursor.execute("SELECT id, email, name, created_at FROM users")
    for row in cursor.fetchall():
        print(f"   [{row['id']}] {row['name']} ({row['email']})")
        print(f"       Created: {row['created_at']}")
    
    # Conversations
    print("\n💬 CONVERSATIONS:")
    cursor.execute("""
        SELECT c.id, c.title, c.created_at, u.name as user_name,
               COUNT(m.id) as msg_count
        FROM conversations c
        JOIN users u ON c.user_id = u.id
        LEFT JOIN messages m ON c.id = m.conversation_id
        GROUP BY c.id
        ORDER BY c.created_at DESC
    """)
    for row in cursor.fetchall():
        print(f"   [{row['id']}] {row['title']}")
        print(f"       User: {row['user_name']}")
        print(f"       Messages: {row['msg_count']}")
        print(f"       Created: {row['created_at']}")
    
    # Recent Messages
    print("\n📨 RECENT MESSAGES (Last 5):")
    cursor.execute("""
        SELECT m.role, m.content, m.created_at, c.title
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        ORDER BY m.created_at DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        content_preview = row['content'][:50] + "..." if len(row['content']) > 50 else row['content']
        print(f"   [{row['role']}] {content_preview}")
        print(f"       Conversation: {row['title']}")
        print(f"       Time: {row['created_at']}")
    
    conn.close()

if __name__ == '__main__':
    view_database()
```

Run it:
```bash
cd ~/Desktop/Flask
python view_database.py
```

Output:
```
============================================================
DATABASE OVERVIEW
============================================================

📊 USERS: 1 records
   Sample data:
   - {'id': 1, 'google_id': '115867...', 'email': 'danicherianbiju@gmail.com', ...}

📊 CONVERSATIONS: 2 records
   Sample data:
   - {'id': 1, 'user_id': 1, 'title': 'Hello...', ...}

📊 MESSAGES: 5 records
   Sample data:
   - {'id': 1, 'conversation_id': 1, 'role': 'user', 'content': 'Hello', ...}

🔍 DETAILED VIEWS
============================================================

👥 USERS:
   [1] DANI (danicherianbiju@gmail.com)
       Created: 2026-03-04 00:45:00

💬 CONVERSATIONS:
   [1] Hello...
       User: DANI
       Messages: 3
       Created: 2026-03-04 00:46:00

📨 RECENT MESSAGES (Last 5):
   [assistant] I'm doing well, thank you! How can I help...
       Conversation: Hello...
       Time: 2026-03-04 00:46:15
```

---

## Method 4: VS Code Extension 💻

### Install Extension:

1. Open VS Code
2. Extensions (Ctrl+Shift+X)
3. Search: "SQLite Viewer" or "SQLite"
4. Install: **SQLite Viewer** by Florian Klampfer

### View Database:

1. Open your Flask folder in VS Code
2. Right-click `database.db`
3. Select **"Open with SQLite Viewer"**
4. Browse tables, run queries

### Features:
- ✅ View tables inline
- ✅ Run SQL queries
- ✅ Export results
- ✅ No need to leave editor

---

## Method 5: Online Viewer (No Install) 🌐

### SQLite Viewer Online:

1. Go to: https://sqliteviewer.app
2. Click **"Open File"**
3. Select `database.db`
4. Browse in browser (all processing client-side)

**Note:** Your data never leaves your computer!

---

## Useful SQL Queries for Your App 🔍

### Get User Info:
```sql
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(DISTINCT c.id) as conversation_count,
    COUNT(m.id) as message_count,
    u.created_at
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY u.id;
```

### Conversation with Messages:
```sql
SELECT 
    c.title,
    m.role,
    m.content,
    m.created_at
FROM conversations c
JOIN messages m ON c.id = m.conversation_id
WHERE c.id = 1
ORDER BY m.created_at;
```

### Find Malayalam Conversations:
```sql
SELECT 
    c.id,
    c.title,
    m.content
FROM conversations c
JOIN messages m ON c.id = m.conversation_id
WHERE m.content LIKE '%മലയാളം%'
   OR m.content LIKE '%കേരളം%';
```

### Database Statistics:
```sql
SELECT 
    'Total Users' as metric, 
    COUNT(*) as value 
FROM users
UNION ALL
SELECT 
    'Total Conversations', 
    COUNT(*) 
FROM conversations
UNION ALL
SELECT 
    'Total Messages', 
    COUNT(*) 
FROM messages
UNION ALL
SELECT 
    'Avg Messages per Conversation',
    CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM conversations)
FROM messages;
```

### Recent Activity:
```sql
SELECT 
    u.name,
    c.title,
    COUNT(m.id) as messages,
    MAX(m.created_at) as last_activity
FROM users u
JOIN conversations c ON u.id = c.user_id
JOIN messages m ON c.id = m.conversation_id
GROUP BY u.id, c.id
ORDER BY last_activity DESC
LIMIT 10;
```

---

## Export Your Data 📤

### Export to CSV:
```bash
sqlite3 database.db <<EOF
.mode csv
.headers on
.output users.csv
SELECT * FROM users;
.output conversations.csv
SELECT * FROM conversations;
.output messages.csv
SELECT * FROM messages;
.quit
EOF
```

### Export to JSON:
```python
import sqlite3
import json

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Export users
cursor.execute('SELECT * FROM users')
users = [dict(row) for row in cursor.fetchall()]

with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)

print("Exported to users.json")
```

### Backup Database:
```bash
# Simple copy
cp database.db database_backup_$(date +%Y%m%d).db

# Or SQL dump
sqlite3 database.db .dump > database_backup.sql

# Restore from dump
sqlite3 new_database.db < database_backup.sql
```

---

## Quick Reference Card 📋

```bash
# View all tables
sqlite3 database.db ".tables"

# Count records
sqlite3 database.db "SELECT COUNT(*) FROM users"

# View structure
sqlite3 database.db ".schema users"

# Interactive mode
sqlite3 database.db

# Run SQL file
sqlite3 database.db < queries.sql

# Export to CSV
sqlite3 database.db -csv -header "SELECT * FROM users" > users.csv

# Database info
sqlite3 database.db "PRAGMA table_info(users)"

# Database size
ls -lh database.db
```

---

## My Recommendation for You 🎯

**For quick checks:**
→ Use **Command Line** (Method 1)

**For browsing/exploring:**
→ Use **DB Browser** (Method 2)

**For automation/scripts:**
→ Use **Python** (Method 3)

**While coding:**
→ Use **VS Code Extension** (Method 4)

---

## Install Everything (One Command) 🚀

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y sqlite3 sqlitebrowser

# macOS
brew install sqlite3
brew install --cask db-browser-for-sqlite

# Verify
sqlite3 --version
sqlitebrowser --version
```

---

## Try It Now! ⚡

```bash
cd ~/Desktop/Flask

# Quick view
sqlite3 database.db "SELECT * FROM users"

# Or GUI
sqlitebrowser database.db &
```

**That's it!** Your database is now visible! 👀✨

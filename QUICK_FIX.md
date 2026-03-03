# ⚡ QUICK FIX - Get Everything Working

## The Problem
- Database schema changed (added file upload support)
- Old database doesn't have new columns
- Getting 500 errors

## The Solution (30 seconds)

### Step 1: Pull Latest Code
```bash
cd ~/Desktop/Flask
git pull origin main
```

### Step 2: Fix Database

**Option A: Keep Your Data (Migrate)**
```bash
python migrate_database.py
```

**Option B: Fresh Start (Recommended for Testing)**
```bash
rm database.db
```

### Step 3: Start Server
```bash
python app.py
```

You should see:
```
============================================================
Flask AI Workshop - Starting Server
============================================================
Debug mode: True
Port: 5001
Database: database.db
Upload folder: uploads
============================================================

Database initialized successfully!
 * Running on http://0.0.0.0:5001
```

### Step 4: Test

Visit `http://localhost:5001`

**Test Conversation Memory:**
1. Send: "My name is DANI"
2. Send: "What's my name?"
3. AI should remember! 🧠✅

---

## Still Having Issues?

### Check Server Logs

Look at your terminal where `python app.py` is running.

**Good signs:**
- ✅ `Database initialized successfully!`
- ✅ `Running on http://0.0.0.0:5001`

**Bad signs:**
- ❌ `sqlite3.OperationalError`
- ❌ `no such column`
- ❌ `500 Internal Server Error`

### If You See Errors:

```bash
# Stop server (Ctrl+C)
# Delete database
rm database.db

# Restart
python app.py
```

---

## What's Working Now:

- ✅ **Conversation Memory** - AI remembers your chat
- ✅ **Text-to-Speech** - Voice controls in settings
- ✅ **File Upload Backend** - Ready (UI coming soon)
- ✅ **Database** - Fixed with new schema
- ✅ **Chat Interface** - All working

---

## What's Next:

Once this works, I'll add:
- 📎 File upload UI in chat
- 🌙 Dark mode toggle
- ✨ All features fully integrated

**Test conversation memory first!** 🚀

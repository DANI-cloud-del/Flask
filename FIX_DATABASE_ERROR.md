# 🔧 Fix Database Error

## The Problem

You're seeing 500 errors because the database schema changed (added attachments support) but your old database doesn't have the new columns.

**Error:** `Failed to load conversation: 500 INTERNAL SERVER ERROR`

---

## Quick Fix (Choose One)

### Option 1: Migrate Existing Database (Keep Your Data) ✅

```bash
cd ~/Desktop/Flask
git pull origin main
python migrate_database.py
python app.py
```

This will:
- ✅ Keep all your existing conversations
- ✅ Add new columns for file attachments
- ✅ Update database schema

---

### Option 2: Fresh Start (Lose Data) 🔥

```bash
cd ~/Desktop/Flask
git pull origin main
rm database.db  # Delete old database
python app.py   # Creates fresh database
```

This will:
- ❌ Delete all conversations
- ✅ Fresh database with new schema
- ✅ No migration issues

---

## Recommended: Option 1 (Migrate)

Run this:
```bash
python migrate_database.py
```

You should see:
```
✓ Added has_attachment column
✓ Created/verified attachments table
✓ Created attachments index
✅ Database migration completed successfully!
```

Then restart:
```bash
python app.py
```

---

## Verify It Works

1. Visit `http://localhost:5001`
2. Old conversations should load without errors
3. You can create new conversations
4. Conversation memory works!

---

## Still Getting Errors?

Check server logs:
```bash
python app.py
```

Look for:
- Database errors
- SQL syntax errors
- Missing columns

If you see errors, use **Option 2** (fresh start).

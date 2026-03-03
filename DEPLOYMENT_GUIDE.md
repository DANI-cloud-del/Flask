# 🚀 Deployment Guide - Flask AI Chat

## 📋 Summary

**Recommended:** Deploy **ENTIRE APP on Render** (not split)

**Why?**
- ✅ Your Flask app serves BOTH frontend (templates) AND backend (API)
- ✅ Render has **better pricing** than Heroku (free tier available)
- ✅ Heroku is in **maintenance mode** as of Feb 2026[web:133]
- ✅ SQLite doesn't work on Heroku (ephemeral filesystem)[web:137]
- ✅ Render has persistent disks + PostgreSQL included[web:133]

---

## ⚠️ Important: Database Migration Required

### Problem with SQLite on Cloud:

**Heroku:** ❌ SQLite NOT supported (ephemeral filesystem)[web:137][web:140]
**Render:** 🟡 SQLite works BUT data lost on each deploy[web:133]

### Solution: Migrate to PostgreSQL ✅

**Good News:** Migration is straightforward! I'll show you how.

---

## 🎯 Deployment Strategy

### Option 1: Render (RECOMMENDED) 🌟

**Pros:**
- ✅ Free tier available (better than Heroku)
- ✅ PostgreSQL included
- ✅ Persistent disk storage
- ✅ 100-minute request timeout (vs Heroku's 30s)[web:136]
- ✅ Modern, actively maintained[web:142]
- ✅ Easy deployment from GitHub

**Pricing:**
- Free tier: $0/month (with limitations)
- Starter: $7/month (web service)
- PostgreSQL: Free 90 days, then $7/month

### Option 2: Railway

**Pros:**
- ✅ Very developer-friendly
- ✅ PostgreSQL included
- ✅ Good free tier ($5 credit/month)

### Option 3: Google App Engine[web:138]

**Pros:**
- ✅ Google Cloud infrastructure
- ✅ Good for scaling
- ✅ Free tier available

**Cons:**
- ❌ More complex setup
- ❌ Requires app.yaml configuration

---

## 📦 Step-by-Step: Deploy to Render

### Phase 1: Prepare Your App (LOCAL)

#### Step 1: Migrate SQLite → PostgreSQL

**Install PostgreSQL adapter:**
```bash
cd ~/Desktop/Flask
pip install psycopg2-binary
pip freeze > requirements.txt
```

#### Step 2: Update database.py

I'll create a version that works with BOTH SQLite (local) and PostgreSQL (production).

#### Step 3: Create deployment files

Create these files:
- `requirements.txt` (Python dependencies)
- `Procfile` (tells Render how to run app)
- `render.yaml` (optional, for infrastructure as code)
- `.env.example` (template for environment variables)

#### Step 4: Update config.py

Add PostgreSQL support with automatic detection.

---

### Phase 2: Deploy to Render

#### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repos

#### Step 2: Create PostgreSQL Database

1. Dashboard → New → PostgreSQL
2. Name: `flask-ai-chat-db`
3. Region: Choose closest to Kerala (Singapore)
4. Plan: Free (or Starter $7/month)
5. Click **Create Database**
6. **SAVE** the "Internal Database URL" (starts with `postgresql://`)

#### Step 3: Create Web Service

1. Dashboard → New → Web Service
2. Connect your GitHub repo: `DANI-cloud-del/Flask`
3. Settings:
   - **Name:** `flask-ai-chat`
   - **Region:** Singapore
   - **Branch:** `main`
   - **Root Directory:** `.` (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (or Starter $7/month)

#### Step 4: Add Environment Variables

In Render dashboard → Environment:

```bash
# Required
DATABASE_URL=<paste PostgreSQL Internal URL from Step 2>
SECRET_KEY=<generate random string>
GROQ_API_KEY=<your Groq API key>

# Google OAuth
GOOGLE_CLIENT_ID=<your client ID>
GOOGLE_CLIENT_SECRET=<your client secret>

# Flask Config
FLASK_ENV=production
DEBUG=False
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

#### Step 5: Update Google OAuth Redirect URIs

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services → Credentials
3. Click your OAuth 2.0 Client ID
4. Add to **Authorized redirect URIs:**
   ```
   https://flask-ai-chat.onrender.com/authorize
   ```
5. Save

#### Step 6: Deploy!

1. Click **Create Web Service**
2. Render will:
   - Clone your repo
   - Install dependencies
   - Run your app
3. Watch logs for errors
4. Visit: `https://flask-ai-chat.onrender.com`

---

## 🔧 Files Needed for Deployment

### 1. `requirements.txt`

```txt
Flask==3.0.0
Authlib==1.3.0
requests==2.31.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

### 2. `Procfile`

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 3. Updated `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Detect if running on cloud (Render/Heroku)
    IS_PRODUCTION = os.getenv('RENDER') or os.getenv('DYNO')
    
    # Database - use PostgreSQL in production, SQLite locally
    if IS_PRODUCTION:
        DATABASE_URL = os.getenv('DATABASE_URL')
        # Render uses postgres:// but psycopg2 needs postgresql://
        if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    else:
        DATABASE_URL = 'sqlite:///database.db'
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

config = Config()
```

### 4. Updated `database.py` (PostgreSQL Support)

```python
import os
from config import config

# Check if using PostgreSQL or SQLite
if config.DATABASE_URL.startswith('postgresql://'):
    # PostgreSQL
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    def get_db():
        conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    
    def init_db():
        conn = get_db()
        cursor = conn.cursor()
        
        # Create tables with PostgreSQL syntax
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
        
        # ... rest of tables ...
        
        conn.commit()
        cursor.close()
        conn.close()
else:
    # SQLite (existing code)
    import sqlite3
    # ... your existing SQLite code ...
```

### 5. `.gitignore`

```
__pycache__/
*.pyc
*.db
.env
uploads/
venv/
.DS_Store
```

---

## 🔄 Migration Script (SQLite → PostgreSQL)

Create `migrate_to_postgres.py`:

```python
"""
Migrate data from SQLite to PostgreSQL
Run ONCE after deploying to Render
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os

# Local SQLite
local_db = sqlite3.connect('database.db')
local_db.row_factory = sqlite3.Row

# Production PostgreSQL (from environment variable)
postgres_url = os.getenv('DATABASE_URL')
if postgres_url.startswith('postgres://'):
    postgres_url = postgres_url.replace('postgres://', 'postgresql://', 1)

pg_conn = psycopg2.connect(postgres_url)
pg_cursor = pg_conn.cursor()

print("Migrating users...")
users = local_db.execute('SELECT * FROM users').fetchall()
for user in users:
    pg_cursor.execute('''
        INSERT INTO users (google_id, email, name, picture, created_at, last_login)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (google_id) DO NOTHING
    ''', (user['google_id'], user['email'], user['name'], user['picture'], 
          user['created_at'], user['last_login']))

print(f"Migrated {len(users)} users")

# Migrate conversations, messages, etc.
# ...

pg_conn.commit()
pg_cursor.close()
pg_conn.close()
local_db.close()

print("Migration complete!")
```

---

## 🧪 Testing Deployment

### 1. Check Logs

Render Dashboard → Logs

Look for:
```
[DB] Database initialized successfully!
Flask AI Workshop - Starting Server
```

### 2. Test Endpoints

```bash
# Health check
curl https://flask-ai-chat.onrender.com/

# Should redirect to /chat or show login
```

### 3. Test Full Flow

1. Visit your Render URL
2. Login with Google
3. Send a test message
4. Enable Malayalam mode
5. Test TTS

---

## 🐛 Common Issues & Fixes

### Issue 1: "Application Error"

**Fix:** Check logs for errors
```bash
render logs --tail
```

### Issue 2: Google OAuth Fails

**Fix:** Add Render URL to authorized redirects:
```
https://your-app.onrender.com/authorize
```

### Issue 3: Database Connection Error

**Fix:** Verify `DATABASE_URL` environment variable

### Issue 4: Import Errors

**Fix:** Make sure `requirements.txt` has all dependencies:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue 5: File Uploads Not Working

**Fix:** Use Render's persistent disk:

In Render Dashboard:
1. Add Disk: `/opt/render/project/src/uploads`
2. Size: 1GB (free)

---

## 💰 Cost Breakdown

### Free Tier (Hobby Projects)

- **Render Web Service:** Free (spins down after 15min inactivity)
- **PostgreSQL:** Free for 90 days
- **Storage:** 1GB free

**Total:** $0/month (first 90 days)

### Paid Tier (Production)

- **Render Starter:** $7/month (always on)
- **PostgreSQL Starter:** $7/month (1GB, backups)
- **Storage:** 1GB included

**Total:** $14/month

Vs Heroku: $16-25/month[web:139]

---

## 🚀 Quick Deployment Checklist

### Before Deployment:

- [ ] Create `requirements.txt`
- [ ] Create `Procfile`
- [ ] Update `config.py` for PostgreSQL
- [ ] Update `database.py` for PostgreSQL
- [ ] Add `.gitignore`
- [ ] Push to GitHub

### On Render:

- [ ] Create PostgreSQL database
- [ ] Create web service
- [ ] Add environment variables
- [ ] Update Google OAuth redirect URIs
- [ ] Deploy!

### After Deployment:

- [ ] Test login
- [ ] Test chat
- [ ] Test Malayalam mode
- [ ] Test file upload (if enabled)
- [ ] Monitor logs for errors

---

## 🎓 Next Steps

Want me to:

1. ✅ Create the deployment files (Procfile, updated config, etc.)?
2. ✅ Create the PostgreSQL migration script?
3. ✅ Create a detailed step-by-step video guide?
4. ✅ Help you set up Render account?

Just say which one and I'll help! 🚀

---

## 📚 Resources

- [Render Docs](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [PostgreSQL with Python](https://www.psycopg.org/docs/)
- [Render vs Heroku Comparison](https://render.com/docs/render-vs-heroku-comparison)[web:133]

---

**Ready to deploy? Let's make your Malayalam AI chat live! 🌏✨**

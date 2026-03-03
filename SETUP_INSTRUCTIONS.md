# Setup Instructions - Flask AI Workshop

Step-by-step guide to get the application running on your machine.

## Prerequisites Check

Before starting, verify you have these installed:

```bash
# Check Python version (need 3.8+)
python --version
# or
python3 --version

# Check pip
pip --version
# or
pip3 --version
```

If you don't have Python, download from: https://www.python.org/downloads/

---

## Step 1: Get the Code

### Option A: Pull from GitHub (if you already cloned)

```bash
cd Flask
git pull origin main
```

### Option B: Clone Fresh

```bash
git clone https://github.com/DANI-cloud-del/Flask.git
cd Flask
```

---

## Step 2: Set Up Python Environment

### Create Virtual Environment

```bash
# Create venv
python -m venv venv
```

### Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Authlib (Google OAuth)
- Requests (API calls)
- python-dotenv (environment variables)

---

## Step 4: Set Up Environment Variables

### Create .env file

```bash
# Copy the example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it in your `.env` file as `SECRET_KEY`.

---

## Step 5: Get Google OAuth Credentials

### Go to Google Cloud Console

1. Visit: https://console.cloud.google.com
2. Sign in with your Google account

### Create a Project

1. Click "Select a project" at the top
2. Click "New Project"
3. Name: `Flask-AI-Workshop`
4. Click "Create"

### Enable APIs

1. Go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click "Enable"

### Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External"
3. Click "Create"
4. Fill in:
   - App name: `Flask AI Assistant`
   - User support email: your email
   - Developer contact: your email
5. Click "Save and Continue"
6. Skip "Scopes" (click "Save and Continue")
7. Add test users: your email
8. Click "Save and Continue"

### Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Application type: "Web application"
4. Name: `Flask AI Workshop`
5. Authorized redirect URIs:
   - Click "Add URI"
   - Enter: `http://localhost:5000/authorize`
6. Click "Create"

### Copy Credentials

1. A popup shows your Client ID and Client Secret
2. Copy **Client ID** → paste in `.env` as `GOOGLE_CLIENT_ID`
3. Copy **Client Secret** → paste in `.env` as `GOOGLE_CLIENT_SECRET`

---

## Step 6: Get Groq API Key

### Create Groq Account

1. Visit: https://console.groq.com
2. Sign up or log in

### Get API Key

1. Go to "API Keys" section
2. Click "Create API Key"
3. Copy the key immediately (you won't see it again!)
4. Paste in `.env` as `GROQ_API_KEY`

---

## Step 7: Verify Your .env File

Your `.env` should look like this:

```
SECRET_KEY=abc123...your-generated-key
GOOGLE_CLIENT_ID=1234567890-abc...googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123...
GROQ_API_KEY=gsk_abc123...
DEBUG=True
```

**Important**: Remove any quotes around the values!

---

## Step 8: Run the Application

```bash
python app.py
```

You should see:

```
Database initialized successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

---

## Step 9: Test the Application

1. Open browser: http://localhost:5000
2. You should see the landing page
3. Click "Sign in with Google"
4. Authorize the application
5. Start chatting!

---

## Common Issues

### Issue 1: "redirect_uri_mismatch"

**Cause**: OAuth redirect URI doesn't match

**Fix**:
1. Go to Google Cloud Console
2. Check your redirect URI is exactly: `http://localhost:5000/authorize`
3. No trailing slash!
4. Must include `http://` prefix

### Issue 2: "Missing required environment variables"

**Cause**: `.env` file not configured correctly

**Fix**:
1. Check `.env` file exists
2. Verify all keys are present
3. Remove any quotes around values
4. No extra spaces

### Issue 3: "ModuleNotFoundError"

**Cause**: Dependencies not installed or wrong Python environment

**Fix**:
```bash
# Ensure venv is activated (you should see (venv) in prompt)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 4: Port Already in Use

**Cause**: Another application using port 5000

**Fix**: Kill the process or use different port:
```bash
python app.py
# Then edit app.py and change port=5000 to port=5001
```

### Issue 5: "database is locked"

**Cause**: Multiple connections or crashed process

**Fix**:
```bash
# Delete database and restart
rm database.db  # Mac/Linux
del database.db  # Windows

# Then restart app
python app.py
```

---

## Quick Command Reference

```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Deactivate venv when done
deactivate
```

---

## Next Steps

Once everything works:

1. Explore the code in `app.py`
2. Check out `database.py` for database operations
3. Look at templates for frontend code
4. Try modifying the UI in `templates/chat.html`
5. Experiment with different AI prompts

---

## Getting Help

If you're stuck:

1. Read the error message carefully
2. Check this troubleshooting guide
3. Review the README.md
4. Ask during the workshop
5. Open an issue on GitHub

---

**You're all set! Enjoy the workshop! 🎉**
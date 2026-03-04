# 🚀 Flask Workshop - Quick Reference Cheat Sheet

> **Quick reference for you during the workshop - all the commands, code snippets, and steps you need!**

---

## 📋 Pre-Workshop Checklist

```bash
# Setup
□ Clone repository: git clone https://github.com/DANI-cloud-del/Flask.git
□ Test app works: python app.py
□ Create workshop folder: mkdir ~/Desktop/Flask-Workshop
□ Have docs open in browser
□ Have AI assistant ready
□ Have Google Cloud Console tab open
```

---

## 🎯 Quick Navigation

**Part 1:** [Flask Basics](#part-1-flask-basics) (30 min)
**Part 2:** [Templates & Frontend](#part-2-templates--frontend) (30 min)
**Part 3:** [Database](#part-3-database) (30 min)
**Part 4:** [Authentication](#part-4-authentication) (30 min)
**Part 5:** [AI Integration](#part-5-ai-integration) (20 min)
**Part 6:** [Demo & Q&A](#part-6-demo--qa) (20 min)

---

## Part 1: Flask Basics

### Minimal Flask App
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask Workshop!'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

### Multiple Routes
```python
@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'
```

### Commands
```bash
python app.py                    # Run Flask
Ctrl+C                          # Stop server
```

**Demo URLs:**
- http://localhost:5001/
- http://localhost:5001/about
- http://localhost:5001/user/DANI

---

## Part 2: Templates & Frontend

### Create Folders
```bash
mkdir templates static static/css static/js
```

### Use Templates
```python
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('index.html')
```

### Pass Data to Template
```python
@app.route('/')
def home():
    return render_template('index.html', 
                         name='DANI',
                         items=['Flask', 'Python', 'AI'])
```

### Template with Jinja2
```html
<h1>Welcome, {{ name }}!</h1>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

### Add Tailwind CSS (CDN)
```html
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <h1 class="text-4xl font-bold text-blue-600">Hello!</h1>
</body>
```

### Add Bootstrap (Alternative)
```html
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="text-primary">Hello!</h1>
    </div>
</body>
```

---

## Part 3: Database

### Install
```bash
# SQLite is built-in to Python - no installation needed!
```

### Create database.py
```python
import sqlite3

DATABASE_FILE = 'workshop.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize
import os
if not os.path.exists(DATABASE_FILE):
    init_db()
```

### CRUD Functions
```python
# CREATE
def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

# READ
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# READ ONE
def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
```

### Use in Flask
```python
from database import create_user, get_all_users

@app.route('/')
def home():
    users = get_all_users()
    return render_template('index.html', users=users)

@app.route('/user/new', methods=['POST'])
def new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    create_user(name, email)
    return redirect(url_for('home'))
```

---

## Part 4: Authentication

### Google OAuth Setup

**1. Go to Google Cloud Console:**
https://console.cloud.google.com

**2. Create Project:**
- Click "Select a project" → "New Project"
- Name: "Flask Workshop"
- Click "Create"

**3. Enable OAuth:**
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth 2.0 Client ID"
- Application type: "Web application"
- Name: "Flask Workshop OAuth"

**4. Add Redirect URI:**
```
Authorized redirect URIs:
http://localhost:5001/authorize
```

**5. Save Credentials:**
- Copy Client ID
- Copy Client Secret
- Save to `.env` file

### Install Packages
```bash
pip install authlib python-dotenv
```

### Create .env
```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### Create config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

config = Config()
```

### Setup OAuth in app.py
```python
from flask import Flask, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Setup OAuth
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

### OAuth Routes
```python
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    session['user'] = {
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture')
    }
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
```

### Protected Route Decorator
```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Use it:
@app.route('/dashboard')
@login_required
def dashboard():
    user = session.get('user')
    return render_template('dashboard.html', user=user)
```

---

## Part 5: AI Integration

### Get Groq API Key
https://console.groq.com

### Add to .env
```env
GROQ_API_KEY=your-groq-api-key
```

### Update config.py
```python
class Config:
    # ... existing config ...
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
```

### Chat API Endpoint
```python
import requests
from flask import jsonify

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {config.GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': user_message}
                ],
                'temperature': 0.7,
                'max_tokens': 1024
            },
            timeout=30
        )
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### JavaScript for Chat
```javascript
async function sendMessage() {
    const message = messageInput.value;
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    });
    
    const data = await response.json();
    displayMessage(data.response);
}
```

---

## Part 6: Demo & Q&A

### Complete Demo Flow

1. **Landing Page**
   - Visit http://localhost:5001/
   - Show login button

2. **OAuth Login**
   - Click "Sign in with Google"
   - Complete authentication
   - Show session in DevTools

3. **Dashboard**
   - Show protected route
   - Display user info

4. **Database**
   - Create new user
   - View all users
   - Show data persists

5. **AI Chat**
   - Send message
   - Show AI response
   - Explain API call

### Common Issues & Fixes

**Issue: ModuleNotFoundError**
```bash
pip install flask authlib requests python-dotenv
```

**Issue: OAuth Error**
- Check redirect URI matches exactly
- Check Client ID and Secret
- Clear browser cookies

**Issue: Database Error**
```bash
rm workshop.db  # Delete and recreate
python database.py
```

**Issue: Port Already in Use**
```python
app.run(debug=True, port=5002)  # Use different port
```

---

## 📚 Documentation Links

**Your Documentation:**
- [Workshop Guide](WORKSHOP_GUIDE.md) - This file!
- [Flask Architecture](FLASK_ARCHITECTURE.md) - How Flask works
- [Authentication Guide](../AUTHENTICATION_EXPLAINED.md) - OAuth details
- [OAuth Flowcharts](OAUTH_FLOWCHART.md) - Visual diagrams

**Official Docs:**
- Flask: https://flask.palletsprojects.com/
- Jinja2: https://jinja.palletsprojects.com/
- Tailwind: https://tailwindcss.com/
- Bootstrap: https://getbootstrap.com/

---

## 🎯 Quick Commands

```bash
# Run Flask
python app.py

# Install packages
pip install flask authlib requests python-dotenv

# Create folders
mkdir templates static

# Initialize database
python database.py

# Git commands (if using)
git add .
git commit -m "Workshop progress"
git push
```

---

## 💡 Pro Tips

**During Workshop:**
- Keep this cheat sheet open
- Have documentation tabs ready
- Use AI assistant for quick help
- Don't worry if you forget syntax - reference this!
- Encourage students to ask questions
- Take breaks every 30 minutes

**If You Get Stuck:**
1. Check this cheat sheet
2. Reference [Flask Architecture docs](FLASK_ARCHITECTURE.md)
3. Ask AI assistant
4. Show students debugging process (it's educational!)
5. Use existing Flask app as reference

**Time Management:**
- ⏰ Part 1: 30 min (Flask basics)
- ⏰ Part 2: 30 min (Templates/Frontend)
- ⏰ Part 3: 30 min (Database)
- ⏰ Part 4: 30 min (Authentication)
- ⏰ Part 5: 20 min (AI Integration)
- ⏰ Part 6: 20 min (Demo & Q&A)
- **Total: 2h 40min + buffer = ~3 hours**

---

## 🚨 Emergency Shortcuts

**If Running Out of Time:**

**Skip to working demo:**
```bash
cd ~/Desktop/Flask
git pull origin main
python app.py
# Show the complete working app instead
```

**Skip authentication:**
- Remove OAuth, use simple session
- Focus on core Flask concepts

**Skip AI integration:**
- Show the code
- Explain the concept
- Demo the complete app

**Most Important Parts:**
1. Flask routes (must cover)
2. Templates (must cover)
3. Database basics (must cover)
4. Authentication (can show complete code)
5. AI (can demo instead of build)

---

## ✅ Success Checklist

**By End of Workshop:**

□ Students understand routes
□ Students can use render_template
□ Students know basic database operations
□ Students understand authentication concept
□ Students have working app to reference
□ Students know where to find documentation
□ Students feel confident to build more

---

**You've got this! 🚀**

Remember: It's okay if things don't go perfectly. Show students that debugging and referencing documentation is part of development!

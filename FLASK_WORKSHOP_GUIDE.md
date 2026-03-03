# Flask Workshop - Professional Guide
## AI-Powered Web Application Development

---

## Table of Contents

1. [Introduction to Flask](#introduction-to-flask)
2. [Why Flask?](#why-flask)
3. [Installation & Setup](#installation--setup)
4. [Framework Comparison](#framework-comparison)
5. [Workshop Project](#workshop-project)
6. [Key Concepts](#key-concepts)
7. [Best Practices](#best-practices)
8. [Resources & Next Steps](#resources--next-steps)

---

## Introduction to Flask

### What is Flask?

Flask is a lightweight Python web framework designed for rapid development and clean, pragmatic design. Created by Armin Ronacher in 2010, Flask follows the WSGI (Web Server Gateway Interface) standard and is built on Werkzeug and Jinja2.

**Core Characteristics:**
- Micro-framework (minimal core, extensible via plugins)
- Built-in development server and debugger
- RESTful request dispatching
- Jinja2 templating engine
- Unit testing support
- WSGI compliant

### Industry Adoption

**Production Deployments:**
- Netflix (microservices architecture)
- Reddit (initial platform, still in use)
- LinkedIn (data engineering pipelines)
- Airbnb (internal tools)
- MIT/Stanford (academic platforms)

**Market Statistics (2026):**
- 35% of Python web development jobs require Flask
- 87,000+ GitHub stars
- 200,000+ StackOverflow questions
- Active development and maintenance

---

## Why Flask?

### 1. Rapid Prototyping

**Development Speed:**
- Minimal boilerplate code
- 5 lines for basic HTTP server
- 30-minute MVP development cycle
- Ideal for hackathons and proof-of-concepts

**Example: Basic Application**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return {'message': 'API running'}

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. Simplicity and Clarity

**Explicit Code:**
- No hidden abstractions
- Clear request-response flow
- Easy debugging and testing
- Minimal learning curve

**Transparent Architecture:**
Every component is visible and modifiable. No "magic" decorators or auto-configuration that obscures functionality.

### 3. Flexibility

**Database Agnostic:**
- SQLAlchemy (ORM)
- Raw SQL (SQLite, PostgreSQL, MySQL)
- NoSQL (MongoDB, Redis)
- Cloud databases (DynamoDB, Firestore)

**Frontend Freedom:**
- Server-side rendering (Jinja2)
- API-only (React, Vue, Angular)
- Hybrid approaches
- Mobile app backends

**Authentication Options:**
- OAuth 2.0 (Google, GitHub, etc.)
- JWT tokens
- Session-based auth
- Third-party services (Auth0, Clerk)

### 4. Extensibility

**Popular Extensions:**
- Flask-SQLAlchemy (database ORM)
- Flask-Login (user session management)
- Flask-CORS (cross-origin resource sharing)
- Flask-RESTful (REST API development)
- Flask-SocketIO (WebSockets)
- Flask-JWT-Extended (token authentication)

### 5. Microservices Architecture

**Advantages:**
- Small footprint (~30KB core)
- Fast startup time
- Easy horizontal scaling
- Service isolation
- Independent deployment

---

## Installation & Setup

### Prerequisites

**Required:**
- Python 3.8 or higher
- pip (Python package manager)
- Text editor or IDE

**Recommended:**
- VS Code with Python extension
- Git for version control
- Virtual environment management

### Installation Steps

**1. Create Project Directory**
```bash
mkdir flask-ai-workshop
cd flask-ai-workshop
```

**2. Create Virtual Environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install flask authlib requests python-dotenv
```

**4. Verify Installation**
```bash
python -c "import flask; print(flask.__version__)"
```

### Project Structure

```
flask-ai-workshop/
├── app.py                 # Main application
├── database.db            # SQLite database
├── .env                   # Environment variables
├── .gitignore            # Git exclusions
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html
│   ├── login.html
│   └── chat.html
└── static/
    ├── css/
    └── js/
```

---

## Framework Comparison

### Flask vs Django vs FastAPI

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|----------|
| **Type** | Micro-framework | Full-stack framework | API framework |
| **Size** | ~30KB | ~1.5MB | ~50KB |
| **Learning Curve** | Low | High | Medium |
| **Setup Time** | 5 minutes | 30+ minutes | 10 minutes |
| **Performance** | 2,000 req/sec | 1,500 req/sec | 20,000 req/sec |
| **Async Support** | Via extensions | Limited | Native |
| **Admin Panel** | No (extensions available) | Built-in | No |
| **ORM** | Optional (SQLAlchemy) | Built-in (Django ORM) | Optional |
| **Best For** | APIs, MVPs, Learning | Full web apps, CMS | High-performance APIs |

### When to Choose Flask

**Use Flask for:**
- Rapid prototyping and MVPs
- RESTful APIs
- Microservices architecture
- Learning web development fundamentals
- Small to medium applications
- Projects requiring custom architecture
- Hackathons and time-constrained development

**Consider Alternatives for:**
- Large monolithic applications (Django)
- Pre-built admin requirements (Django)
- High-concurrency APIs (FastAPI)
- Real-time applications with WebSockets (FastAPI)

---

## Workshop Project

### Project Overview

**Application:** AI-Powered Chat Assistant with Authentication

**Core Features:**
1. OAuth 2.0 authentication (Google)
2. AI integration (Groq API / Ollama)
3. SQLite database for user management
4. Modern responsive UI (Tailwind CSS)
5. RESTful API architecture

### Technology Stack

**Backend:**
- Flask 3.0+ (web framework)
- SQLite (database)
- Authlib (OAuth implementation)
- Requests (HTTP client)

**Frontend:**
- HTML5
- Tailwind CSS 3.0+ (utility-first CSS)
- Vanilla JavaScript (fetch API)

**External APIs:**
- Google OAuth 2.0
- Groq API (cloud LLM)
- Ollama API (local LLM - optional)

### Learning Objectives

**Backend Development:**
- Flask routing and request handling
- OAuth 2.0 authentication flow
- Database design and SQL operations
- API integration patterns
- Error handling and logging
- Environment variable management

**Frontend Development:**
- Modern CSS frameworks (Tailwind)
- JavaScript fetch API
- DOM manipulation
- Responsive design principles

**Security:**
- Secure credential storage
- Session management
- CORS configuration
- Input validation
- HTTPS requirements

### Workshop Timeline (2 Hours)

**Phase 1: Setup (10 minutes)**
- Environment verification
- Dependency installation
- Project structure overview

**Phase 2: Authentication (30 minutes)**
- Google OAuth setup
- Login/logout implementation
- User session management
- Database integration

**Phase 3: AI Integration (20 minutes)**
- Groq API configuration
- Chat endpoint implementation
- Request/response handling
- Error management

**Phase 4: Frontend (40 minutes)**
- UI development with Tailwind
- JavaScript API integration
- Real-time chat interface
- Styling and UX polish

**Phase 5: Advanced Topics (20 minutes)**
- Local LLM demo (Ollama)
- Deployment considerations
- Extension possibilities
- Q&A

---

## Key Concepts

### 1. Routing

**Definition:** Mapping URLs to Python functions

**Basic Route:**
```python
@app.route('/')
def home():
    return 'Home Page'
```

**Dynamic Routes:**
```python
@app.route('/user/<username>')
def user_profile(username):
    return f'Profile: {username}'
```

**HTTP Methods:**
```python
@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        return process_data(request.json)
    return get_data()
```

### 2. Templates

**Jinja2 Syntax:**
```html
<!-- Variable output -->
<h1>Welcome, {{ user.name }}</h1>

<!-- Conditional rendering -->
{% if user.authenticated %}
    <p>Logged in</p>
{% endif %}

<!-- Loops -->
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
```

**Rendering Templates:**
```python
from flask import render_template

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                         user=current_user,
                         data=get_data())
```

### 3. Request Handling

**Accessing Request Data:**
```python
from flask import request

@app.route('/submit', methods=['POST'])
def submit():
    # JSON data
    data = request.json
    
    # Form data
    username = request.form.get('username')
    
    # Query parameters
    page = request.args.get('page', 1)
    
    # Headers
    auth_token = request.headers.get('Authorization')
    
    return {'status': 'success'}
```

### 4. Response Handling

**JSON Responses:**
```python
from flask import jsonify

@app.route('/api/users')
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
```

**Status Codes:**
```python
from flask import make_response

@app.route('/create', methods=['POST'])
def create():
    result = create_resource(request.json)
    return jsonify(result), 201  # Created

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

### 5. Database Integration

**SQLite with Raw SQL:**
```python
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user
```

### 6. OAuth 2.0 Authentication

**Setup:**
```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

**Login Flow:**
```python
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info
    return redirect('/dashboard')
```

### 7. API Integration

**Groq API Example:**
```python
import requests

def chat_with_ai(message):
    response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'llama-3.1-70b-versatile',
            'messages': [{'role': 'user', 'content': message}]
        }
    )
    return response.json()['choices'][0]['message']['content']
```

**Ollama (Local) Example:**
```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  # Required but not used
)

def chat_with_local_ai(message):
    response = client.chat.completions.create(
        model='llama3.2',
        messages=[{'role': 'user', 'content': message}]
    )
    return response.choices[0].message.content
```

---

## Best Practices

### 1. Project Structure

**Recommended Organization:**
```
project/
├── app/
│   ├── __init__.py       # Application factory
│   ├── routes/           # Route blueprints
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── utils/            # Helper functions
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

### 2. Configuration Management

**Environment Variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**.env File:**
```
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GROQ_API_KEY=your-groq-key
```

**Never commit .env to version control!**

### 3. Error Handling

**Global Error Handlers:**
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled exception: {e}')
    return jsonify({'error': 'An error occurred'}), 500
```

### 4. Security

**Essential Security Measures:**

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# HTTPS redirect in production
if not app.debug:
    @app.before_request
    def before_request():
        if not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'))
```

**Input Validation:**
```python
from flask import request, abort

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    
    # Validate required fields
    if not data or 'email' not in data:
        abort(400, 'Email is required')
    
    # Validate email format
    if not is_valid_email(data['email']):
        abort(400, 'Invalid email format')
    
    # Sanitize inputs
    email = data['email'].strip().lower()
    
    return create_user_record(email)
```

### 5. Database Connection Management

**Using Context Managers:**
```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with get_db() as db:
    users = db.execute('SELECT * FROM users').fetchall()
```

### 6. Logging

**Configure Logging:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
```

### 7. Testing

**Unit Tests:**
```python
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_endpoint(self):
        response = self.app.post('/api/chat',
                                json={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)
```

---

## Local LLM Integration (Ollama)

### Why Local LLMs?

**Advantages:**
- Data privacy (no external API calls)
- No API costs for high-volume usage
- Offline functionality
- Custom model fine-tuning
- No rate limits

**Use Cases:**
- Healthcare applications (HIPAA compliance)
- Legal documents (confidentiality)
- Internal enterprise tools
- Development and experimentation
- Air-gapped environments

### Ollama Setup

**Installation:**
```bash
# Download from ollama.com
# Or via command line (Linux/Mac):
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model (3-7GB download)
ollama pull llama3.2

# Verify installation
ollama run llama3.2 "Hello, who are you?"
```

**Flask Integration:**
```python
from openai import OpenAI

# Initialize Ollama client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  # Not used but required
)

@app.route('/api/chat/local', methods=['POST'])
def chat_local():
    message = request.json.get('message')
    
    try:
        response = client.chat.completions.create(
            model='llama3.2',
            messages=[{'role': 'user', 'content': message}]
        )
        return jsonify({
            'response': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Cloud vs Local Comparison

| Aspect | Cloud API (Groq) | Local (Ollama) |
|--------|------------------|----------------|
| **Setup Time** | 5 minutes | 30-60 minutes |
| **Cost** | Pay per token | Free (hardware cost) |
| **Latency** | 200-500ms | 100-300ms |
| **Privacy** | Data leaves network | Fully private |
| **Model Access** | Latest models | Open-source only |
| **Scaling** | Automatic | Manual hardware |
| **Maintenance** | Provider managed | Self-managed |
| **Best For** | Prototypes, MVPs | Production, privacy |

---

## Deployment Considerations

### Production Servers

**Don't use Flask's development server in production!**

**Recommended Production Setup:**
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With configuration
gunicorn -c gunicorn_config.py app:app
```

**gunicorn_config.py:**
```python
bind = '0.0.0.0:8000'
workers = 4
worker_class = 'sync'
accesslog = 'access.log'
errorlog = 'error.log'
loglevel = 'info'
```

### Platform Options

**Quick Deploy (Free Tier):**
- **Render**: Auto-deploy from GitHub
- **Railway**: Zero-config deployment
- **PythonAnywhere**: Flask-optimized hosting
- **Fly.io**: Global edge deployment

**Scalable Options:**
- **AWS Elastic Beanstalk**: Managed Flask hosting
- **Google Cloud Run**: Serverless containers
- **Azure App Service**: Integrated CI/CD
- **DigitalOcean App Platform**: Simple scaling

**Container Deployment:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

---

## Extension Ideas

### Beginner Extensions
1. **Chat History**: Store conversations in database
2. **User Profiles**: Add profile pages with avatars
3. **Dark Mode**: Toggle theme preference
4. **Export Chat**: Download conversations as PDF/TXT

### Intermediate Extensions
1. **Multiple AI Models**: Switch between different LLMs
2. **Voice Input**: Speech-to-text integration
3. **File Uploads**: Chat with documents (RAG)
4. **Real-time Updates**: WebSocket integration

### Advanced Extensions
1. **Vector Database**: Implement semantic search with embeddings
2. **Fine-tuning**: Custom model training interface
3. **Multi-user Chat**: Collaborative chat rooms
4. **Analytics Dashboard**: Usage metrics and visualizations
5. **API Rate Limiting**: Request throttling and quotas

---

## Resources & Next Steps

### Official Documentation
- Flask: https://flask.palletsprojects.com/
- SQLite: https://www.sqlite.org/docs.html
- Tailwind CSS: https://tailwindcss.com/docs
- Groq API: https://console.groq.com/docs
- Ollama: https://ollama.com/library

### Learning Resources
- Flask Mega-Tutorial (Miguel Grinberg)
- Real Python Flask Tutorials
- Flask Web Development (O'Reilly)
- CS50 Web Programming with Python

### Community
- r/flask (Reddit)
- Flask Discord Server
- Stack Overflow (flask tag)
- GitHub Discussions

### Next Steps After Workshop

**Week 1-2: Consolidate Basics**
- Build 3-4 small Flask apps
- Practice database operations
- Experiment with different APIs

**Week 3-4: Intermediate Concepts**
- Learn Flask Blueprints (modular apps)
- Implement JWT authentication
- Add automated testing
- Deploy to cloud platform

**Month 2: Advanced Topics**
- Build RESTful API with full CRUD
- Implement WebSockets
- Add caching (Redis)
- Learn Docker containerization

**Month 3: Production Ready**
- CI/CD pipeline setup
- Monitoring and logging
- Performance optimization
- Security hardening

---

## Quick Reference

### Essential Commands

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Installation
pip install flask
pip freeze > requirements.txt
pip install -r requirements.txt

# Running Flask
flask run
flask run --debug
flask run --host=0.0.0.0 --port=5000

# Environment variables
export FLASK_APP=app.py  # Mac/Linux
set FLASK_APP=app.py     # Windows
```

### Common Patterns

```python
# JSON API
@app.route('/api/data')
def get_data():
    return jsonify({'key': 'value'})

# POST handler
@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    return jsonify({'status': 'success'}), 201

# Error handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

# Template rendering
@app.route('/page')
def page():
    return render_template('page.html', data=data)
```

---

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or use different port
flask run --port=5001
```

**Module Not Found:**
```bash
# Ensure virtual environment is activated
which python  # Should show venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

**Template Not Found:**
```python
# Check folder structure
# templates/ must be in same directory as app.py
# Use render_template('filename.html'), not full path
```

**Database Locked:**
```python
# Ensure connections are closed
with get_db() as db:
    # Operations here
# Connection auto-closed after with block
```

---

**END OF PROFESSIONAL GUIDE**

*This document provides technical reference for Flask web development with focus on practical implementation and best practices.*
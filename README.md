# 🤖 Flask AI Chat Application

> A full-stack AI-powered chat application with Google OAuth authentication, conversation memory, file uploads, and Malayalam language support.

## 📚 Documentation

### Core Documentation

- **[Authentication Guide](AUTHENTICATION_EXPLAINED.md)** - Complete OAuth flow, session management, and security
- **[OAuth Flowcharts](docs/OAUTH_FLOWCHART.md)** - Visual diagrams of authentication system
- **[Flask Architecture Guide](docs/FLASK_ARCHITECTURE.md)** - How Flask works, templates, request-response cycle

### Quick Links

| Topic | Documentation |
|-------|---------------|
| 🔐 **Authentication** | [OAuth & Sessions](AUTHENTICATION_EXPLAINED.md) |
| 📊 **Visual Flowcharts** | [Complete Diagrams](docs/OAUTH_FLOWCHART.md) |
| 🏗️ **Flask Architecture** | [How Flask Works](docs/FLASK_ARCHITECTURE.md) |
| 🎨 **Templates & Rendering** | [Flask Architecture - Templates Section](docs/FLASK_ARCHITECTURE.md#-templates--jinja2) |
| 💾 **Database** | [Flask Architecture - Database Section](docs/FLASK_ARCHITECTURE.md#-database-integration) |

---

## ✨ Features

- ✅ **Google OAuth Authentication** - Secure login with Google
- ✅ **AI Chat Integration** - Powered by Groq API (Llama 3.3 70B)
- ✅ **Conversation Memory** - Full conversation history
- ✅ **File Upload Support** - Upload and process files
- ✅ **Malayalam Language Mode** - Communicate in Malayalam
- ✅ **Text-to-Speech** - Voice output for responses
- ✅ **Dark Mode** - Modern UI with Tailwind CSS
- ✅ **Session Management** - Secure session handling
- ✅ **RESTful API** - Clean API design

---

## 🏗️ Project Structure

```
Flask/
├── app.py                    # Main application (routes, auth, logic)
├── config.py                 # Configuration management
├── database.py               # Database operations (SQLite)
├── .env                      # Environment variables (secrets)
│
├── templates/                # Jinja2 HTML templates
│   ├── index.html           # Landing page
│   ├── chat.html            # Chat interface
│   ├── settings.html        # Settings page
│   └── 404.html             # Error page
│
├── static/                   # Static assets (CSS, JS, images)
├── uploads/                  # User uploaded files
├── docs/                     # Documentation
│   ├── OAUTH_FLOWCHART.md   # Authentication flowcharts
│   └── FLASK_ARCHITECTURE.md # Flask architecture guide
│
└── flask_chat.db            # SQLite database
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Cloud Console account (for OAuth)
- Groq API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/DANI-cloud-del/Flask.git
cd Flask
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Run the application:**
```bash
python app.py
```

5. **Open browser:**
```
http://localhost:5001
```

---

## 🔧 Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable OAuth 2.0
4. Add authorized redirect URIs:
   - `http://localhost:5001/authorize` (development)
   - `https://your-domain.com/authorize` (production)
5. Copy Client ID and Client Secret to `.env`

**[→ Detailed OAuth Setup Guide](AUTHENTICATION_EXPLAINED.md#-step-1-google-cloud-console-setup)**

### Environment Variables

```env
# Flask
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Groq API
GROQ_API_KEY=your-groq-api-key
```

---

## 📖 How It Works

### Authentication Flow

```
User → Click Login → Google OAuth → Verify → Create Session → Access Chat
```

**[→ See Complete Authentication Flow](docs/OAUTH_FLOWCHART.md#-complete-authentication-flow-high-level)**

### Request-Response Cycle

```
Browser → Flask Routes → Authentication Check → Database Query → AI API → Template Rendering → Response
```

**[→ See Flask Architecture Guide](docs/FLASK_ARCHITECTURE.md#-request-response-cycle)**

### Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Authentication:** Google OAuth 2.0 (Authlib)
- **AI:** Groq API (Llama 3.3 70B)
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Template Engine:** Jinja2

---

## 🎯 Key Features Explained

### 1. Google OAuth Authentication

Secure authentication using Google accounts. No password storage!

**[→ Complete Authentication Guide](AUTHENTICATION_EXPLAINED.md)**

### 2. Conversation Memory

Each chat maintains full conversation history for context-aware responses.

```python
# Get conversation history
history = get_conversation_messages(conversation_id, user_id)

# Send to AI with context
messages = [{'role': 'system', 'content': system_message}]
for msg in history[-10:]:  # Last 10 messages
    messages.append({'role': msg['role'], 'content': msg['content']})
```

### 3. File Upload & Processing

Upload files (images, PDFs, text) and discuss them with AI.

```python
# File upload handling
if 'file' in request.files:
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    file_context = process_file_for_ai(file_path, file_type)
```

### 4. Malayalam Language Mode

Automatic translation for Malayalam communication.

```python
if malayalam_mode:
    user_message = translate_text(user_message, 'ml')
    system_message += ' You MUST respond ONLY in Malayalam.'
```

---

## 🔐 Security Features

- ✅ **OAuth 2.0** - No password storage
- ✅ **Session Encryption** - Encrypted cookies with SECRET_KEY
- ✅ **HttpOnly Cookies** - JavaScript cannot access session
- ✅ **Route Protection** - `@login_required` decorator
- ✅ **CSRF Protection** - Built-in Flask security
- ✅ **Input Validation** - Sanitized user inputs

**[→ Security Details](AUTHENTICATION_EXPLAINED.md#-security-features-included)**

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    name TEXT,
    picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    has_attachment BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

---

## 🛠️ API Endpoints

### Authentication
- `GET /` - Landing page
- `GET /login` - Start OAuth flow
- `GET /authorize` - OAuth callback
- `GET /logout` - End session

### Chat Interface
- `GET /chat` - Chat page (protected)
- `GET /chat/<id>` - Specific conversation (protected)
- `GET /settings` - Settings page (protected)

### API Routes
- `POST /api/chat` - Send message to AI (protected)
- `POST /api/translate` - Translate text (protected)
- `GET /api/conversations` - List conversations (protected)
- `GET /api/conversations/<id>` - Get conversation (protected)
- `DELETE /api/conversations/<id>` - Delete conversation (protected)
- `PUT /api/conversations/<id>/title` - Update title (protected)

**[→ See Complete API Flow](docs/FLASK_ARCHITECTURE.md#-complete-application-flow)**

---

## 🎨 Frontend Structure

### Templates (Jinja2)

```html
<!-- Base template with inheritance -->
{% extends "base.html" %}

{% block title %}Chat{% endblock %}

{% block content %}
    <h1>Welcome, {{ user.name }}!</h1>
    
    {% for conversation in conversations %}
        <div>{{ conversation.title }}</div>
    {% endfor %}
{% endblock %}
```

**[→ Template Guide](docs/FLASK_ARCHITECTURE.md#-templates--jinja2)**

### JavaScript Integration

```javascript
// Send message to backend
fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: userMessage, conversation_id: convId})
})
.then(response => response.json())
.then(data => displayMessage(data.response));
```

---

## 🧪 Testing

### Manual Testing Guide

1. **Authentication:**
   - Open incognito window
   - Try accessing `/chat` directly (should redirect)
   - Click "Sign in with Google"
   - Complete OAuth flow
   - Verify access to `/chat`

2. **Chat Functionality:**
   - Send a message
   - Check AI response
   - Upload a file
   - Toggle Malayalam mode
   - Create new conversation

3. **Session Persistence:**
   - Close and reopen browser
   - Verify still logged in
   - Click logout
   - Verify redirected to home

**[→ Complete Testing Flow](docs/OAUTH_FLOWCHART.md#-testing-authentication-flow)**

---

## 📝 Development Notes

### Adding New Routes

```python
@app.route('/new-page')
@login_required  # Protect if needed
def new_page():
    user = session.get('user')
    # Your logic here
    return render_template('new-page.html', user=user)
```

### Database Operations

```python
# Always use database.py functions
from database import get_user_by_google_id, create_user

# Don't write SQL directly in app.py
user = get_user_by_google_id(google_id)  # ✅ Good
# cursor.execute('SELECT ...')            # ❌ Bad
```

### Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use production-grade WSGI server (Gunicorn)
- [ ] Set strong `SECRET_KEY`
- [ ] Add production domain to Google OAuth redirect URIs
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring

### Example Deployment (Render)

```bash
# Procfile
web: gunicorn app:app

# requirements.txt
Flask==3.0.0
gunicorn==21.2.0
# ... other dependencies
```

---

## 🤝 Contributing

Contributions welcome! Please read the documentation first:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project for learning and development!

---

## 🎓 Learning Resources

- **[Flask Documentation](https://flask.palletsprojects.com/)**
- **[Jinja2 Template Guide](https://jinja.palletsprojects.com/)**
- **[OAuth 2.0 Explained](https://oauth.net/2/)**
- **[SQLite Tutorial](https://www.sqlitetutorial.net/)**

---

## 📞 Support

For questions or issues:

1. Check the documentation guides
2. Review the flowcharts
3. Open an issue on GitHub

---

**Built with ❤️ using Flask, Python, and AI**

**Documentation:** Complete guides with visual flowcharts available in `/docs`

🔗 **[Authentication Guide](AUTHENTICATION_EXPLAINED.md)** | **[Flowcharts](docs/OAUTH_FLOWCHART.md)** | **[Flask Architecture](docs/FLASK_ARCHITECTURE.md)**

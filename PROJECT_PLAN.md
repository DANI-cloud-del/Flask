# Flask AI Workshop - Professional Development Plan

## Project Overview

**Project Name:** AI Chat Assistant with Google OAuth

**Timeline:** 2-hour workshop + 2-hour prep tonight

**Goal:** Build a production-ready MVP that teaches core web development concepts

---

## Phase 1: Planning & Architecture (COMPLETED)

### Requirements Analysis ✅

**Core Features:**
1. Google OAuth authentication
2. AI chat integration (Groq API)
3. User data persistence (SQLite)
4. Modern responsive UI (Tailwind CSS)
5. Real-time chat interface

**Technical Requirements:**
- Python 3.8+
- Flask 3.0+
- SQLite (no external DB setup)
- Tailwind CSS via CDN
- External APIs: Google OAuth, Groq

**Non-Functional Requirements:**
- Simple enough for 2-hour workshop
- Production-ready code structure
- Well-commented for learning
- Mobile responsive
- Secure credential management

---

## Phase 2: Project Setup (TONIGHT - 20 minutes)

### 2.1 Repository Structure

```
flask-ai-workshop/
├── app.py                      # Main Flask application
├── database.py                 # Database helper functions
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Git exclusions
├── README.md                  # Project documentation
├── templates/
│   ├── base.html              # Base template with Tailwind
│   ├── index.html             # Landing/home page
│   ├── login.html             # Login page
│   └── chat.html              # Chat interface
└── static/
    ├── css/
    │   └── custom.css         # Custom styles (if needed)
    └── js/
        └── chat.js            # Frontend JavaScript for chat
```

### 2.2 Setup Checklist

**Step 1: Create project directory**
```bash
mkdir flask-ai-workshop
cd flask-ai-workshop
```

**Step 2: Initialize virtual environment**
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**Step 3: Create requirements.txt**
```
flask==3.0.0
authlib==1.3.0
requests==2.31.0
python-dotenv==1.0.0
```

**Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Create directory structure**
```bash
mkdir templates static
mkdir static/css static/js
```

**Step 6: Initialize Git**
```bash
git init
```

**Step 7: Create .gitignore**
```
venv/
__pycache__/
*.pyc
.env
*.db
.DS_Store
```

---

## Phase 3: External Service Setup (TONIGHT - 30 minutes)

### 3.1 Google OAuth Setup

**Steps:**
1. Go to: https://console.cloud.google.com
2. Create new project: "Flask-AI-Workshop"
3. Enable Google+ API
4. Configure OAuth consent screen:
   - User Type: External
   - App name: Flask AI Assistant
   - User support email: your email
   - Developer email: your email
5. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Name: Flask AI Workshop
   - Authorized redirect URIs: http://localhost:5000/authorize
6. Copy Client ID and Client Secret

**Save credentials to .env file**

### 3.2 Groq API Setup

**Steps:**
1. Go to: https://console.groq.com
2. Sign up / Log in
3. Go to API Keys section
4. Create new API key
5. Copy the key immediately (can't view again)

**Save to .env file**

### 3.3 Create .env file

```bash
# .env (DO NOT COMMIT TO GIT)
SECRET_KEY=your-random-secret-key-here-generate-with-python
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GROQ_API_KEY=your-groq-api-key
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3.4 Create .env.example

```bash
# .env.example (safe to commit)
SECRET_KEY=generate-with-python-secrets
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
GROQ_API_KEY=your-groq-key-here
```

---

## Phase 4: Backend Development (TONIGHT - 60 minutes)

### 4.1 Database Setup (15 minutes)

**File: database.py**

**Tasks:**
1. Create database initialization function
2. Create users table schema
3. Create helper functions:
   - `get_db()` - Get database connection
   - `init_db()` - Initialize database
   - `get_user_by_email(email)` - Fetch user
   - `create_user(google_id, email, name)` - Create user
4. Add proper error handling
5. Use context managers for connections

**Database Schema:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 Configuration (10 minutes)

**File: config.py**

**Tasks:**
1. Load environment variables
2. Create Config class
3. Add validation for required variables
4. Export configuration object

**Key configurations:**
- SECRET_KEY
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GROQ_API_KEY
- DEBUG mode

### 4.3 Main Application (35 minutes)

**File: app.py**

**Route Plan:**

1. **`/` (GET)** - Home/Landing page
   - Show login button if not authenticated
   - Redirect to /chat if authenticated

2. **`/login` (GET)** - Initiate Google OAuth
   - Redirect to Google sign-in
   - Handle OAuth flow

3. **`/authorize` (GET)** - OAuth callback
   - Receive authorization code
   - Exchange for user info
   - Create/update user in database
   - Set session
   - Redirect to /chat

4. **`/logout` (GET)** - Clear session
   - Remove session data
   - Redirect to home

5. **`/chat` (GET)** - Chat interface
   - Require authentication
   - Render chat page with user info

6. **`/api/chat` (POST)** - AI chat endpoint
   - Require authentication
   - Accept JSON: `{"message": "user message"}`
   - Call Groq API
   - Return JSON: `{"response": "ai response"}`
   - Handle errors gracefully

**Implementation Order:**
1. Flask app initialization
2. OAuth setup with authlib
3. Session management
4. Authentication routes (login, authorize, logout)
5. Protected routes (chat page)
6. API endpoint (chat)
7. Error handlers (404, 500)

---

## Phase 5: Frontend Development (TONIGHT - 40 minutes)

### 5.1 Base Template (10 minutes)

**File: templates/base.html**

**Tasks:**
1. HTML5 boilerplate
2. Include Tailwind CSS CDN
3. Add meta tags (viewport, charset)
4. Create navigation bar
5. Add Jinja2 blocks:
   - `{% block title %}`
   - `{% block content %}`
   - `{% block scripts %}`
6. Add flash message display area

### 5.2 Landing Page (10 minutes)

**File: templates/index.html**

**Tasks:**
1. Extend base template
2. Hero section with title
3. Feature list
4. "Sign in with Google" button
5. Simple responsive layout
6. Use Tailwind utility classes

### 5.3 Chat Interface (20 minutes)

**File: templates/chat.html**

**Tasks:**
1. Extend base template
2. Chat container (fixed height, scrollable)
3. Message display area
4. Message components:
   - User message (right-aligned, blue)
   - AI message (left-aligned, gray)
5. Input form:
   - Text input
   - Send button
6. Loading indicator
7. User profile in header (name, logout button)
8. Mobile responsive design

### 5.4 JavaScript for Chat (included in chat.html)

**Tasks:**
1. Handle form submission
2. Prevent default form behavior
3. Get user message from input
4. Display user message immediately
5. Show loading indicator
6. Send POST request to `/api/chat`
7. Handle response
8. Display AI message
9. Clear input field
10. Scroll to bottom
11. Handle errors
12. Add keyboard shortcuts (Enter to send)

---

## Phase 6: Testing & Debugging (TONIGHT - 20 minutes)

### 6.1 Local Testing Checklist

**Database:**
- [ ] Database file created
- [ ] Users table exists
- [ ] User can be created
- [ ] User can be retrieved

**Authentication:**
- [ ] Google OAuth redirect works
- [ ] User info received correctly
- [ ] User saved to database
- [ ] Session maintained
- [ ] Logout clears session
- [ ] Protected routes check authentication

**Chat Functionality:**
- [ ] Chat page loads for authenticated users
- [ ] Message can be sent
- [ ] Groq API responds
- [ ] AI response displays correctly
- [ ] Error handling works

**UI/UX:**
- [ ] Tailwind styles applied
- [ ] Responsive on mobile
- [ ] Navigation works
- [ ] Messages scroll properly
- [ ] Loading states visible

### 6.2 Common Issues & Fixes

**Issue: OAuth redirect fails**
- Check redirect URI matches Google Console exactly
- Must be http://localhost:5000/authorize

**Issue: Session not persisting**
- Check SECRET_KEY is set
- Check session cookies enabled

**Issue: Groq API errors**
- Verify API key is correct
- Check rate limits
- Ensure proper JSON formatting

**Issue: Database locked**
- Close all connections properly
- Use context managers

---

## Phase 7: Documentation (TONIGHT - 10 minutes)

### 7.1 README.md

**Sections:**
1. Project title and description
2. Features list
3. Prerequisites
4. Installation steps
5. Configuration (.env setup)
6. Running the application
7. Project structure
8. Technologies used
9. License

### 7.2 Code Comments

**Add comments for:**
- Function purposes
- Complex logic
- API endpoints
- Database queries
- Configuration options

**Comment style:**
```python
def get_user_by_email(email):
    """
    Fetch user from database by email.
    
    Args:
        email (str): User's email address
    
    Returns:
        dict: User data or None if not found
    """
    # Implementation
```

---

## Phase 8: Workshop Preparation (TOMORROW MORNING - 30 minutes)

### 8.1 Pre-Workshop Setup

**30 minutes before workshop:**
1. Test all functionality one more time
2. Have .env.example ready to share
3. Ensure Groq API key works
4. Have Google OAuth project ready
5. Prepare to show credentials setup
6. Open relevant documentation
7. Have cheat sheets accessible
8. Test internet connection
9. Close unnecessary applications
10. Have backup plan if API fails

### 8.2 Teaching Flow

**Phase 1: Introduction (10 min)**
- What we're building
- Why Flask, why Tailwind
- Architecture overview

**Phase 2: Setup (15 min)**
- Create project structure
- Install dependencies
- Verify environment

**Phase 3: Backend Core (40 min)**
- Database setup
- Google OAuth implementation
- Session management
- Chat API endpoint

**Phase 4: Frontend (40 min)**
- Base template
- Landing page
- Chat interface with Tailwind
- JavaScript functionality

**Phase 5: Demo & Extensions (15 min)**
- Live demo
- Ollama local LLM (brief)
- Extension ideas
- Q&A

---

## Phase 9: Extension Ideas (POST-WORKSHOP)

### Beginner Extensions
1. **Chat History**
   - Add messages table
   - Store conversations
   - Display previous chats

2. **User Profiles**
   - Display profile picture
   - Show user stats
   - Edit preferences

3. **Dark Mode**
   - Toggle theme
   - Save preference
   - Use Tailwind dark: classes

4. **Export Chat**
   - Download as TXT
   - Download as PDF
   - Copy to clipboard

### Intermediate Extensions
1. **Multiple AI Models**
   - Add model selector
   - Support Ollama, OpenAI, Claude
   - Compare responses

2. **Voice Input**
   - Web Speech API
   - Speech-to-text
   - Text-to-speech responses

3. **Markdown Support**
   - Parse AI responses
   - Render code blocks
   - Format lists and headers

4. **Real-time Updates**
   - WebSocket integration
   - Live typing indicators
   - Multi-user chat rooms

### Advanced Extensions
1. **RAG (Retrieval-Augmented Generation)**
   - Upload documents
   - Vector embeddings
   - Context-aware responses

2. **Fine-tuning Interface**
   - Collect training data
   - Fine-tune models
   - Deploy custom models

3. **Analytics Dashboard**
   - Usage statistics
   - Popular queries
   - Response times

4. **API Rate Limiting**
   - Request throttling
   - User quotas
   - Premium tiers

---

## Development Best Practices Used

### 1. Code Organization
- Separation of concerns (database, config, routes)
- Modular file structure
- Clear naming conventions

### 2. Security
- Environment variables for secrets
- Session-based authentication
- Input validation
- Error handling without exposing internals

### 3. Documentation
- Inline comments
- Function docstrings
- README with setup instructions
- Code examples in templates

### 4. Version Control
- Git initialization
- Proper .gitignore
- Meaningful commit messages
- .env.example for team setup

### 5. Testing Strategy
- Manual testing checklist
- Error scenario handling
- Cross-browser compatibility
- Mobile responsiveness

### 6. Code Quality
- Consistent formatting
- DRY (Don't Repeat Yourself)
- Clear variable names
- Proper indentation

---

## Timeline Summary

**TONIGHT (Total: ~3 hours)**
- Planning: 20 min ✅
- Setup: 20 min
- External services: 30 min
- Backend: 60 min
- Frontend: 40 min
- Testing: 20 min
- Documentation: 10 min
- Buffer: 20 min

**TOMORROW MORNING (30 min)**
- Final testing
- Workshop preparation

**WORKSHOP (2 hours)**
- Teaching and building together

---

## Success Criteria

**Technical:**
- [ ] Application runs without errors
- [ ] Users can authenticate with Google
- [ ] Chat functionality works
- [ ] UI is responsive and modern
- [ ] Code is well-commented

**Educational:**
- [ ] Students understand Flask basics
- [ ] Students can explain OAuth flow
- [ ] Students can style with Tailwind
- [ ] Students can make API calls
- [ ] Students can extend the project

**Workshop:**
- [ ] Completed in 2 hours
- [ ] All students have working code
- [ ] Questions answered
- [ ] Resources shared
- [ ] Students are motivated to continue learning

---

## Risk Mitigation

**Risk: API services down**
- Mitigation: Have backup mock responses ready
- Prepare sample data to demonstrate

**Risk: OAuth setup issues**
- Mitigation: Pre-create OAuth credentials
- Share credentials for workshop if needed

**Risk: Time overrun**
- Mitigation: Have pre-built sections ready
- Focus on core features, skip extensions

**Risk: Student environment issues**
- Mitigation: Test on Windows/Mac/Linux beforehand
- Have troubleshooting guide ready

**Risk: Internet connectivity**
- Mitigation: Download dependencies beforehand
- Have offline documentation

---

## Next Steps

Now that you have the plan, let's execute:

1. **Start with Phase 2** (Project Setup)
2. **Then Phase 3** (External Services Setup)
3. **Then Phase 4** (Backend Development)
4. **Then Phase 5** (Frontend Development)
5. **Then Phase 6** (Testing)

Ready to start building? I can create the files in order, starting with the project structure and requirements.txt.

---

**END OF PROJECT PLAN**

*This is your roadmap. Follow it step-by-step. Each phase builds on the previous one.*
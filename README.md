# Flask AI Workshop - AI Chat Assistant

A modern AI-powered chat application built with Flask, featuring Google OAuth authentication, Groq AI integration, and a beautiful Tailwind CSS interface.

![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Tailwind](https://img.shields.io/badge/Tailwind-3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🤖 **AI-Powered Chat**: Intelligent responses using Groq's LLaMA 3.1 70B model
- 🔐 **Secure Authentication**: Google OAuth 2.0 integration
- 💾 **User Management**: SQLite database for storing user data
- 🎨 **Modern UI**: Beautiful glassmorphic design with Tailwind CSS
- 📱 **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- ⚡ **Real-time Chat**: Instant AI responses with loading indicators
- 🛡️ **Error Handling**: Graceful error management and user feedback

## 📚 Tech Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0 (Web Framework)
- SQLite (Database)
- Authlib (OAuth Implementation)
- Requests (HTTP Client)

**Frontend:**
- HTML5
- Tailwind CSS 3.0 (Utility-first CSS)
- Vanilla JavaScript (Fetch API)

**External APIs:**
- Google OAuth 2.0
- Groq AI API (LLaMA 3.1)

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- A Google Cloud account (for OAuth)
- A Groq account (for AI API)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/DANI-cloud-del/Flask.git
cd Flask
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
# Generate a secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Add to .env:
SECRET_KEY=your-generated-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GROQ_API_KEY=your-groq-api-key
```

### 5. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure OAuth consent screen:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5000/authorize`
6. Copy Client ID and Client Secret to `.env`

### 6. Get Groq API Key

1. Go to [Groq Console](https://console.groq.com)
2. Sign up / Log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to `.env`

### 7. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📋 Project Structure

```
flask-ai-workshop/
├── app.py                    # Main Flask application
├── database.py               # Database management
├── config.py                 # Configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this!)
├── .env.example             # Environment template
├── .gitignore               # Git exclusions
├── README.md                # This file
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Landing page
│   └── chat.html            # Chat interface
└── database.db              # SQLite database (auto-created)
```

## 🔧 Configuration

### Environment Variables

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | Yes |
| `GROQ_API_KEY` | Groq AI API Key | Yes |
| `DEBUG` | Enable debug mode (True/False) | No |
| `FLASK_ENV` | Environment (development/production) | No |

## 📝 API Endpoints

### Authentication

- `GET /` - Landing page
- `GET /login` - Initiate Google OAuth flow
- `GET /authorize` - OAuth callback endpoint
- `GET /logout` - Log out current user

### Chat

- `GET /chat` - Chat interface (requires authentication)
- `POST /api/chat` - Send message to AI (requires authentication)
  ```json
  Request: {"message": "Your message"}
  Response: {"response": "AI response"}
  ```

## 👥 Usage

1. **Sign In**: Click "Sign in with Google" on the homepage
2. **Authorize**: Allow the application to access your Google account
3. **Chat**: Start chatting with the AI assistant
4. **Ask Questions**: The AI can help with:
   - General knowledge questions
   - Programming help and code examples
   - Explanations of concepts
   - Creative writing
   - And much more!

## 🛡️ Security

- All secrets are stored in environment variables
- OAuth 2.0 for secure authentication
- Session-based user management
- Input validation on all endpoints
- SQL injection protection via parameterized queries
- HTTPS recommended for production

## 🐛 Troubleshooting

### OAuth Redirect Error
**Problem**: "redirect_uri_mismatch" error

**Solution**: Ensure your Google OAuth redirect URI is exactly:
```
http://localhost:5000/authorize
```

### API Key Errors
**Problem**: "Invalid API key" or authentication errors

**Solution**: 
- Verify your `.env` file has correct API keys
- Check for extra spaces or quotes
- Regenerate keys if needed

### Database Locked
**Problem**: "database is locked" error

**Solution**:
- Close all connections properly
- Delete `database.db` and restart (will lose data)
- Use the context manager pattern (already implemented)

### Module Not Found
**Problem**: Import errors

**Solution**:
```bash
pip install -r requirements.txt
```

## 🚀 Deployment

### Production Considerations

**Do NOT use Flask's development server in production!**

Use a production WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Deployment Platforms

**Recommended platforms:**
- [Render](https://render.com) - Free tier available
- [Railway](https://railway.app) - Easy deployment
- [PythonAnywhere](https://www.pythonanywhere.com) - Flask-optimized
- [Heroku](https://www.heroku.com) - Classic choice
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)

### Environment Setup for Production

1. Set `DEBUG=False` in production
2. Use HTTPS (required for OAuth)
3. Set strong `SECRET_KEY`
4. Update OAuth redirect URI to production domain
5. Consider PostgreSQL instead of SQLite for scale

## 📚 Learning Resources

### Workshop Materials

- `FLASK_WORKSHOP_GUIDE.md` - Complete technical guide
- `FLASK_TOMORROW_NOTES.md` - Quick teaching notes
- `TAILWIND_CHEAT_SHEET.md` - Tailwind CSS reference
- `TAILWIND_BASICS.md` - Tailwind teaching notes
- `PROJECT_PLAN.md` - Development roadmap

### Official Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Groq API](https://console.groq.com/docs)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)

## ✨ Extension Ideas

### Beginner
- [ ] Add chat history to database
- [ ] Display previous conversations
- [ ] Add dark mode toggle
- [ ] Export chat as text file
- [ ] Add typing indicators

### Intermediate
- [ ] Multiple AI model support (OpenAI, Claude)
- [ ] Voice input (Web Speech API)
- [ ] Markdown rendering for AI responses
- [ ] User profile customization
- [ ] Rate limiting

### Advanced
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Vector embeddings for document search
- [ ] Fine-tune custom models
- [ ] WebSocket for real-time updates
- [ ] Multi-user chat rooms
- [ ] Admin dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**DANI**
- GitHub: [@DANI-cloud-del](https://github.com/DANI-cloud-del)

## 🙏 Acknowledgments

- Flask community for the excellent framework
- Groq for providing fast AI inference
- Google for OAuth infrastructure
- Tailwind CSS for the utility-first approach
- All workshop participants and contributors

## 💬 Support

If you have any questions or need help:

1. Check the troubleshooting section
2. Review the workshop guides
3. Open an issue on GitHub
4. Reach out during the workshop

---

**Built with ❤️ for learning Flask and AI integration**
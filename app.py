"""Flask AI Workshop - Main Application.

This is the main Flask application that demonstrates:
- Google OAuth authentication
- AI chat integration with Groq
- Session management
- RESTful API design
- Modern web UI with Tailwind CSS
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from authlib.integrations.flask_client import OAuth
import requests
from functools import wraps

# Import our custom modules
from config import config
from database import init_db, get_user_by_google_id, create_user, update_user

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Validate configuration
try:
    config.validate()
except ValueError as e:
    print(f"\n⚠️  Configuration Error: {e}\n")
    print("Please create a .env file with the required variables.")
    print("See .env.example for a template.\n")

# Initialize database
init_db()

# Setup OAuth
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================

def login_required(f):
    """Decorator to protect routes that require authentication.
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return 'This requires login'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# ROUTES - AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    """Landing page.
    
    Shows login option if not authenticated.
    Redirects to chat if already authenticated.
    """
    if 'user' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')


@app.route('/login')
def login():
    """Initiate Google OAuth login flow.
    
    Redirects user to Google sign-in page.
    """
    # Create the redirect URL for OAuth callback
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    """OAuth callback route.
    
    Google redirects here after user signs in.
    We receive the authorization code and exchange it for user info.
    """
    try:
        # Get the access token
        token = oauth.google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if user_info:
            google_id = user_info.get('sub')
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')
            
            # Check if user exists in database
            user = get_user_by_google_id(google_id)
            
            if user:
                # Update existing user info (in case name or picture changed)
                update_user(google_id, email, name, picture)
            else:
                # Create new user
                create_user(google_id, email, name, picture)
            
            # Store user info in session
            session['user'] = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture
            }
            
            flash(f'Welcome, {name}!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"OAuth error: {e}")
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Log out the current user.
    
    Clears the session and redirects to home page.
    """
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ROUTES - CHAT INTERFACE
# ============================================================================

@app.route('/chat')
@login_required
def chat():
    """Chat interface page.
    
    Protected route - requires authentication.
    Displays the AI chat interface.
    """
    user = session.get('user')
    return render_template('chat.html', user=user)


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """API endpoint for AI chat.
    
    Accepts JSON with user message, sends to Groq API, returns AI response.
    
    Request JSON:
        {
            "message": "User's message text"
        }
    
    Response JSON:
        {
            "response": "AI's response text"
        }
    
    Error Response:
        {
            "error": "Error message"
        }
    """
    try:
        # Get message from request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Call Groq API
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {config.GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-70b-versatile',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a helpful AI assistant. Provide clear, concise, and friendly responses.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 1024
            },
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract AI response
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    
    except requests.exceptions.RequestException as e:
        print(f"Groq API error: {e}")
        return jsonify({'error': 'Failed to get AI response. Please try again.'}), 500
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors (page not found)."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors (internal server error)."""
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Run the Flask development server
    # WARNING: Do not use in production! Use Gunicorn or similar.
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',  # Allow external connections
        port=5000
    )

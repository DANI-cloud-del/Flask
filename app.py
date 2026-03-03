"""Flask AI Workshop - Main Application.

This is the main Flask application that demonstrates:
- Google OAuth authentication
- AI chat integration with Groq
- Chat history storage
- Session management
- RESTful API design
- Modern web UI with Tailwind CSS
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from authlib.integrations.flask_client import OAuth
import requests
from functools import wraps
import json
import traceback

# Import our custom modules
from config import config
from database import (
    init_db, 
    get_user_by_google_id, 
    create_user, 
    update_user,
    get_user_id_by_google_id,
    create_conversation,
    get_user_conversations,
    get_conversation,
    get_conversation_messages,
    add_message,
    delete_conversation,
    update_conversation_title,
    generate_conversation_title,
    DATABASE_FILE
)

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
    """Decorator to protect routes that require authentication."""
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
    """Landing page."""
    if 'user' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')


@app.route('/login')
def login():
    """Initiate Google OAuth login flow."""
    print("\n" + "="*60)
    print("[DEBUG] LOGIN - Starting OAuth flow")
    print("="*60)
    
    redirect_uri = url_for('authorize', _external=True)
    print(f"[DEBUG] Redirect URI: {redirect_uri}")
    print(f"[DEBUG] Client ID: {config.GOOGLE_CLIENT_ID[:20]}...")
    print("="*60 + "\n")
    
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    """OAuth callback route."""
    print("\n" + "="*60)
    print("[DEBUG] AUTHORIZE - OAuth callback received")
    print("="*60)
    
    try:
        # Log request details
        print(f"[DEBUG] Request URL: {request.url}")
        print(f"[DEBUG] Request args: {dict(request.args)}")
        
        # Check for error in callback
        if 'error' in request.args:
            error = request.args.get('error')
            error_description = request.args.get('error_description', 'No description')
            print(f"[ERROR] OAuth error from Google: {error}")
            print(f"[ERROR] Description: {error_description}")
            flash(f'OAuth error: {error_description}', 'error')
            return redirect(url_for('index'))
        
        print("[DEBUG] Attempting to authorize access token...")
        token = oauth.google.authorize_access_token()
        print(f"[DEBUG] Token received: {bool(token)}")
        print(f"[DEBUG] Token keys: {list(token.keys()) if token else 'None'}")
        
        user_info = token.get('userinfo')
        print(f"[DEBUG] User info retrieved: {bool(user_info)}")
        
        if user_info:
            google_id = user_info.get('sub')
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')
            
            print(f"[DEBUG] User details:")
            print(f"  - Google ID: {google_id}")
            print(f"  - Email: {email}")
            print(f"  - Name: {name}")
            print(f"  - Picture: {picture[:50] if picture else 'None'}...")
            
            print("[DEBUG] Checking if user exists in database...")
            user = get_user_by_google_id(google_id)
            
            if user:
                print(f"[DEBUG] User found in DB (ID: {user['id']}), updating...")
                update_user(google_id, email, name, picture)
            else:
                print("[DEBUG] New user, creating in database...")
                user_id = create_user(google_id, email, name, picture)
                print(f"[DEBUG] User created with ID: {user_id}")
            
            print("[DEBUG] Setting session data...")
            session['user'] = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture
            }
            
            print(f"[DEBUG] Session user set: {bool(session.get('user'))}")
            print("="*60)
            print("[SUCCESS] Authentication successful!")
            print("="*60 + "\n")
            
            flash(f'Welcome, {name}!', 'success')
            return redirect(url_for('chat'))
        else:
            print("[ERROR] No user info in token")
            print(f"[ERROR] Token content: {token}")
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print("\n" + "="*60)
        print("[ERROR] Exception in authorize()")
        print("="*60)
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] Exception message: {str(e)}")
        print(f"[ERROR] Full traceback:")
        print(traceback.format_exc())
        print("="*60 + "\n")
        
        flash(f'Authentication failed: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Log out the current user."""
    print("\n[DEBUG] User logging out...")
    session.pop('user', None)
    session.pop('current_conversation_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ROUTES - CHAT INTERFACE
# ============================================================================

@app.route('/chat')
@app.route('/chat/<int:conversation_id>')
@login_required
def chat(conversation_id=None):
    """Chat interface page."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    
    # Get user's conversations for sidebar
    conversations = get_user_conversations(user_id)
    
    # If conversation_id provided, load that conversation
    current_conversation = None
    messages = []
    
    if conversation_id:
        current_conversation = get_conversation(conversation_id, user_id)
        if current_conversation:
            messages = get_conversation_messages(conversation_id, user_id)
            session['current_conversation_id'] = conversation_id
    
    return render_template(
        'chat.html', 
        user=user,
        conversations=conversations,
        current_conversation=current_conversation,
        messages=messages
    )


# ============================================================================
# API ROUTES - CHAT
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """API endpoint for AI chat with message storage."""
    print("\n" + "="*60)
    print("[DEBUG] API Chat Request Started")
    print("="*60)
    
    try:
        user = session.get('user')
        user_id = get_user_id_by_google_id(user['google_id'])
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        print(f"[DEBUG] User ID: {user_id}")
        print(f"[DEBUG] User message: {user_message}")
        print(f"[DEBUG] Conversation ID: {conversation_id}")
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create new conversation if none exists
        if not conversation_id:
            title = generate_conversation_title(user_message)
            conversation_id = create_conversation(user_id, title)
            session['current_conversation_id'] = conversation_id
            print(f"[DEBUG] Created new conversation: {conversation_id}")
        else:
            # Verify user owns this conversation
            conv = get_conversation(conversation_id, user_id)
            if not conv:
                return jsonify({'error': 'Invalid conversation'}), 403
        
        # Store user message
        add_message(conversation_id, 'user', user_message)
        print(f"[DEBUG] Stored user message")
        
        # Prepare AI request
        payload = {
            'model': 'llama-3.3-70b-versatile',
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
        }
        
        print(f"[DEBUG] Calling Groq API...")
        
        # Call Groq API
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {config.GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )
        
        print(f"[DEBUG] Response status: {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        
        # Extract AI response
        ai_response = result['choices'][0]['message']['content']
        print(f"[DEBUG] Got AI response ({len(ai_response)} chars)")
        
        # Store AI response
        add_message(conversation_id, 'assistant', ai_response)
        print(f"[DEBUG] Stored AI response")
        
        print("="*60)
        print("[DEBUG] Request completed successfully")
        print("="*60 + "\n")
        
        return jsonify({
            'response': ai_response,
            'conversation_id': conversation_id
        })
        
    except requests.exceptions.Timeout as e:
        print(f"[ERROR] Timeout: {e}")
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP Error: {e}")
        print(f"[ERROR] Response: {response.text}")
        return jsonify({'error': f'API error: {response.status_code}'}), 500
    
    except Exception as e:
        print(f"[ERROR] Unexpected error: {type(e).__name__}")
        print(f"[ERROR] Details: {e}")
        import traceback
        print(f"[ERROR] Traceback:\n{traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# ============================================================================
# API ROUTES - CONVERSATIONS
# ============================================================================

@app.route('/api/conversations', methods=['GET'])
@login_required
def api_get_conversations():
    """Get all conversations for the current user."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    conversations = get_user_conversations(user_id)
    return jsonify({'conversations': conversations})


@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
@login_required
def api_get_conversation(conversation_id):
    """Get a specific conversation with messages."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    
    conversation = get_conversation(conversation_id, user_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    messages = get_conversation_messages(conversation_id, user_id)
    
    return jsonify({
        'conversation': conversation,
        'messages': messages
    })


@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
@login_required
def api_delete_conversation(conversation_id):
    """Delete a conversation."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    
    if delete_conversation(conversation_id, user_id):
        # Clear from session if it's the current one
        if session.get('current_conversation_id') == conversation_id:
            session.pop('current_conversation_id', None)
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Conversation not found'}), 404


@app.route('/api/conversations/<int:conversation_id>/title', methods=['PUT'])
@login_required
def api_update_conversation_title(conversation_id):
    """Update conversation title."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    
    data = request.get_json()
    title = data.get('title', '').strip()
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    if update_conversation_title(conversation_id, title, user_id):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Conversation not found'}), 404


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Flask AI Workshop - Starting Server")
    print("="*60)
    print(f"Debug mode: {config.DEBUG}")
    print(f"Port: 5001")
    print(f"Groq API Key configured: {bool(config.GROQ_API_KEY)}")
    print(f"Database: {DATABASE_FILE}")
    print(f"Google Client ID: {config.GOOGLE_CLIENT_ID[:30]}...")
    print(f"Secret Key configured: {bool(config.SECRET_KEY)}")
    print("="*60 + "\n")
    
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5001
    )

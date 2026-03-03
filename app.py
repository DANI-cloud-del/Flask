"""Flask AI Workshop - Main Application.

This is the main Flask application that demonstrates:
- Google OAuth authentication
- AI chat integration with Groq
- Chat history storage with conversation memory
- File upload and processing
- Session management
- RESTful API design
- Modern web UI with Tailwind CSS
- Text-to-Speech settings
- Dark mode support
- Malayalam language mode
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from authlib.integrations.flask_client import OAuth
import requests
from functools import wraps
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

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
    add_attachment,
    get_message_attachments,
    DATABASE_FILE
)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
# HELPER FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_file_for_ai(file_path, file_type):
    """Process uploaded file for AI context."""
    try:
        if file_type in ['txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return f"File content:\n{content[:2000]}"  # Limit to 2000 chars
        elif file_type in ['png', 'jpg', 'jpeg', 'gif']:
            return "[Image uploaded - AI can describe images if requested]"
        elif file_type == 'pdf':
            return "[PDF document uploaded - content analysis available]"
        else:
            return f"[File uploaded: {file_type}]"
    except Exception as e:
        return f"[Could not process file: {str(e)}]"


def translate_text(text, target_lang='ml'):
    """Translate text using Google Translate API (free).
    
    Args:
        text: Text to translate
        target_lang: Target language code ('ml' for Malayalam)
    """
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text}"
        response = requests.get(url, timeout=5)
        if response.ok:
            result = response.json()
            translated = ''.join([item[0] for item in result[0] if item[0]])
            return translated
        return text
    except Exception as e:
        print(f"[TRANSLATE ERROR] {e}")
        return text


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
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    """OAuth callback route."""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if user_info:
            google_id = user_info.get('sub')
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')
            
            print(f"[AUTH] User logging in: {email}")
            
            user = get_user_by_google_id(google_id)
            
            if user:
                print(f"[AUTH] Existing user found: {user['id']}")
                update_user(google_id, email, name, picture)
            else:
                print(f"[AUTH] Creating new user")
                create_user(google_id, email, name, picture)
            
            session['user'] = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture
            }
            
            print(f"[AUTH] Session created for {email}")
            
            flash(f'Welcome, {name}!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"[AUTH ERROR] {e}")
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Log out the current user."""
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
    
    print(f"[CHAT] User: {user.get('email')}, ID: {user_id}")
    
    conversations = get_user_conversations(user_id)
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


@app.route('/settings')
@login_required
def settings():
    """Settings page with TTS and Malayalam mode configuration."""
    user = session.get('user')
    return render_template('settings.html', user=user)


# ============================================================================
# ROUTES - FILE UPLOADS
# ============================================================================

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ============================================================================
# API ROUTES - CHAT WITH CONVERSATION MEMORY & MALAYALAM MODE
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """API endpoint for AI chat with conversation memory, file support, and Malayalam mode.
    
    Supports both JSON (for simple messages) and FormData (for file uploads).
    """
    try:
        user = session.get('user')
        print(f"\n[API CHAT] User from session: {user}")
        
        if not user or 'google_id' not in user:
            print("[API CHAT ERROR] No user in session or missing google_id")
            return jsonify({'error': 'Session expired. Please log in again.'}), 401
        
        user_id = get_user_id_by_google_id(user['google_id'])
        print(f"[API CHAT] User ID from DB: {user_id}")
        
        if not user_id:
            print(f"[API CHAT ERROR] No user_id found for google_id: {user['google_id']}")
            return jsonify({'error': 'User not found. Please log in again.'}), 401
        
        # Handle file upload (FormData)
        uploaded_files = []
        file_context = ""
        
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                file_type = filename.rsplit('.', 1)[1].lower()
                file_size = os.path.getsize(file_path)
                
                uploaded_files.append({
                    'filename': unique_filename,
                    'original_filename': filename,
                    'file_type': file_type,
                    'file_size': file_size,
                    'file_path': file_path
                })
                
                file_context = process_file_for_ai(file_path, file_type)
                print(f"[API CHAT] File uploaded: {filename}")
        
        # Get message, conversation_id, and Malayalam mode from either JSON or FormData
        if request.is_json:
            data = request.get_json()
            user_message = data.get('message', '').strip()
            conversation_id = data.get('conversation_id')
            malayalam_mode = data.get('malayalam_mode', False)
        else:
            user_message = request.form.get('message', '').strip()
            conversation_id = request.form.get('conversation_id')
            malayalam_mode = request.form.get('malayalam_mode', 'false').lower() == 'true'
        
        print(f"[API CHAT] Message: '{user_message[:50]}...', Conv ID: {conversation_id}, Malayalam: {malayalam_mode}")
        
        if not user_message and not uploaded_files:
            return jsonify({'error': 'Message or file is required'}), 400
        
        # Translate to Malayalam if mode is enabled
        original_message = user_message
        if malayalam_mode and user_message:
            print(f"[MALAYALAM] Translating: {user_message[:30]}...")
            user_message = translate_text(user_message, 'ml')
            print(f"[MALAYALAM] Translated: {user_message[:30]}...")
        
        # Create new conversation if none exists
        if not conversation_id:
            title = generate_conversation_title(original_message or "File upload")
            print(f"[API CHAT] Creating new conversation: '{title}'")
            print(f"[API CHAT] With user_id: {user_id}")
            conversation_id = create_conversation(user_id, title)
            print(f"[API CHAT] Created conversation ID: {conversation_id}")
            session['current_conversation_id'] = conversation_id
        else:
            conversation_id = int(conversation_id)
            conv = get_conversation(conversation_id, user_id)
            if not conv:
                print(f"[API CHAT ERROR] Invalid conversation: {conversation_id}")
                return jsonify({'error': 'Invalid conversation'}), 403
            print(f"[API CHAT] Using existing conversation: {conversation_id}")
        
        # Build message content
        full_message = user_message
        if file_context:
            full_message += f"\n\n{file_context}"
        
        # Store user message (in Malayalam if translated)
        message_id = add_message(conversation_id, 'user', full_message, has_attachment=bool(uploaded_files))
        print(f"[API CHAT] Stored user message ID: {message_id}")
        
        # Store attachments
        for file_info in uploaded_files:
            add_attachment(
                message_id,
                file_info['filename'],
                file_info['original_filename'],
                file_info['file_type'],
                file_info['file_size'],
                file_info['file_path']
            )
        
        # Get conversation history for context (CONVERSATION MEMORY)
        conversation_history = get_conversation_messages(conversation_id, user_id, include_attachments=False)
        print(f"[API CHAT] Conversation history: {len(conversation_history)} messages")
        
        # Build system message based on language mode
        system_message = 'You are a helpful AI assistant. Provide clear, concise, and friendly responses. You have access to the full conversation history, so you can reference previous messages and maintain context.'
        
        if malayalam_mode:
            system_message += ' IMPORTANT: The user is communicating in Malayalam. You MUST respond ONLY in Malayalam language. Do not use English in your responses.'
            print(f"[MALAYALAM] AI will respond in Malayalam")
        
        # Build messages array with full conversation history
        messages = [
            {
                'role': 'system',
                'content': system_message
            }
        ]
        
        # Add conversation history (last 10 messages for context)
        for msg in conversation_history[-10:]:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        print(f"[API CHAT] Sending {len(messages)} messages to AI")
        
        # Prepare AI request with conversation memory
        payload = {
            'model': 'llama-3.3-70b-versatile',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 2048
        }
        
        # Call Groq API
        print(f"[API CHAT] Calling Groq API...")
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {config.GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract AI response
        ai_response = result['choices'][0]['message']['content']
        print(f"[API CHAT] AI response received: {len(ai_response)} chars")
        
        # Store AI response
        add_message(conversation_id, 'assistant', ai_response)
        print(f"[API CHAT] Stored AI response")
        
        return jsonify({
            'response': ai_response,
            'conversation_id': conversation_id,
            'files': [{'filename': f['original_filename'], 'type': f['file_type']} for f in uploaded_files],
            'malayalam_mode': malayalam_mode
        })
        
    except requests.exceptions.Timeout:
        print(f"[API CHAT ERROR] Timeout")
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    
    except requests.exceptions.HTTPError as e:
        print(f"[API CHAT ERROR] HTTP Error: {e}")
        return jsonify({'error': f'API error: {response.status_code}'}), 500
    
    except Exception as e:
        print(f"[API CHAT ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


# ============================================================================
# API ROUTES - TRANSLATION
# ============================================================================

@app.route('/api/translate', methods=['POST'])
@login_required
def api_translate():
    """API endpoint for text translation."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'ml')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        translated = translate_text(text, target_lang)
        return jsonify({'translated': translated})
        
    except Exception as e:
        print(f"[TRANSLATE ERROR] {e}")
        return jsonify({'error': 'Translation failed'}), 500


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
    try:
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
    except Exception as e:
        print(f"[API ERROR] get_conversation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Database error'}), 500


@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
@login_required
def api_delete_conversation(conversation_id):
    """Delete a conversation."""
    user = session.get('user')
    user_id = get_user_id_by_google_id(user['google_id'])
    
    if delete_conversation(conversation_id, user_id):
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
    print(f"[500 ERROR] {error}")
    import traceback
    traceback.print_exc()
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Flask AI Workshop - Starting Server")
    print("="*60)
    print(f"Debug mode: {config.DEBUG}")
    print(f"Port: 5001")
    print(f"Database: {DATABASE_FILE}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print("Features: Malayalam Mode, File Upload, Conversation Memory")
    print("="*60 + "\n")
    
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5001
    )

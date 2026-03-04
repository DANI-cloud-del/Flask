# 🔐 Google OAuth & Authentication - Complete Explanation

## 📊 Overview: How Authentication Works in Your App

```
👤 User Clicks "Sign in with Google"
   ↓
🌐 Redirected to Google Login
   ↓
🔑 User enters Google credentials
   ↓
✅ Google verifies and sends back user info
   ↓
💾 Your app stores user in database
   ↓
🎉 User gets access to /chat
```

---

## 🔧 Step 1: Google Cloud Console Setup

### What You Did (Or Need To Do):

1. **Create Project:**
   - Go to: https://console.cloud.google.com
   - Create new project: "Flask AI Chat"

2. **Enable OAuth:**
   - APIs & Services → Credentials
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: **Web application**
   - Name: "Flask AI Chat OAuth"

3. **Configure Redirect URIs:**
   ```
   Authorized redirect URIs:
   - http://localhost:5001/authorize        (for local dev)
   - https://your-app.onrender.com/authorize  (for production)
   ```

4. **Get Credentials:**
   - 🔑 **Client ID**: `123456789-abc...googleusercontent.com`
   - 🔒 **Client Secret**: `GOCSPX-xyz...`
   - Save these in `.env` file

### Why These URLs?

**Redirect URI = Where Google sends user after login**

```
User logs in at Google
         ↓
Google redirects to: http://localhost:5001/authorize
         ↓
Your /authorize route handles it
```

**Critical:** The redirect URI in Google Console MUST match your Flask route!

---

## 📦 Step 2: Flask OAuth Setup

### Code in `app.py`:

```python
from authlib.integrations.flask_client import OAuth

# Initialize OAuth
oauth = OAuth(app)

# Register Google as OAuth provider
oauth.register(
    name='google',  # ← You'll call this as oauth.google
    client_id=config.GOOGLE_CLIENT_ID,  # From .env
    client_secret=config.GOOGLE_CLIENT_SECRET,  # From .env
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'  # What data to request
    }
)
```

**What This Does:**
- Tells Authlib how to talk to Google
- Configures what user data to request (email, name, picture)
- Sets up the OAuth client

---

## 🚪 Step 3: The Three Authentication Routes

### Route 1: `/login` - Start OAuth Flow

```python
@app.route('/login')
def login():
    """Initiate Google OAuth login flow."""
    redirect_uri = url_for('authorize', _external=True)
    # redirect_uri = 'http://localhost:5001/authorize'
    return oauth.google.authorize_redirect(redirect_uri)
```

**What Happens:**
1. User clicks "Sign in with Google" button
2. Button links to `/login`
3. Flask redirects to Google login page
4. URL includes your redirect_uri parameter

**Google sees:**
```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=http://localhost:5001/authorize&
  scope=openid+email+profile&
  response_type=code
```

---

### Route 2: `/authorize` - Google Callback (THE MAGIC!) ✨

```python
@app.route('/authorize')
def authorize():
    """OAuth callback route - Google redirects here after login."""
    try:
        # 1. Exchange authorization code for access token
        token = oauth.google.authorize_access_token()
        
        # 2. Get user info from token
        user_info = token.get('userinfo')
        
        if user_info:
            # 3. Extract user details
            google_id = user_info.get('sub')  # Unique Google ID
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')  # Profile pic URL
            
            print(f"[AUTH] User logging in: {email}")
            
            # 4. Check if user exists in database
            user = get_user_by_google_id(google_id)
            
            if user:
                # Existing user - update their info
                print(f"[AUTH] Existing user found: {user['id']}")
                update_user(google_id, email, name, picture)
            else:
                # New user - create account
                print(f"[AUTH] Creating new user")
                create_user(google_id, email, name, picture)
            
            # 5. Store user in session (logged in!)
            session['user'] = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture
            }
            
            print(f"[AUTH] Session created for {email}")
            
            # 6. Success! Redirect to chat
            flash(f'Welcome, {name}!', 'success')
            return redirect(url_for('chat'))
        else:
            # Something went wrong
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        # Error during OAuth
        print(f"[AUTH ERROR] {e}")
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('index'))
```

**Step-by-Step Breakdown:**

#### Step 1: Exchange Code for Token
```python
token = oauth.google.authorize_access_token()
```

**What happens:**
- Google redirected user to `/authorize?code=ABC123`
- This code is single-use and expires in 10 minutes
- Authlib exchanges code for access token (behind the scenes)
- Access token allows fetching user info

#### Step 2: Get User Info
```python
user_info = token.get('userinfo')
```

**Returns:**
```json
{
  "sub": "115867420123456789",  // Unique Google ID
  "email": "danicherianbiju@gmail.com",
  "name": "DANI",
  "picture": "https://lh3.googleusercontent.com/...",
  "email_verified": true
}
```

#### Step 3-4: Database Check
```python
user = get_user_by_google_id(google_id)

if user:
    update_user(google_id, email, name, picture)  # Update existing
else:
    create_user(google_id, email, name, picture)  # Create new
```

**Database Query (database.py):**
```python
def get_user_by_google_id(google_id):
    cursor.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
    return cursor.fetchone()

def create_user(google_id, email, name, picture):
    cursor.execute(
        'INSERT INTO users (google_id, email, name, picture) VALUES (?, ?, ?, ?)',
        (google_id, email, name, picture)
    )
```

#### Step 5: Create Session
```python
session['user'] = {
    'google_id': google_id,
    'email': email,
    'name': name,
    'picture': picture
}
```

**Session = Encrypted cookie stored in browser**

**What this does:**
- Flask creates encrypted cookie
- Cookie sent to browser
- Browser sends cookie with every request
- Your app knows user is logged in

---

### Route 3: `/logout` - Clear Session

```python
@app.route('/logout')
def logout():
    """Log out the current user."""
    session.pop('user', None)  # Remove user from session
    session.pop('current_conversation_id', None)  # Clear conversation
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
```

**What happens:**
1. Removes user data from session
2. Browser cookie updated (user removed)
3. Next request: user not in session → blocked by `@login_required`

---

## 🔒 Step 4: The `@login_required` Decorator

### How It Protects Routes:

```python
def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
```

**Usage:**
```python
@app.route('/chat')
@login_required  # ← This protects the route!
def chat():
    user = session.get('user')  # Safe - user exists
    return render_template('chat.html', user=user)
```

**How It Works:**

1. **User tries to access `/chat`**
2. **Decorator runs first:**
   ```python
   if 'user' not in session:  # Check if logged in
       return redirect(url_for('index'))  # Not logged in → redirect home
   ```
3. **If user in session:**
   ```python
   return f(*args, **kwargs)  # Run the actual route function
   ```

**Visual Flow:**
```
User requests /chat
        ↓
@login_required checks session
        ↓
   ┌──────────────────┐
   │ User in session?  │
   └──────┬───────────┘
          │
    ┌─────┼─────┐
    │          │
   YES         NO
    │          │
    ↓          ↓
Allow    Redirect to /
(Show chat) (Login page)
```

---

## 🔍 Why You Can't Manually Go to /chat

### Test This:

1. **Open incognito window**
2. **Go to:** `http://localhost:5001/chat`
3. **Result:** Redirected to `/` (home page)

**Why?**

```python
@app.route('/chat')
@login_required  # ← THIS!
def chat():
    # This never runs if not logged in
```

**Decorator checks:**
```python
if 'user' not in session:  # True in incognito (no session)
    return redirect(url_for('index'))  # Redirect home
```

**To access /chat, you MUST:**
1. Click "Sign in with Google"
2. Complete OAuth flow
3. Get `session['user']` set
4. Then `/chat` works!

---

## 🧑‍💻 The Session Object Explained

### What is `session`?

**Session = Encrypted dictionary stored in browser cookie**

```python
# Flask stores this:
session['user'] = {
    'google_id': '115867420123456789',
    'email': 'danicherianbiju@gmail.com',
    'name': 'DANI',
    'picture': 'https://...'
}

# Browser receives cookie:
Set-Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyI...; Path=/; HttpOnly
```

**Properties:**
- ✅ **Encrypted** (using `SECRET_KEY`)
- ✅ **HttpOnly** (JavaScript can't access)
- ✅ **Sent with every request**
- ✅ **Persists across page loads**
- ✅ **Cleared on logout**

### How Session Works:

```
Request 1 (Login):
  User logs in
  ↓
  session['user'] = {...}
  ↓
  Flask encrypts data
  ↓
  Set-Cookie: session=encrypted_data
  ↓
  Browser stores cookie

Request 2 (Chat):
  Browser sends: Cookie: session=encrypted_data
  ↓
  Flask decrypts data
  ↓
  session['user'] available in Python
  ↓
  @login_required sees user
  ↓
  Access granted!
```

---

## ❓ Your Questions Answered

### Q1: Can we make `/authorize` a separate template?

**Answer:** No, and here's why:

```python
@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    # ... process token ...
    return redirect(url_for('chat'))  # ← Immediate redirect!
```

**The flow:**
1. Google redirects to `/authorize?code=ABC123`
2. Your code exchanges code for token (instant)
3. Your code saves user to database (instant)
4. Your code redirects to `/chat` (instant)

**Total time: < 500ms**

User **never sees** `/authorize` - it's just a processing endpoint!

**If you want a loading screen:**

You could add one BEFORE redirect:

```python
@app.route('/authorize')
def authorize():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        # ... save user ...
        
        # Show loading template briefly
        return render_template('loading.html', redirect_to='/chat')
        
    except Exception as e:
        return redirect(url_for('index'))
```

**loading.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Logging in...</title>
    <meta http-equiv="refresh" content="1;url={{ redirect_to }}">
</head>
<body>
    <h1>⏳ Logging you in...</h1>
    <script>
        setTimeout(() => {
            window.location.href = "{{ redirect_to }}";
        }, 1000);
    </script>
</body>
</html>
```

**But this is unnecessary** - OAuth is instant!

### Q2: Do we need Jinja for a template?

**Answer:** Yes, all Flask templates use Jinja2.

**Any `.html` file in `templates/` uses Jinja:**

```html
<!-- templates/chat.html -->
<h1>Welcome, {{ user.name }}!</h1>  <!-- ← Jinja syntax -->
<img src="{{ user.picture }}">  <!-- ← Jinja syntax -->

{% if user %}  <!-- ← Jinja if statement -->
    <p>Logged in as: {{ user.email }}</p>
{% else %}
    <p>Not logged in</p>
{% endif %}
```

**Flask automatically uses Jinja2 for all `render_template()` calls.**

### Q3: What URLs did we put in Google Console?

**For Local Development:**
```
Authorized JavaScript origins:
- http://localhost:5001

Authorized redirect URIs:
- http://localhost:5001/authorize
```

**For Production (Render):**
```
Authorized JavaScript origins:
- https://flask-ai-chat.onrender.com

Authorized redirect URIs:
- https://flask-ai-chat.onrender.com/authorize
```

**Both at same time:**
You can have BOTH in Google Console simultaneously!

```
Redirect URIs:
- http://localhost:5001/authorize         ← For dev
- https://your-app.onrender.com/authorize  ← For production
```

Google allows multiple redirect URIs! 🎉

---

## 📊 Complete Authentication Flow Diagram

```
┌──────────────────────────────────────────────┐
│           USER AUTHENTICATION FLOW               │
└──────────────────────────────────────────────┘

1. User visits http://localhost:5001/
   │
   v
   ┌───────────────────────────────┐
   │ @app.route('/')                │
   │ def index():                    │
   │   if 'user' in session:         │
   │     return redirect('/chat')    │  ← Already logged in
   │   return render_template(...)   │  ← Show login page
   └───────────────────────────────┘
   │
   v
2. User clicks "Sign in with Google"
   │
   v
   ┌───────────────────────────────────────────┐
   │ @app.route('/login')                        │
   │ def login():                                │
   │   redirect_uri = 'http://localhost:5001/authorize' │
   │   return oauth.google.authorize_redirect(redirect_uri) │
   └───────────────────────────────────────────┘
   │
   v
3. Redirected to Google
   https://accounts.google.com/o/oauth2/v2/auth?client_id=...
   │
   v
4. User enters Google credentials
   │
   v
5. Google verifies user
   │
   v
6. Google redirects back with code:
   http://localhost:5001/authorize?code=ABC123XYZ
   │
   v
   ┌──────────────────────────────────────────┐
   │ @app.route('/authorize')                   │
   │ def authorize():                           │
   │   # Exchange code for token                 │
   │   token = oauth.google.authorize_access_token() │
   │                                              │
   │   # Get user info                           │
   │   user_info = token.get('userinfo')        │
   │                                              │
   │   # Save to database                        │
   │   if user exists:                           │
   │     update_user(...)                        │
   │   else:                                     │
   │     create_user(...)                        │
   │                                              │
   │   # Create session                          │
   │   session['user'] = user_info              │
   │                                              │
   │   # Redirect to chat                        │
   │   return redirect('/chat')                 │
   └──────────────────────────────────────────┘
   │
   v
7. User lands on /chat (logged in!)
   │
   v
   ┌──────────────────────────────────────────┐
   │ @app.route('/chat')                        │
   │ @login_required  ← Checks session!        │
   │ def chat():                                │
   │   user = session.get('user')  ← Available! │
   │   # Show chat interface                     │
   └──────────────────────────────────────────┘
```

---

## 🛠️ Testing Your Understanding

### Experiment 1: Try Manual Access

```bash
# Open incognito window
curl http://localhost:5001/chat

# Result: Redirected to /
# Why? @login_required blocks it!
```

### Experiment 2: Check Session

Add this route temporarily:

```python
@app.route('/debug-session')
def debug_session():
    return jsonify({
        'has_user': 'user' in session,
        'user_data': session.get('user', {})
    })
```

Visit:
- Before login: `{"has_user": false}`
- After login: `{"has_user": true, "user_data": {...}}`

### Experiment 3: Break OAuth

In Google Console, remove `http://localhost:5001/authorize` from redirect URIs.

Then try to login:

**Error:** `redirect_uri_mismatch`

**Why?** Google doesn't trust that URL anymore!

---

## 🔑 Security Features Included

### 1. Session Encryption

```python
app.config['SECRET_KEY'] = config.SECRET_KEY
```

- Session data encrypted with `SECRET_KEY`
- Cannot be tampered with
- If someone modifies cookie, Flask rejects it

### 2. HttpOnly Cookies

- JavaScript cannot access session cookie
- Prevents XSS attacks
- Even if malicious JS runs, can't steal session

### 3. OAuth (Not Password Storage)

- You never see user's Google password
- Google handles authentication
- You just get verified user info
- User can revoke access anytime

### 4. Google ID (Not Email) for Lookup

```python
user = get_user_by_google_id(google_id)  # ← google_id
# NOT: get_user_by_email(email)
```

**Why?**
- Email can change
- `google_id` (sub) is permanent
- More secure

---

## 📚 Summary: Key Concepts

### 1. OAuth Flow
```
Your App → Google → User Logs In → Google → Your App
```

### 2. Redirect URI
```
http://localhost:5001/authorize  ← Where Google sends user back
```

### 3. Session
```
session['user'] = {...}  ← Encrypted cookie in browser
```

### 4. Authentication
```
@login_required  ← Checks if 'user' in session
```

### 5. Database
```
Google ID → Lookup user → Create or update → Set session
```

---

## 🎓 Next Steps

Want to understand more?

1. **Study the flow diagram** (above)
2. **Add print statements** to see OAuth in action
3. **Try breaking it** (remove redirect URI, etc.)
4. **Check session cookie** in browser DevTools
5. **Read Authlib docs:** https://docs.authlib.org

---

**You now understand the complete authentication system!** 🎉

Questions? Ask away! 🚀

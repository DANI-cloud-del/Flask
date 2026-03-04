# 🎨 Google OAuth Authentication - Visual Flowcharts

## 📊 Complete Authentication Flow (High-Level)

```mermaid
flowchart TD
    Start([User visits app]) --> CheckSession{Logged in?}
    CheckSession -->|Yes| Chat[Show Chat Page]
    CheckSession -->|No| Landing[Show Landing Page]
    
    Landing --> ClickLogin[User clicks 'Sign in with Google']
    ClickLogin --> LoginRoute["/login route"]
    LoginRoute --> RedirectGoogle[Redirect to Google]
    
    RedirectGoogle --> GoogleLogin[Google Login Page]
    GoogleLogin --> UserEntersCreds[User enters credentials]
    UserEntersCreds --> GoogleVerify{Google verifies}
    
    GoogleVerify -->|Invalid| GoogleError[Show error]
    GoogleError --> GoogleLogin
    
    GoogleVerify -->|Valid| GoogleCallback[Google redirects with code]
    GoogleCallback --> AuthorizeRoute["/authorize route"]
    
    AuthorizeRoute --> ExchangeToken[Exchange code for token]
    ExchangeToken --> GetUserInfo[Get user info from token]
    GetUserInfo --> CheckDB{User exists in DB?}
    
    CheckDB -->|Yes| UpdateUser[Update user info]
    CheckDB -->|No| CreateUser[Create new user]
    
    UpdateUser --> CreateSession[Create session cookie]
    CreateUser --> CreateSession
    
    CreateSession --> RedirectChat[Redirect to /chat]
    RedirectChat --> Chat
    
    Chat --> UserAction{User action}
    UserAction -->|Send message| APIChat["/api/chat"]
    UserAction -->|Logout| LogoutRoute["/logout"]
    UserAction -->|Close browser| SessionPersists[Session persists]
    
    LogoutRoute --> ClearSession[Clear session]
    ClearSession --> Landing
    
    APIChat --> CheckAuth{Authenticated?}
    CheckAuth -->|No| Redirect401[Return 401]
    CheckAuth -->|Yes| ProcessMessage[Process message]
    ProcessMessage --> SaveDB[Save to database]
    SaveDB --> CallGroq[Call Groq API]
    CallGroq --> ReturnResponse[Return AI response]
    ReturnResponse --> Chat
```

---

## 🔐 Detailed OAuth Flow (Technical)

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask as Flask App
    participant Google
    participant DB as Database
    
    User->>Browser: Visit http://localhost:5001/
    Browser->>Flask: GET /
    Flask->>Flask: Check session['user']
    
    alt User logged in
        Flask->>Browser: Redirect to /chat
    else User not logged in
        Flask->>Browser: Show landing page with login button
    end
    
    User->>Browser: Click "Sign in with Google"
    Browser->>Flask: GET /login
    Flask->>Flask: Generate redirect_uri
    Flask->>Browser: Redirect to Google OAuth
    
    Browser->>Google: GET https://accounts.google.com/o/oauth2/v2/auth
    Google->>Browser: Show Google Login Page
    
    User->>Google: Enter email & password
    Google->>Google: Verify credentials
    Google->>Browser: Redirect to /authorize?code=ABC123
    
    Browser->>Flask: GET /authorize?code=ABC123
    Flask->>Google: Exchange code for access token
    Google->>Flask: Return token + userinfo
    
    Flask->>Flask: Extract user data (email, name, picture, google_id)
    Flask->>DB: SELECT * FROM users WHERE google_id = ?
    
    alt User exists
        DB->>Flask: Return user data
        Flask->>DB: UPDATE user SET email, name, picture, last_login
    else User doesn't exist
        DB->>Flask: Return null
        Flask->>DB: INSERT INTO users (google_id, email, name, picture)
    end
    
    Flask->>Flask: session['user'] = {google_id, email, name, picture}
    Flask->>Browser: Set-Cookie: session=encrypted_data
    Flask->>Browser: Redirect to /chat
    
    Browser->>Flask: GET /chat (with session cookie)
    Flask->>Flask: @login_required checks session
    Flask->>Flask: 'user' in session? ✅ Yes
    Flask->>Browser: Render chat.html with user data
```

---

## 🛡️ Authentication Guard (@login_required) Flow

```mermaid
flowchart TD
    Start([User requests protected route]) --> Decorator[@login_required decorator runs]
    
    Decorator --> CheckSession{Is 'user' in session?}
    
    CheckSession -->|No| Flash[Flash warning message]
    Flash --> RedirectHome[Redirect to /]
    RedirectHome --> ShowLogin[Show login page]
    
    CheckSession -->|Yes| ExtractUser[Extract user from session]
    ExtractUser --> RunFunction[Execute route function]
    RunFunction --> ReturnResponse[Return page/data to user]
    
    style CheckSession fill:#ff6b6b
    style RunFunction fill:#51cf66
    style RedirectHome fill:#ffd93d
```

---

## 🔄 Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> NoSession: User visits site
    
    NoSession --> Authenticating: Click "Sign in"
    Authenticating --> OAuthFlow: Redirect to Google
    OAuthFlow --> Authenticating: Google callback
    Authenticating --> SessionCreated: Create session cookie
    
    SessionCreated --> Active: User logged in
    
    Active --> Active: Browse pages
    Active --> Active: Send messages
    Active --> Active: Close/reopen browser (cookie persists)
    
    Active --> NoSession: Click logout
    Active --> NoSession: Session expires (rare)
    Active --> NoSession: Clear cookies
    
    NoSession --> [*]
```

---

## 📡 API Chat Request Flow (with Authentication)

```mermaid
flowchart TD
    Start([User sends message]) --> Frontend[Frontend JavaScript]
    Frontend --> PrepareData[Prepare request data]
    PrepareData --> SendRequest[POST /api/chat]
    
    SendRequest --> FlaskReceives[Flask receives request]
    FlaskReceives --> CheckAuth{@login_required}
    
    CheckAuth -->|No session| Return401[Return 401 Unauthorized]
    Return401 --> ShowError[Show error to user]
    
    CheckAuth -->|Has session| ExtractUser[Extract user from session]
    ExtractUser --> GetUserID[Get user_id from database]
    GetUserID --> ValidateConv{Conversation ID provided?}
    
    ValidateConv -->|No| CreateConv[Create new conversation]
    ValidateConv -->|Yes| CheckOwner{User owns conversation?}
    
    CheckOwner -->|No| Return403[Return 403 Forbidden]
    CheckOwner -->|Yes| UseExisting[Use existing conversation]
    
    CreateConv --> SaveMessage[Save user message to DB]
    UseExisting --> SaveMessage
    
    SaveMessage --> GetHistory[Get conversation history]
    GetHistory --> BuildPrompt[Build messages array for AI]
    BuildPrompt --> CallGroq[Call Groq API]
    
    CallGroq --> ReceiveResponse[Receive AI response]
    ReceiveResponse --> SaveAI[Save AI message to DB]
    SaveAI --> ReturnJSON[Return JSON to frontend]
    ReturnJSON --> DisplayMessage[Display in chat UI]
    
    style CheckAuth fill:#ff6b6b
    style CallGroq fill:#4dabf7
    style SaveMessage fill:#51cf66
```

---

## 🗄️ Database Operations During Auth

```mermaid
flowchart LR
    subgraph "OAuth Callback"
        A[Get user info from Google] --> B{Check if user exists}
    end
    
    subgraph "Database Query"
        B -->|Query| C[SELECT * FROM users<br/>WHERE google_id = ?]
    end
    
    subgraph "User Exists Path"
        C -->|Found| D[UPDATE users<br/>SET email, name, picture, last_login<br/>WHERE google_id = ?]
        D --> G[Return user_id]
    end
    
    subgraph "New User Path"
        C -->|Not Found| E[INSERT INTO users<br/>google_id, email, name, picture]
        E --> F[Get newly created user_id]
        F --> G
    end
    
    subgraph "Session Creation"
        G --> H[Create session cookie]
        H --> I[Redirect to /chat]
    end
    
    style D fill:#4dabf7
    style E fill:#51cf66
    style H fill:#ffd93d
```

---

## 🎯 Route Protection Mechanism

```mermaid
flowchart TD
    subgraph "Public Routes (No Auth Required)"
        A1[/ - Landing page]
        A2[/login - Start OAuth]
        A3[/authorize - OAuth callback]
    end
    
    subgraph "Protected Routes (@login_required)"
        B1[/chat - Chat interface]
        B2[/settings - Settings page]
        B3[/api/chat - Send message]
        B4[/api/conversations - Get conversations]
        B5[/logout - End session]
    end
    
    subgraph "Session Check"
        C{session['user']<br/>exists?}
    end
    
    A1 --> NoAuth[Accessible to everyone]
    A2 --> NoAuth
    A3 --> NoAuth
    
    B1 --> C
    B2 --> C
    B3 --> C
    B4 --> C
    B5 --> C
    
    C -->|Yes| Allow[✅ Allow access]
    C -->|No| Block[❌ Redirect to /]
    
    style A1 fill:#51cf66
    style A2 fill:#51cf66
    style A3 fill:#51cf66
    style B1 fill:#ff6b6b
    style B2 fill:#ff6b6b
    style B3 fill:#ff6b6b
    style Allow fill:#51cf66
    style Block fill:#ff6b6b
```

---

## 🍪 Session Cookie Flow

```mermaid
flowchart TD
    subgraph "Login Process"
        A[User authenticates via Google] --> B[Flask receives user info]
        B --> C[Create session dictionary]
        C --> D["session['user'] = {<br/>google_id, email, name, picture<br/>}"]
    end
    
    subgraph "Flask Session Handling"
        D --> E[Serialize to JSON]
        E --> F[Encrypt with SECRET_KEY]
        F --> G[Base64 encode]
    end
    
    subgraph "Browser"
        G --> H[Set-Cookie header]
        H --> I[Browser stores cookie]
        I --> J[Cookie sent with every request]
    end
    
    subgraph "Subsequent Requests"
        J --> K[Flask receives Cookie header]
        K --> L[Decode Base64]
        L --> M[Decrypt with SECRET_KEY]
        M --> N[Deserialize JSON]
        N --> O["session['user'] available<br/>in Python code"]
    end
    
    O --> P{Route needs auth?}
    P -->|Yes| Q[@login_required checks session]
    P -->|No| R[Execute route normally]
    
    style D fill:#4dabf7
    style F fill:#ffd93d
    style I fill:#51cf66
    style O fill:#51cf66
```

---

## 🔄 Complete User Journey (First Time User)

```mermaid
journey
    title First-Time User Authentication Journey
    section Discovery
      Visit app URL: 5: User
      See landing page: 5: User
      Read about features: 4: User
    section Authentication
      Click "Sign in with Google": 5: User
      Redirected to Google: 3: System
      Enter Google credentials: 4: User
      Google verifies: 5: Google
      Redirected back to app: 3: System
    section First Use
      Account created in database: 5: System
      Session cookie created: 5: System
      Redirected to chat: 5: System
      See welcome message: 5: User
      Send first message: 5: User
      Receive AI response: 5: User, AI
    section Return Visit
      Close browser: 5: User
      Reopen app (same day): 5: User
      Still logged in (cookie persists): 5: System
      Continue chatting: 5: User
```

---

## 🔐 Security Layers Visualization

```mermaid
flowchart TB
    subgraph "Layer 1: OAuth (Google)"
        A[Google verifies user identity]
        A1[No password stored in your app]
        A2[User can revoke access anytime]
    end
    
    subgraph "Layer 2: Session Encryption"
        B[Session data encrypted with SECRET_KEY]
        B1[Cookie signed to prevent tampering]
        B2[HttpOnly flag prevents JS access]
    end
    
    subgraph "Layer 3: Route Protection"
        C[@login_required decorator]
        C1[Checks session before every protected route]
        C2[Blocks unauthenticated requests]
    end
    
    subgraph "Layer 4: Database Security"
        D[User lookup by google_id (not email)]
        D1[Permanent identifier]
        D2[Foreign key constraints]
    end
    
    subgraph "Layer 5: API Validation"
        E[Verify user owns resources]
        E1[Check conversation ownership]
        E2[Validate user_id matches session]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F[✅ Secure Access Granted]
    
    style F fill:#51cf66
```

---

## 🎭 Comparison: With vs Without Authentication

```mermaid
flowchart LR
    subgraph "Without Auth (Insecure)"
        N1[Anyone can access /chat] --> N2[No user identification]
        N2 --> N3[All conversations shared]
        N3 --> N4[No privacy]
        N4 --> N5[❌ Security risk]
    end
    
    subgraph "With Auth (Your App)"
        Y1[Must login to access /chat] --> Y2[User identified by google_id]
        Y2 --> Y3[Personal conversations only]
        Y3 --> Y4[Data privacy maintained]
        Y4 --> Y5[✅ Secure & private]
    end
    
    style N5 fill:#ff6b6b
    style Y5 fill:#51cf66
```

---

## 🧪 Testing Authentication Flow

```mermaid
flowchart TD
    Start([Start Testing]) --> Test1[Open incognito window]
    
    Test1 --> Test2[Try accessing /chat directly]
    Test2 --> Check1{Redirected to /?}
    Check1 -->|Yes| Pass1[✅ Test 1 Passed]
    Check1 -->|No| Fail1[❌ Auth not working]
    
    Pass1 --> Test3[Click 'Sign in with Google']
    Test3 --> Test4[Complete Google login]
    Test4 --> Check2{Redirected to /chat?}
    Check2 -->|Yes| Pass2[✅ Test 2 Passed]
    Check2 -->|No| Fail2[❌ OAuth not working]
    
    Pass2 --> Test5[Check session cookie in DevTools]
    Test5 --> Check3{Cookie exists?}
    Check3 -->|Yes| Pass3[✅ Test 3 Passed]
    Check3 -->|No| Fail3[❌ Session not created]
    
    Pass3 --> Test6[Send a chat message]
    Test6 --> Check4{Message sent successfully?}
    Check4 -->|Yes| Pass4[✅ Test 4 Passed]
    Check4 -->|No| Fail4[❌ API auth issue]
    
    Pass4 --> Test7[Click logout]
    Test7 --> Check5{Session cleared?}
    Check5 -->|Yes| Pass5[✅ All Tests Passed! 🎉]
    Check5 -->|No| Fail5[❌ Logout not working]
    
    Fail1 --> Debug[Check @login_required]
    Fail2 --> Debug
    Fail3 --> Debug
    Fail4 --> Debug
    Fail5 --> Debug
    
    Debug --> FixIssue[Fix and retest]
    FixIssue --> Start
    
    style Pass5 fill:#51cf66
    style Fail1 fill:#ff6b6b
    style Fail2 fill:#ff6b6b
    style Fail3 fill:#ff6b6b
    style Fail4 fill:#ff6b6b
    style Fail5 fill:#ff6b6b
```

---

## 📊 Data Flow: User Login to First Message

```mermaid
flowchart TD
    A[User clicks login] --> B[/login route]
    B --> C[Redirect to Google]
    C --> D[Google authenticates]
    D --> E[/authorize callback]
    
    E --> F[Exchange code for token]
    F --> G[Get user info]
    G --> H[Query database]
    
    H --> I{User exists?}
    I -->|No| J[INSERT INTO users]
    I -->|Yes| K[UPDATE users]
    
    J --> L[Get user_id]
    K --> L
    
    L --> M["session['user'] = {...}"]
    M --> N[Redirect to /chat]
    N --> O[Load chat interface]
    
    O --> P[User types message]
    P --> Q[POST /api/chat]
    Q --> R[@login_required]
    R --> S[Get user from session]
    S --> T[Get user_id from DB]
    T --> U[Create/get conversation_id]
    U --> V[INSERT message into DB]
    V --> W[Call Groq API]
    W --> X[Save AI response to DB]
    X --> Y[Return to frontend]
    Y --> Z[Display in chat]
    
    style M fill:#ffd93d
    style R fill:#ff6b6b
    style W fill:#4dabf7
    style Z fill:#51cf66
```

---

## 🎯 Quick Reference: Authentication Checkpoints

```mermaid
mindmap
  root((Authentication<br/>System))
    Google OAuth
      /login starts flow
      /authorize receives callback
      Exchange code for token
      Get user info
    Session Management
      Encrypted cookie
      session user object
      Persists across requests
      Cleared on logout
    Route Protection
      @login_required decorator
      Checks session user
      Redirects if not authenticated
      Works on routes and APIs
    Database
      Users table
      google_id unique identifier
      Create or update on login
      Foreign keys to conversations
    Security
      No password storage
      HttpOnly cookies
      SECRET_KEY encryption
      OAuth token validation
```

---

## 📝 Summary Diagram

```mermaid
flowchart LR
    A[🌐 Google OAuth] --> B[🍪 Session Cookie]
    B --> C[🛡️ @login_required]
    C --> D[💾 Database]
    D --> E[✅ Authenticated Access]
    
    style A fill:#4285f4
    style B fill:#ffd93d
    style C fill:#ff6b6b
    style D fill:#51cf66
    style E fill:#a78bfa
```

---

**All these diagrams visually explain your authentication system!** 🎨

The flowcharts show:
- ✅ Complete OAuth flow
- ✅ Session management
- ✅ Route protection
- ✅ Database operations
- ✅ Security layers
- ✅ Testing procedures

**View on GitHub with proper Mermaid rendering!** 🚀

# 🎨 Google OAuth Authentication - Visual Flowcharts

## 📊 Complete Authentication Flow (High-Level)

```mermaid
flowchart TD
    Start([User visits app]) --> CheckSession{Logged in?}
    CheckSession -->|Yes| Chat[Show Chat Page]
    CheckSession -->|No| Landing[Show Landing Page]
    
    Landing --> ClickLogin[User clicks Sign in with Google]
    ClickLogin --> LoginRoute[login route]
    LoginRoute --> RedirectGoogle[Redirect to Google]
    
    RedirectGoogle --> GoogleLogin[Google Login Page]
    GoogleLogin --> UserEntersCreds[User enters credentials]
    UserEntersCreds --> GoogleVerify{Google verifies}
    
    GoogleVerify -->|Invalid| GoogleError[Show error]
    GoogleError --> GoogleLogin
    
    GoogleVerify -->|Valid| GoogleCallback[Google redirects with code]
    GoogleCallback --> AuthorizeRoute[authorize route]
    
    AuthorizeRoute --> ExchangeToken[Exchange code for token]
    ExchangeToken --> GetUserInfo[Get user info from token]
    GetUserInfo --> CheckDB{User exists in DB?}
    
    CheckDB -->|Yes| UpdateUser[Update user info]
    CheckDB -->|No| CreateUser[Create new user]
    
    UpdateUser --> CreateSession[Create session cookie]
    CreateUser --> CreateSession
    
    CreateSession --> RedirectChat[Redirect to chat]
    RedirectChat --> Chat
    
    Chat --> UserAction{User action}
    UserAction -->|Send message| APIChat[api chat endpoint]
    UserAction -->|Logout| LogoutRoute[logout route]
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
    
    User->>Browser: Visit localhost:5001
    Browser->>Flask: GET /
    Flask->>Flask: Check session user
    
    alt User logged in
        Flask->>Browser: Redirect to /chat
    else User not logged in
        Flask->>Browser: Show landing page with login button
    end
    
    User->>Browser: Click Sign in with Google
    Browser->>Flask: GET /login
    Flask->>Flask: Generate redirect_uri
    Flask->>Browser: Redirect to Google OAuth
    
    Browser->>Google: GET oauth2/v2/auth
    Google->>Browser: Show Google Login Page
    
    User->>Google: Enter email and password
    Google->>Google: Verify credentials
    Google->>Browser: Redirect to /authorize?code=ABC123
    
    Browser->>Flask: GET /authorize?code=ABC123
    Flask->>Google: Exchange code for access token
    Google->>Flask: Return token + userinfo
    
    Flask->>Flask: Extract user data
    Flask->>DB: SELECT FROM users WHERE google_id
    
    alt User exists
        DB->>Flask: Return user data
        Flask->>DB: UPDATE user info
    else User does not exist
        DB->>Flask: Return null
        Flask->>DB: INSERT INTO users
    end
    
    Flask->>Flask: Create session cookie
    Flask->>Browser: Set-Cookie session data
    Flask->>Browser: Redirect to /chat
    
    Browser->>Flask: GET /chat with session cookie
    Flask->>Flask: Check login_required
    Flask->>Flask: User in session - Yes
    Flask->>Browser: Render chat.html with user data
```

---

## 🛡️ Authentication Guard Flow

```mermaid
flowchart TD
    Start([User requests protected route]) --> Decorator[login_required decorator runs]
    
    Decorator --> CheckSession{Is user in session?}
    
    CheckSession -->|No| Flash[Flash warning message]
    Flash --> RedirectHome[Redirect to home]
    RedirectHome --> ShowLogin[Show login page]
    
    CheckSession -->|Yes| ExtractUser[Extract user from session]
    ExtractUser --> RunFunction[Execute route function]
    RunFunction --> ReturnResponse[Return page or data to user]
    
    style CheckSession fill:#ff6b6b
    style RunFunction fill:#51cf66
    style RedirectHome fill:#ffd93d
```

---

## 🔄 Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> NoSession: User visits site
    
    NoSession --> Authenticating: Click Sign in
    Authenticating --> OAuthFlow: Redirect to Google
    OAuthFlow --> Authenticating: Google callback
    Authenticating --> SessionCreated: Create session cookie
    
    SessionCreated --> Active: User logged in
    
    Active --> Active: Browse pages
    Active --> Active: Send messages
    Active --> Active: Close and reopen browser
    
    Active --> NoSession: Click logout
    Active --> NoSession: Session expires
    Active --> NoSession: Clear cookies
    
    NoSession --> [*]
```

---

## 📡 API Chat Request Flow

```mermaid
flowchart TD
    Start([User sends message]) --> Frontend[Frontend JavaScript]
    Frontend --> PrepareData[Prepare request data]
    PrepareData --> SendRequest[POST to api chat]
    
    SendRequest --> FlaskReceives[Flask receives request]
    FlaskReceives --> CheckAuth{login_required check}
    
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
flowchart TD
    A[Get user info from Google] --> B{Check if user exists}
    
    B -->|Query| C[SELECT FROM users WHERE google_id]
    
    C -->|Found| D[UPDATE users SET email name picture]
    C -->|Not Found| E[INSERT INTO users]
    
    D --> G[Return user_id]
    E --> F[Get newly created user_id]
    F --> G
    
    G --> H[Create session cookie]
    H --> I[Redirect to chat]
    
    style D fill:#4dabf7
    style E fill:#51cf66
    style H fill:#ffd93d
```

---

## 🎯 Route Protection Mechanism

```mermaid
flowchart TD
    A1[Landing page route] --> NoAuth[Accessible to everyone]
    A2[Login route] --> NoAuth
    A3[Authorize route] --> NoAuth
    
    B1[Chat interface route] --> C{session user exists?}
    B2[Settings page route] --> C
    B3[API chat route] --> C
    B4[API conversations route] --> C
    B5[Logout route] --> C
    
    C -->|Yes| Allow[Allow access]
    C -->|No| Block[Redirect to home]
    
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
    A[User authenticates via Google] --> B[Flask receives user info]
    B --> C[Create session dictionary]
    C --> D[Set session user data]
    
    D --> E[Serialize to JSON]
    E --> F[Encrypt with SECRET_KEY]
    F --> G[Base64 encode]
    
    G --> H[Set-Cookie header]
    H --> I[Browser stores cookie]
    I --> J[Cookie sent with every request]
    
    J --> K[Flask receives Cookie header]
    K --> L[Decode Base64]
    L --> M[Decrypt with SECRET_KEY]
    M --> N[Deserialize JSON]
    N --> O[session user available in Python]
    
    O --> P{Route needs auth?}
    P -->|Yes| Q[login_required checks session]
    P -->|No| R[Execute route normally]
    
    style D fill:#4dabf7
    style F fill:#ffd93d
    style I fill:#51cf66
    style O fill:#51cf66
```

---

## 🔄 User Journey Map

```mermaid
journey
    title First-Time User Authentication Journey
    section Discovery
      Visit app URL: 5: User
      See landing page: 5: User
      Read about features: 4: User
    section Authentication
      Click Sign in with Google: 5: User
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
      Reopen app: 5: User
      Still logged in: 5: System
      Continue chatting: 5: User
```

---

## 🔐 Security Layers

```mermaid
flowchart TB
    A[Google verifies user identity] --> B[Session data encrypted]
    B --> C[login_required decorator]
    C --> D[User lookup by google_id]
    D --> E[Verify user owns resources]
    E --> F[Secure Access Granted]
    
    style F fill:#51cf66
    style A fill:#4285f4
    style B fill:#ffd93d
    style C fill:#ff6b6b
```

---

## 🎭 With vs Without Authentication

```mermaid
flowchart TD
    subgraph Without["Without Auth - Insecure"]
        N1[Anyone can access chat]
        N1 --> N2[No user identification]
        N2 --> N3[All conversations shared]
        N3 --> N4[No privacy]
        N4 --> N5[Security risk]
    end
    
    subgraph With["With Auth - Your App"]
        Y1[Must login to access chat]
        Y1 --> Y2[User identified by google_id]
        Y2 --> Y3[Personal conversations only]
        Y3 --> Y4[Data privacy maintained]
        Y4 --> Y5[Secure and private]
    end
    
    style N5 fill:#ff6b6b
    style Y5 fill:#51cf66
```

---

## 🧪 Testing Authentication

```mermaid
flowchart TD
    Start([Start Testing]) --> Test1[Open incognito window]
    
    Test1 --> Test2[Try accessing chat directly]
    Test2 --> Check1{Redirected to home?}
    Check1 -->|Yes| Pass1[Test 1 Passed]
    Check1 -->|No| Fail1[Auth not working]
    
    Pass1 --> Test3[Click Sign in with Google]
    Test3 --> Test4[Complete Google login]
    Test4 --> Check2{Redirected to chat?}
    Check2 -->|Yes| Pass2[Test 2 Passed]
    Check2 -->|No| Fail2[OAuth not working]
    
    Pass2 --> Test5[Check session cookie in DevTools]
    Test5 --> Check3{Cookie exists?}
    Check3 -->|Yes| Pass3[Test 3 Passed]
    Check3 -->|No| Fail3[Session not created]
    
    Pass3 --> Test6[Send a chat message]
    Test6 --> Check4{Message sent successfully?}
    Check4 -->|Yes| Pass4[Test 4 Passed]
    Check4 -->|No| Fail4[API auth issue]
    
    Pass4 --> Test7[Click logout]
    Test7 --> Check5{Session cleared?}
    Check5 -->|Yes| Pass5[All Tests Passed]
    Check5 -->|No| Fail5[Logout not working]
    
    Fail1 --> Debug[Check login_required]
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

## 📊 Login to First Message Flow

```mermaid
flowchart TD
    A[User clicks login] --> B[login route]
    B --> C[Redirect to Google]
    C --> D[Google authenticates]
    D --> E[authorize callback]
    
    E --> F[Exchange code for token]
    F --> G[Get user info]
    G --> H[Query database]
    
    H --> I{User exists?}
    I -->|No| J[INSERT INTO users]
    I -->|Yes| K[UPDATE users]
    
    J --> L[Get user_id]
    K --> L
    
    L --> M[Create session]
    M --> N[Redirect to chat]
    N --> O[Load chat interface]
    
    O --> P[User types message]
    P --> Q[POST to api chat]
    Q --> R[login_required check]
    R --> S[Get user from session]
    S --> T[Get user_id from DB]
    T --> U[Create or get conversation_id]
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

## 🎯 Authentication System Overview

```mermaid
mindmap
  root((Authentication System))
    Google OAuth
      login starts flow
      authorize receives callback
      Exchange code for token
      Get user info
    Session Management
      Encrypted cookie
      session user object
      Persists across requests
      Cleared on logout
    Route Protection
      login_required decorator
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

## 📝 Summary

```mermaid
flowchart LR
    A[Google OAuth] --> B[Session Cookie]
    B --> C[login_required]
    C --> D[Database]
    D --> E[Authenticated Access]
    
    style A fill:#4285f4
    style B fill:#ffd93d
    style C fill:#ff6b6b
    style D fill:#51cf66
    style E fill:#a78bfa
```

---

## 🎨 Key Points

**These flowcharts visually explain your authentication system:**

- ✅ Complete OAuth flow from login to chat
- ✅ Session management and cookies
- ✅ Route protection with decorators
- ✅ Database operations during auth
- ✅ Security layers and validation
- ✅ Testing procedures step-by-step
- ✅ User journey from discovery to return visits

**All diagrams use proper Mermaid syntax and should render correctly on GitHub!** 🚀

---

## 💡 Tips for Viewing

1. **Best view:** On GitHub - diagrams render automatically
2. **VS Code:** Install "Markdown Preview Mermaid Support" extension
3. **Local:** Use any Mermaid-compatible Markdown viewer

**GitHub will render all these diagrams beautifully!** ✨

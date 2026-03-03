# Flask Workshop – Quick Teaching Notes

Goal: Simple notes you can glance at while teaching. Short, clear, and focused only on what you need **tomorrow**.

---

## 1. What to Say About Flask (3–5 minutes)

### What is Flask?
- Flask is a small Python tool for building websites and APIs.
- It lets Python code respond to URLs like `/`, `/login`, `/chat`.
- You control everything: what each page does, what data is saved, and how the app behaves.

### Why are we using Flask today?
- Easy to learn if you know basic Python.
- Very fast to build a working project (good for hackathons and college projects).
- Used in real companies, so what you learn is useful later.

### One‑sentence pitch you can say
> "Flask is a simple Python framework that lets us turn Python code into real web apps and AI tools very quickly."

---

## 2. What Students Need Installed

Tell them to check these quickly:

1. **Python 3**
   - Run in terminal:
     ```bash
     python --version
     # or
     python3 --version
     ```

2. **pip** (comes with Python)
   - Check:
     ```bash
     pip --version
     ```

3. **Code editor**
   - VS Code is enough.

4. **Terminal**
   - Command Prompt / PowerShell / Terminal app.

You can say: "If these four are working, you are ready." 

---

## 3. Commands to Start the Project

You can show these step‑by‑step and ask everyone to follow.

### Step 1: Create a folder
```bash
mkdir flask-ai-workshop
cd flask-ai-workshop
```

### Step 2: Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
(Explain: "This keeps this project’s Python packages separate from other projects.")

### Step 3: Install needed packages
```bash
pip install flask authlib requests python-dotenv
```
(Explain briefly:
- `flask` → web framework
- `authlib` → Google login
- `requests` → call AI APIs
- `python-dotenv` → read secrets from `.env` file
)

### Step 4: Save dependencies
```bash
pip freeze > requirements.txt
```

---

## 4. First Flask App (You Can Live‑Code This)

Create `app.py` in the project folder:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flask 👋</h1>"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### What to explain in simple words
- `from flask import Flask` → "We are importing the Flask class from the flask package."
- `app = Flask(__name__)` → "We create our web application object called `app`."
- `@app.route("/")` → "When someone opens the home page `/`, run the function below."
- `home()` → "This function decides what to show on the page. Here we just send simple HTML text."
- `app.run(...)` → "This starts a small web server on our machine so we can test the app."

### How to run
```bash
python app.py
```
Then open: `http://localhost:5000`

Tell them: "If you see ‘Hello from Flask’, your setup works."

---

## 5. Simple Flask vs Django vs FastAPI (1–2 minutes)

Use this when someone asks "Why not Django/FastAPI?" – keep it short.

- **Flask**
  - Very small and flexible.
  - Good for learning, small–medium projects, APIs, hackathons.
  - You decide which database, which auth, which frontend.

- **Django**
  - Big and batteries‑included.
  - Has admin panel, built‑in auth, ORM and more.
  - Good for large, structured projects, but heavier for beginners.

- **FastAPI**
  - Designed for very fast APIs.
  - Great when you need high performance and async.
  - A bit more advanced than Flask for complete beginners.

One line to say:
> "We use Flask today because it’s easier to understand line‑by‑line and fast to build something useful in 2 hours."

---

## 6. What You Actually Need Tomorrow

This is the **minimal teaching flow** you can follow.

1. **Intro (5 min)**
   - What is Flask?
   - Why Flask for this project/hackathons.

2. **Setup (10–15 min)**
   - Create folder, venv, install packages.
   - Run the simple `app.py` and show it works.

3. **Move to Real Project (rest of time)**
   - Add:
     - Google login route
     - Simple SQLite usage
     - AI chat route using Groq
     - Frontend page that calls the chat route

For the intro, **this file plus your professional guide are enough**. 
You can:
- Use this file as your "talking script".
- Use `FLASK_WORKSHOP_GUIDE.md` for deeper technical details if someone asks.

---

## 7. Talking Style Tips

- Use short sentences.
- Avoid heavy words like "WSGI", "microservices", "asynchronous" in the intro.
- Focus on:
  - "This is what Flask does."
  - "This is why we chose it."
  - "This is how you start."

If someone wants deeper details, you can open the professional guide and show them.

---

**End of quick notes – meant for fast reading before and during the workshop.**

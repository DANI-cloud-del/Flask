from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello from Flask!</p>"

@app.route("/Home")
def home():
    return "<p>Welcome to the Home Page!</p>"

if __name__ == "__main__":
    app.run(debug=True,port=5001)

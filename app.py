from flask import Flask, redirect, request, session, render_template
from flask_session import Session
# from flask_session.__init__ import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

@app.route('/')
def initiate():
    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return 'From sign up'

@app.route('/logout')
def logout():
    return redirect('/login')
if __name__=="__main__":
    app.run(debug=True)

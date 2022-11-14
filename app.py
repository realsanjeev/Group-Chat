from flask import Flask, redirect, request, session
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
    print('-'*77)
    session['logged_in'] = True
    print (type(session.get('logged_in')))
    print('-'*77)
    return('FRom login redirect')

@app.route('/signup')
def signup():
    return 'From sign up'

@app.route('/logout')
def logout():
    return redirect('/login')
if __name__=="__main__":
    app.run(debug=True)

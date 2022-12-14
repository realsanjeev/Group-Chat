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
    return render_template('login.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('user.txt', 'w') as f:
            f.write(username)
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    return redirect('/login')
if __name__=="__main__":
    app.run(debug=True)

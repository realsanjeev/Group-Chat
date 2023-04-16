import sqlite3
from flask import Flask, redirect, request, session, render_template, url_for
from flask_session import Session
# from flask_session.__init__ import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

conn = sqlite3.connect("myDatabase.sqlite", check_same_thread=False)
db = conn.cursor()

def is_registered(username:str, email:str):
    flag=False
    get_record_by_email = db.execute("""SELECT id from user WHERE username=?""", (username,)).fetchone()
    get_record_by_username = db.execute(""""SELECT id FROM userinfo WHERE email=?""", (email,)).fetchone()
    if get_record_by_email:
        return render_template("sorry.html", message=f"User with email {email} already exist....")
    elif get_record_by_username:
        return render_template("sorry.html", message=f"Username: {username} is already taken")
    return flag

def register_user(user: dict):
    """
    Register the user in database

    Args:
        user: dict -> keys passed {"firstname": , "middlename":, "lastname":, "dob":
                                    "username": , "password", "email", "gender"}
    Return:
        render_template(sucess) if user is sucessfully saved
        render_template(sorry) if user cannot be saved
    """
    try:
        db.execute("""
                    INSERT INTO user (username, password) VALUES (?, ?)""", (user["username"], user["password"]))
        userid = db.execute("""SELECT id FROM user WHERE username=?""", (user["username"],)).fetchone()[0]
        db.execute("""
            INSERT INTO userinfo (user_id, firstName, middlename, lastname, gender, email, dob)
            values (?,?,?,?,?,?,?)""", (userid, user["firstname"], user["middlename"], user["lastname"], user["gender"], user["email"], user["dob"]))
        conn.commit()
    except sqlite3.Error as err:
        print("Error is: ", err)
        return render_template("sorry.html", message=err)


@app.route('/')
def initiate():
    return redirect(url_for("home"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if session:
        return redirect("/home")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        # check in database
        record = db.execute("""
                            SELECT * FROM user WHERE
                            username=? AND password=?""", (username, password)).fetchone()

        print(f"Record: {record}")
        if not record:
            return render_template("sorry.html", message="Either username or password mismatch")
        else: 
            # if sucessful assign session to user
            session["user_id"] = record[0] #record=(id, username, password)
        with open('user.txt', 'a') as f:
            f.write(username)
            f.write(password)
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    if not session:
        return redirect(url_for("login"))
    return render_template("indexx.html", myid=session["user_id"])

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if session:
        return redirect("/home")
    # creating dict for storing user information
    user = dict()
    if request.method == 'POST':
        user["username"] = request.form.get('username')
        user["firstname"] = request.form.get('firstname')
        user["middlename"] = request.form.get('middlename')
        user["lastname"] = request.form.get('lastname')
        user["email"] = request.form.get('email')
        user["password"] = request.form.get('password')
        user["dob"] = request.form.get('dob')
        user["gender"] = request.form.get('gender')

        # Checking if username or email already exist or not
        status = is_registered(username=user["username"], email=user["email"])
        txt = f"""username: {user["username"]}
          firstname:{user["firstname"]} 
          lastname: {user["lastname"]} 
          password: {user["password"]}
            dob: {user["dob"]} email: {user["email"]}
            gender: {user["gender"]}"""
        with open('sign.txt', 'a') as fp:
            fp.write(txt)
        register_user(user=user)
        return render_template("success.html", title="Register Sucessful!!!")
    else:
        # it is done so that when user goes to /signup in url
        return render_template("signup.html")

@app.route("/terms-and-conditions")
def display_terms_condition():
    return render_template("terms_privacy.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/login')
if __name__=="__main__":
    app.run(debug=True)

import sqlite3
from flask import (Flask, redirect, 
                    request, session, 
                    render_template, url_for)
from flask_session import Session

from database_handler import MyDatabase
# from flask_session.__init__ import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

database_conn = MyDatabase("myDatabase.sqlite")

@app.route('/')
def initiate() -> redirect:
    """
    Redirect the user to the `home` page of the application.

    Returns:
        redirect - the response to redirect the user to the `home` page.
    """
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

        print(f"[INFO] Record: {record}")
        if not record:
            return render_template("login.html", message="Either username or password mismatch")
        else:
            # if sucessful assign session to user
            session["user_id"] = record[0] #record=(id, username, password)
        # with open('user.txt', 'a') as fp:
        #     fp.write(username)
        #     fp.write(password)
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if session:
        return redirect("/home")
    if request.method == 'POST':
        # creating dict for storing user information
        user = {}
        user["username"] = request.form.get('username')
        user["firstname"] = request.form.get('firstname')
        user["middlename"] = request.form.get('middlename')
        user["lastname"] = request.form.get('lastname')
        user["email"] = request.form.get('email')
        user["password"] = request.form.get('password')
        user["dob"] = request.form.get('dob')
        user["gender"] = request.form.get('gender')

        # Checking if username or email already exist or not
        status = database_conn.is_registered(username=user["username"], email=user["email"])
        # txt = f"""username: {user["username"]}
        #   firstname:{user["firstname"]}
        #   lastname: {user["lastname"]}
        #   password: {user["password"]}
        #     dob: {user["dob"]} email: {user["email"]}
        #     gender: {user["gender"]}"""
        # with open('sign.txt', 'a') as fp:
        #     fp.write(txt)
        database_conn.register_user(user=user)
        return render_template("success.html", title="Register Sucessful!!!")

    # it is done so that when user goes to /signup in url
    return render_template("signup.html")

@app.route("/terms-and-conditions")
def display_terms_condition():
    """
    Displays the terms and conditions HTML template.

    Returns:
        A rendered HTML template for terms and conditions.
    """
    return render_template("terms_privacy.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    """
    Logs out the user by clearing the session.

    Returns:
        A redirect to the login page.
    """
    session.clear()
    return redirect(url_for("login"))


@app.route("/home")
def home():
    print("[INFO] Routing to /home of url")
    print(session)
    if not session:
        return redirect(url_for("login"))
    profile = database_conn.get_user_profile(session["user_id"])

    return render_template("indexx.html", user=profile)

@app.route("/profile")
def profile_user():
    if not session:
        return redirect(url_for("login"))
    print(f"[INFO] Issuue: construct /profile/<username>")
    profile = database_conn.get_user_profile(session["user_id"])
    return render_template("profile.html", user=profile)


@app.route("/group_ops", methods=["GET", "POST"])
def group_ops():
    if not session:
        return redirect(url_for("login"))
    groups = dict()
    new_group = group_name = None
    community = database_conn.get_current_connection(user_id=session["user_id"])
    print("@"*10, community)
    groups["community"] = community
    if request.method == "POST":
        new_group = request.form.get("create-community")
        group_name = request.form.get("join-community")

    if new_group:
        database_conn.create_group(user_id=session["user_id"], group_name=new_group)

    if group_name:
        print("-"*100, group_name)
        database_conn.join_group(user_id=session["user_id"], group_name=group_name)

    return render_template("group_ops.html", groups=groups)

@app.route("/group/<group_name>", methods=["GET", "POST"])
def group_discussion(group_name):
    if not session:
        return redirect(url_for("login"))
    if database_conn.check_group(group=group_name) is False:
        return render_template("sorry.html",
                                message=f"Group '{group_name}' not found.")
    community = database_conn.get_current_connection(user_id=session["user_id"])

    # community returns list of tuple. So comapre tuple with list to check
    if tuple(group_name) not in community:
        print(f"group_name: {group_name} and community: {community}")

        return render_template("sorry.html",
                                message=f"You arenot member of Group '{group_name}'. \
                                Please join group {group_name} to view this forum.")

    forum = {
        "group_name": group_name,
        "posts": []
    }

    posts = get_posts(user_id=session["user_id"], group=group_name)
    if posts is not None:
        forum["posts"] = posts

    if request.method == "POST":
        new_post = request.form.get("create-post")
        print(new_post)
        create_post(user_id=session["user_id"], group=group_name, post=new_post)

    return render_template("discussion.html", forum=forum)

def create_post(user_id, group, post):
    print("[INFO] Creating Post")
    try:
        group_id = db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group,)
        ).fetchone()
        db.execute("""
                    INSERT INTO posts 
                    (content, user_id, group_id) 
                    VALUES (?, ?, ?)""", (post, user_id, group_id[0]))
        conn.commit()
    except sqlite3.Error:
        return render_template("sorry.html",
                                message=f"Failed to create post in group {group}")


def get_posts(user_id, group):
    try:
        group_id = db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group,)
        ).fetchone()
        posts = db.execute("""SELECT user.username, posts.content, posts.doc
                FROM user JOIN posts ON user.id = posts.user_id
                WHERE group_id = (?)""",
                (group_id[0],)).fetchmany(5)
        print("[INFO] getting all post for group....")
        return posts

    except sqlite3.Error as err:
        print(f"[INFO] Error wile retriving posts: {err}")
        return None

# add url route in web application
app.add_url_rule('/signout', 'logout', logout)

# @app.route("/group")
if __name__=="__main__":
    app.run(debug=True)

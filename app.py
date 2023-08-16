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

def is_registered(username: str, email: str):
    """
    Check if a user is already registered in the system, using their username and email address.

    Args:
        username (str): The username of the user to check.
        email (str): The email address of the user to check.

    Returns:
        If the user is already registered with the given username or email,\
        a `sorry.html` page with an error \
        message is rendered. Otherwise, the function returns False.
    """
    flag = False
    get_record_by_email = db.execute("""
                                SELECT id 
                                FROM user 
                                WHERE username=?""", (username,)).fetchone()
    get_record_by_username = db.execute("""SELECT user_id
                                            FROM userinfo 
                                            WHERE email=?""", (email,)).fetchone()
    if get_record_by_email:
        return render_template("sorry.html",
                                message=f"User with email {email} already exists.")
    if get_record_by_username:
        return render_template("sorry.html",
                                message=f"Username '{username}' is already taken.")
    return flag


def get_user_profile(user_id: int):
    """
    Get the user profile for a given user ID.

    Args:
        user_id (int): The ID of the user to retrieve the profile for.

    Returns:
        dict: A dictionary containing the user's profile information.
            The dictionary has the following keys:
            - user_id (int): The ID of the user.
            - username (str): The username of the user.
            - firstname (str): The first name of the user.
            - middlename (str): The middle name of the user.
            - lastname (str): The last name of the user.
            - gender (str): The gender of the user.
            - dob (str): The date of birth of the user.
            - email (str): The email address of the user.
            - name (str): The full name of the user, including first name,
                          middle name, and last name.
    """
    user_profile = dict()
    user_profile["user_id"] = user_id
    get_record_by_username = db.execute("""SELECT *
                                            FROM userinfo 
                                            WHERE 
                                            user_id=?""", (user_id,)).fetchone()
    profile_username = db.execute("""
                            SELECT username FROM user 
                            WHERE
                            id=?""", (user_id,)).fetchone()[0]

    user_profile["username"] = profile_username
    fields = ["firstname", "middlename", "lastname", "gender", "dob", "email"]
    for index, attribute in enumerate(fields):
        user_profile[attribute] = get_record_by_username[index+1]
    user_profile["name"] = user_profile["firstname"] + " "  \
                            + user_profile["middlename"] + " "  \
                            + user_profile["lastname"]

    return user_profile

def register_user(user: dict):
    """
    Register the user in the database with their personal information and login credentials.

    Args:
        user (dict): A dictionary containing user information with keys "firstname", "middlename",
                     "lastname", "dob", "username", "password", "email", and "gender".

    Returns:
        If the user is successfully saved, this function returns a success message rendered by
        the Flask template. If the user cannot be saved, it returns a sorry message rendered by the
        Flask template.
    """
    try:
        db.execute("""
                    INSERT INTO user 
                    (username, password) 
                    VALUES (?, ?)""", (user["username"], user["password"]))
        userid = db.execute("""SELECT id
                                FROM user 
                                WHERE username=?""", (user["username"],)).fetchone()[0]
        db.execute("""
            INSERT INTO userinfo 
            (user_id, firstName, middlename, lastname, gender, email, dob)
            values (?,?,?,?,?,?,?)
            """, (userid, user["firstname"], user["middlename"], user["lastname"], \
                  user["gender"], user["email"], user["dob"]))
        conn.commit()
        return render_template("success.html")
    except sqlite3.Error as err:
        print("Error is: ", err)
        return render_template("sorry.html", message=err)


def create_group(user_id: int, group_name: str):
    """
    Create a new group and add the specified user as a member.

    Args:
        user_id (int): The ID of the user creating the group.
        group_name (str): The name of the group to be created.

    Returns:
        None.

    Raises:
        TemplateError: If the group already exists.

    """
    # Check if group already exists
    group_id = db.execute(
        """SELECT id FROM user_group WHERE name = ?""", (group_name,)
    ).fetchone()

    if group_id:
        return render_template("sorry.html",
            message=f"{group_name} already exists. Please choose a different \
                name or join the existing group."
        )

    # Create new group and add user as member
    db.execute("""INSERT INTO user_group (name) VALUES (?)""", (group_name,))
    group_id = db.execute(
        """SELECT id FROM user_group WHERE name = ?""", (group_name,)
    ).fetchone()[0]
    db.execute(
        """INSERT INTO group_member 
        (user_id, group_id) 
        VALUES (?, ?)""",
        (user_id, group_id),
    )
    conn.commit()

def join_group(user_id, group_name):
    """
    Join Group that already exist

    Args:
        user_id (int): The ID of the user creating the group.
        group_name (str): The name of the group to be created.

    Returns:
        None.

    Raises:
        TemplateError: If the group already exists.

    """
    # Check if group already exists
    group_id = db.execute(
        """SELECT id FROM user_group WHERE name = ?""", (group_name,)
    ).fetchone()

    if not group_id:
        return render_template("sorry.html",
            message=f"{group_name} already exists. Please choose a different \
                name or join the existing group."
        )

    # Add user as member in given Group
    db.execute(
        """INSERT INTO group_member 
        (user_id, group_id) 
        VALUES (?, ?)""",
        (user_id, group_id),
    )
    conn.commit()


def get_current_connection(user_id: int):
    """
    Retrieve the names of the groups that a user with the given `user_id` is a member of.

    Args:
        user_id: int - the id of the user to retrieve the group membership for.

    Returns:
        List of tuple - the names of the groups that the \
            user with the given `user_id` is a member of.
    """
    groups_name = db.execute("""
                        SELECT user_group.name
                        FROM group_member 
                        JOIN user_group ON user_group.id = group_member.group_id
                        WHERE group_member.user_id=?
                    """, (user_id,)).fetchall()

    return groups_name

def check_group(group):
    group_record = db.execute(
        """SELECT id FROM user_group WHERE name = ?""", (group,)
    ).fetchone()
    if group_record:
        return True
    else:
        return False

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
        status = is_registered(username=user["username"], email=user["email"])
        # txt = f"""username: {user["username"]}
        #   firstname:{user["firstname"]}
        #   lastname: {user["lastname"]}
        #   password: {user["password"]}
        #     dob: {user["dob"]} email: {user["email"]}
        #     gender: {user["gender"]}"""
        # with open('sign.txt', 'a') as fp:
        #     fp.write(txt)
        register_user(user=user)
        return render_template("success.html", title="Register Sucessful!!!")
    else:
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
    profile = get_user_profile(session["user_id"])

    return render_template("indexx.html", user=profile)

@app.route("/profile")
def profile_user():
    if not session:
        return redirect(url_for("login"))
    print(f"[INFO] Issuue: construct /profile/<username>")
    profile = get_user_profile(session["user_id"])
    return render_template("profile.html", user=profile)


@app.route("/group_ops", methods=["GET", "POST"])
def group_ops():
    if not session:
        return redirect(url_for("login"))
    groups = dict()
    new_group = group_name = None
    community = get_current_connection(user_id=session["user_id"])
    print("@"*10, community)
    groups["community"] = community
    if request.method == "POST":
        new_group = request.form.get("create-community")
        group_name = request.form.get("join-community")

    if new_group:
        create_group(user_id=session["user_id"], group_name=new_group)

    if group_name:
        join_group(user_id=session["user_id"], group_name=group_name)

    return render_template("group_ops.html", groups=groups)

@app.route("/group/<group_name>", methods=["GET", "POST"])
def group_discussion(group_name):
    if not session:
        return redirect(url_for("login"))
    if check_group(group=group_name) is False:
        return render_template("sorry.html",
                                message=f"Group '{group_name}' not found.")
    community = get_current_connection(user_id=session["user_id"])

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

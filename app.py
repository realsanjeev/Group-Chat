from flask import Flask, redirect, request, session, render_template, url_for
from flask_session import Session
from src.database_handler import UserDatabase, GroupDatabase, PostDatabase

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

user_db = UserDatabase("myDatabase.sqlite")
group_db = GroupDatabase("myDatabase.sqlite")
post_db = PostDatabase("myDatabase.sqlite")


@app.route("/")
def initiate() -> redirect:
    """
    Redirect the user to the `home` page of the application.

    Returns:
        redirect - the response to redirect the user to the `home` page.
    """
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session:
        return redirect("/home")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # check in database
        record = user_db.db.execute(
            "SELECT * FROM user WHERE username=? AND password=?", (username, password)
        ).fetchone()

        print(f"[INFO] Record: {record}")
        if not record:
            return render_template(
                "account/login.html", message="Either username or password mismatch"
            )
        else:
            # if successful assign session to user
            session["user_id"] = record[0]  # record = (id, username, password)
        return redirect(url_for("home"))
    else:
        return render_template("account/login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session:
        return redirect("/home")
    if request.method == "POST":
        # creating dict for storing user information
        user = {
            "username": request.form.get("username"),
            "firstname": request.form.get("firstname"),
            "middlename": request.form.get("middlename"),
            "lastname": request.form.get("lastname"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
        }

        # Checking if username or email already exist or not
        status = user_db.is_registered(username=user["username"], email=user["email"])
        if status:
            return status  # render_template("sorry.html", message=status)

        user_db.register_user(user=user)
        return render_template("success.html", title="Register Successful!!!")

    return render_template("account/signup.html")


@app.route("/terms-and-conditions")
def display_terms_condition():
    """
    Displays the terms and conditions HTML template.

    Returns:
        A rendered HTML template for terms and conditions.
    """
    return render_template("public/terms_privacy.html")


@app.route("/logout", methods=["GET", "POST"])
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
    profile = user_db.get_user_profile(session["user_id"])

    return render_template("home.html", user=profile)


@app.route("/profile")
def profile_user():
    if not session:
        return redirect(url_for("login"))
    profile = user_db.get_user_profile(session["user_id"])
    return render_template("account/profile.html", user=profile)


@app.route("/group_ops", methods=["GET", "POST"])
def group_ops():
    if not session:
        return redirect(url_for("login"))
    groups = dict()
    new_group = group_name = None
    community = group_db.get_current_connection(user_id=session["user_id"])
    groups["community"] = community
    if request.method == "POST":
        new_group = request.form.get("create-community")
        group_name = request.form.get("join-community")

    if new_group:
        group_db.create_group(user_id=session["user_id"], group_name=new_group)

    if group_name:
        group_db.join_group(user_id=session["user_id"], group_name=group_name)

    return render_template("group_ops.html", groups=groups)


@app.route("/group/<group_name>", methods=["GET", "POST"])
def group_discussion(group_name):
    if not session:
        return redirect(url_for("login"))
    if group_db.check_group(group=group_name) is False:
        return render_template("sorry.html", message=f"Group '{group_name}' not found.")
    community = group_db.get_current_connection(user_id=session["user_id"])

    if group_name not in [group[0] for group in community]:
        return render_template(
            "sorry.html",
            message=f"You are not member of Group '{group_name}'. \
                               Please join group {group_name} to view this forum.",
        )

    forum = {"group_name": group_name, "posts": []}
    if request.method == "POST":
        new_post = request.form.get("create-post")
        post_db.create_post(user_id=session["user_id"], group=group_name, post=new_post)
        return redirect(url_for("group_discussion", group_name=group_name))

    posts = post_db.get_posts(user_id=session["user_id"], group=group_name)
    if posts is not None:
        forum["posts"] = posts
        forum["posts"].reverse()

    return render_template("discussion.html", forum=forum)


app.add_url_rule("/signout", "logout", logout)

if __name__ == "__main__":
    app.run(debug=True)

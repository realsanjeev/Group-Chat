from flask import Flask, redirect, request, session, render_template, url_for, flash
from flask_session import Session
from src.database_handler import UserDatabase, GroupDatabase, PostDatabase
from src.utils import hash_password, verify_password, sanitize_input
from src.forms import LoginForm, SignupForm, CreateGroupForm, JoinGroupForm, CreatePostForm
from config import config
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])
Session(app)

# Initialize database handlers
user_db = UserDatabase("myDatabase.sqlite")
group_db = GroupDatabase("myDatabase.sqlite")
post_db = PostDatabase("myDatabase.sqlite")


def is_authenticated():
    """Check if user is authenticated."""
    return 'user_id' in session and session['user_id'] is not None


@app.route("/")
def initiate():
    """
    Redirect the user to the `home` page of the application.

    Returns:
        redirect - the response to redirect the user to the `home` page.
    """
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if is_authenticated():
        return redirect("/home")
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = sanitize_input(form.username.data)
        password = form.password.data

        # Check in database
        record = user_db.db.execute(
            "SELECT * FROM user WHERE username=?", (username,)
        ).fetchone()

        if not record:
            flash("Invalid username or password", "error")
            return render_template("account/login.html", form=form)
        
        # Verify password (record = (id, username, password_hash))
        if not verify_password(password, record[2]):
            flash("Invalid username or password", "error")
            return render_template("account/login.html", form=form)
        
        # Successful login - assign session to user
        session['user_id'] = record[0]
        session.permanent = True
        flash(f"Welcome back, {username}!", "success")
        return redirect(url_for("home"))
    
    return render_template("account/login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user registration."""
    if is_authenticated():
        return redirect("/home")
    
    form = SignupForm()
    
    if form.validate_on_submit():
        # Creating dict for storing user information
        username = sanitize_input(form.username.data)
        email = sanitize_input(form.email.data)
        
        # Check if username already exists
        existing_username = user_db.db.execute(
            "SELECT id FROM user WHERE username=?", (username,)
        ).fetchone()
        
        if existing_username:
            flash(f"Username '{username}' is already taken. Please choose a different username.", "error")
            return render_template("account/signup.html", form=form)
        
        # Check if email already exists
        existing_email = user_db.db.execute(
            "SELECT user_id FROM userinfo WHERE email=?", (email,)
        ).fetchone()
        
        if existing_email:
            flash(f"An account with email {email} already exists. Please use a different email or log in.", "error")
            return render_template("account/signup.html", form=form)
        
        # Create user dict
        user = {
            "username": username,
            "firstname": sanitize_input(form.firstname.data),
            "middlename": sanitize_input(form.middlename.data),
            "lastname": sanitize_input(form.lastname.data),
            "email": email,
            "password": hash_password(form.password.data),  # Hash the password
            "dob": form.dob.data.strftime("%Y-%m-%d"),
            "gender": form.gender.data,
        }

        # Register the user
        try:
            user_db.register_user(user=user)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("An error occurred during registration. Please try again.", "error")
            return render_template("account/signup.html", form=form)

    return render_template("account/signup.html", form=form)


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
    if is_authenticated():
        session.clear()
        flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/home")
def home():
    """Display the home page."""
    if not is_authenticated():
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    profile = user_db.get_user_profile(session["user_id"])
    
    # Get recent activity from user's groups
    community = group_db.get_current_connection(user_id=session["user_id"])
    recent_posts = []
    
    # Get recent posts from all groups (limit to 5 most recent)
    for group in community[:3]:  # Limit to first 3 groups
        posts = post_db.get_posts(group=group[0])
        if posts:
            recent_posts.extend([(group[0], post) for post in posts[:2]])
    
    return render_template("home.html", user=profile, groups=community, recent_posts=recent_posts)


@app.route("/profile")
def profile_user():
    """Display user profile."""
    if not is_authenticated():
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    profile = user_db.get_user_profile(session["user_id"])
    return render_template("account/profile.html", user=profile)


@app.route("/group_ops", methods=["GET", "POST"])
def group_ops():
    """Handle group operations (create/join)."""
    if not is_authenticated():
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    create_form = CreateGroupForm()
    join_form = JoinGroupForm()
    
    groups = dict()
    community = group_db.get_current_connection(user_id=session["user_id"])
    groups["community"] = community
    
    if request.method == "POST":
        # Check which form was submitted
        if 'create-submit' in request.form and create_form.validate_on_submit():
            new_group = sanitize_input(create_form.group_name.data)
            result = group_db.create_group(user_id=session["user_id"], group_name=new_group)
            if result is True:
                flash(f"Group '{new_group}' created successfully!", "success")
                return redirect(url_for("group_ops"))
            else:
                return result
        
        elif 'join-submit' in request.form and join_form.validate_on_submit():
            group_name = sanitize_input(join_form.group_name.data)
            result = group_db.join_group(user_id=session["user_id"], group_name=group_name)
            if result is True:
                flash(f"Successfully joined group '{group_name}'!", "success")
                return redirect(url_for("group_ops"))
            elif result is False:
                flash(f"You are already a member of '{group_name}' or an error occurred.", "error")
            else:
                return result

    return render_template("group_ops.html", groups=groups, create_form=create_form, join_form=join_form)


@app.route("/group/<group_name>", methods=["GET", "POST"])
def group_discussion(group_name):
    """Display and handle group discussion."""
    if not is_authenticated():
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    if group_db.check_group(group=group_name) is False:
        flash(f"Group '{group_name}' not found.", "error")
        return redirect(url_for("group_ops"))
    
    community = group_db.get_current_connection(user_id=session["user_id"])

    if group_name not in [group[0] for group in community]:
        flash(f"You are not a member of Group '{group_name}'. Please join the group to view this forum.", "warning")
        return redirect(url_for("group_ops"))

    post_form = CreatePostForm()
    forum = {"group_name": group_name, "posts": []}
    
    if post_form.validate_on_submit():
        new_post = sanitize_input(post_form.content.data)
        result = post_db.create_post(content=new_post, user_id=session["user_id"], group=group_name)
        if result is True:
            flash("Post created successfully!", "success")
            return redirect(url_for("group_discussion", group_name=group_name))
        else:
            return result

    posts = post_db.get_posts(group=group_name)
    if posts is not None:
        # Enhance posts with like and comment data
        enhanced_posts = []
        for post in posts:
            post_data = {
                'username': post[0],
                'content': post[1],
                'date': post[2],
                'post_id': post[3],
                'like_count': post_db.get_like_count(post[3]),
                'comment_count': post_db.get_comment_count(post[3]),
                'user_has_liked': post_db.user_has_liked(post[3], session["user_id"]),
                'comments': post_db.get_comments(post[3])
            }
            enhanced_posts.append(post_data)
        forum["posts"] = enhanced_posts

    return render_template("discussion.html", forum=forum, post_form=post_form)


@app.route("/api/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    """Toggle like on a post via AJAX."""
    if not is_authenticated():
        return {"success": False, "error": "Not authenticated"}, 401
    
    try:
        is_liked = post_db.toggle_like(post_id, session["user_id"])
        like_count = post_db.get_like_count(post_id)
        return {
            "success": True,
            "is_liked": is_liked,
            "like_count": like_count
        }
    except Exception as e:
        logging.error(f"Error in like_post: {e}")
        return {"success": False, "error": str(e)}, 500


@app.route("/api/comment/<int:post_id>", methods=["POST"])
def add_comment_to_post(post_id):
    """Add a comment to a post via AJAX."""
    if not is_authenticated():
        return {"success": False, "error": "Not authenticated"}, 401
    
    try:
        data = request.get_json()
        comment_content = sanitize_input(data.get("content", "").strip())
        
        if not comment_content:
            return {"success": False, "error": "Comment cannot be empty"}, 400
        
        success = post_db.add_comment(post_id, session["user_id"], comment_content)
        
        if success:
            comment_count = post_db.get_comment_count(post_id)
            comments = post_db.get_comments(post_id)
            return {
                "success": True,
                "comment_count": comment_count,
                "comments": [
                    {
                        "username": c[0],
                        "content": c[1],
                        "timestamp": c[2]
                    } for c in comments
                ]
            }
        else:
            return {"success": False, "error": "Failed to add comment"}, 500
    except Exception as e:
        logging.error(f"Error in add_comment_to_post: {e}")
        return {"success": False, "error": str(e)}, 500


# Add URL rule alias for logout
app.add_url_rule("/signout", "logout", logout)

if __name__ == "__main__":
    app.run(debug=True)


import sqlite3
from flask_session import Session
from flask import Flask,render_template,request,redirect,session, url_for

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("announceMe.db", check_same_thread=False)
db = conn.cursor()
@app.route("/")
def index():
    return redirect("/login")

@app.route("/group",methods = ["GET","POST"])
def group():
    userName=session["userName"]
    if request.method == "GET":
        groupName=request.form.get("groupName")
        groupId=request.form.get("groupId")
        groups=db.execute("""SELECT grp.groupName, members.groupId 
                            FROM members 
                            INNER JOIN grp 
                            ON 
                            members.groupId = grp.groupId 
                            WHERE members.userName=? """, (userName,))
        return render_template("groups.html",groups=groups)
    else:
        if request.form.get("groupId"):
            checkRow = db.execute("SELECT * FROM members WHERE groupId=? AND userName=?", (groupId, userName))
            if len(checkRow)==0:
                return render_template("apology.html",message="Group Doesn't exist For you")
            else:
                session["groupId"] = request.form.get("groupId")
                return redirect("/posts")
        elif request.form.get("groupName"):#create group
            checksum = db.execute("SELECT * FROM grp WHERE groupName=?", (groupName,))
            if len(checksum)==0:
                db.execute("INSERT INTO grp (groupName) VALUES (?)", (groupName,))
                groupId=db.execute("SELECT groupId FROM grp WHERE groupName=?", (groupName,))
                db.execute("INSERT INTO members (groupId,userName) VALUES (?, ?)", (groupId[0]["groupId"], userName))
                return redirect("/group")
            else:
                return render_template("apology.html",message="Group already exists!!")
        elif request.form.get("groupToJoin"):#join group
            check = db.execute("SELECT * FROM grp WHERE groupName=?", (groupName,))
            if len(check) == 0:
                return render_template("apology.html",message="There is no such group to join")
            else:
                id = db.execute("SELECT groupId FROM grp where groupName=?", (groupName,))
                db.execute("INSERT INTO members (groupId,userName) VALUES (?, ?)", (groupId, userName))
                return redirect("/group")

@app.route("/posts",methods=["GET","POST"])
def posts():
    if request.method == "POST":
        if request.form.get("like"):
             likedBy=session["userName"]
             postId = request.form.get("like")
             tada = db.execute("SELECT * FROM liked WHERE postId=:postId AND likedBy=:likedBy", postId)
             if len(tada) == 0:
                 db.execute("INSERT INTO liked(postId,likedBy) VALUES (:postId,:likedBy)",postId=postId)
             else:
                 db.execute("DELETE FROM liked WHERE likedBy=:likedBy AND postId=:postId",postId=postId)
             return redirect("/posts")
        elif request.form.get("comment"):
            comment = request.form.get("comment")
            commentedPostId = request.form.get("commentedPostId")
            db.execute("INSERT INTO commented(postId,commentedBy,comment) VALUES (:postId,:commentedBy,:comment)",postId=commentedPostId,commentedBy=session["userName"],comment=comment)
            return redirect("/posts")
        elif request.form.get("comments"):
            postId = request.form.get("comments")
            comments = db.execute("SELECT commentedBy,comment FROM commented WHERE postId=:postId",postId=postId)
            return render_template("comments.html",comments=comments)
        elif request.form.get("post"):
            post = request.form.get("post")
            db.execute("INSERT INTO posts (postedBy,postedAt,groupId,post) VALUES (:postedBy,DateTime('now'),:groupId,:post)",postedBy=session["userName"],groupId=session["groupId"],post=post)
            return redirect("/posts")
    else:
        thisUserLikes = db.execute("SELECT postId FROM liked WHERE likedBy=:likedBy")
        likes = db.execute("SELECT COUNT(likedBy) numberOfLikes,postId FROM liked GROUP BY postId")
        posts = db.execute("SELECT postId,postedBy,postedAt,post FROM  posts  WHERE groupId=:groupId ORDER BY postedAt DESC",groupId=session["groupId"])
        return render_template("group.html",posts=posts,likes=likes,thisUserLikes=thisUserLikes)


@app.route("/login",methods=["GET","POST"])
def logIn():
    session.clear()
    if request.method == 'POST':
        userName = request.form.get("userName", None)
        password = request.form.get("password", None)
        if not userName or not password:
            return render_template("apology.html", message="Enter username and password field")
        rows = db.execute("SELECT * FROM user WHERE userName=? AND password=?",
                           (userName, password)).fetchone()
        if not rows:
            return redirect("/signup")
        session["userName"] = rows[0]
        return redirect("/group")
    else:
        return render_template("login.html")



@app.route("/logout")
def logOut():
    session.clear()
    return redirect("/login")



@app.route("/signup",methods=["GET","POST"])
def signUp():
    if request.method == "GET":
        return render_template("signUp.html")
    else:
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        userName = request.form.get("userName")
        password = request.form.get("password")
        if not firstName or not lastName or not userName or not password:
            return render_template("apology.html", message="Please fill in all fields to sign up")
        db.execute("SELECT userName FROM user WHERE userName = ?", (userName,))
        user = db.fetchone()
        if user is not None:
            return render_template("apology.html", message="Username already taken")
        else:
            db.execute("INSERT INTO user (firstName, lastName, userName, password) VALUES (?, ?, ?, ?)",
                       (firstName, lastName, userName, password))
            conn.commit()
            return render_template("success.html")




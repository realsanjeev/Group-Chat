@app.route("/group", methods=["GET", "POST"])
def group():
    userName = session["userName"]
    if request.method == "GET":
        groupName = request.form.get("groupName")
        groupId = request.form.get("groupId")
        groups = db.execute("""SELECT grp.groupName, members.groupId
                            FROM members 
                            INNER JOIN grp 
                            ON 
                            members.groupId = grp.groupId 
                            WHERE members.userName=? """, (userName,)).fetchall()
        print("="*100, '\n', groups, " TYPE: ", type(groups), '\n', "="*100)
        return render_template("groups.html", groups=groups)
    else:
        if request.form.get("groupId"):
            groupId = request.form.get("groupId")
            checkRow = db.execute("""SELECT * FROM members
                                    WHERE groupId=?
                                    AND 
                                    userName=?""", (groupId, userName))
            if not checkRow:
                return render_template("apology.html",
                                       message="Group Doesn't exist For you")

            else:
                session["groupId"] = request.form.get("groupId")
                return redirect("/posts")

        elif request.form.get("groupName"):  # create group
            groupName = request.form.get("groupName")
            print("*"*100, '\n', groupName, '\n', "*"*100)
            checksum = db.execute("""SELECT * FROM grp
                                    WHERE groupName=?""", (groupName,)).fetchone()
            if not checksum:
                db.execute(
                    "INSERT INTO grp (groupName) VALUES (?);", (groupName,))
                groupId = db.execute(
                    "SELECT groupId FROM grp WHERE groupName=?;", (groupName,)).fetchone()
                print("*"*100, '\n', groupId, " TYPE: ",
                      type(groupId), '\n', "*"*100)
                db.execute("""
                            INSERT INTO members (groupId, userName) 
                            VALUES (?, ?);""",
                           (int(groupId[0]), userName))

                return redirect("/group")

            else:
                return render_template("apology.html",
                                       message="Group already exists!!")

        elif request.form.get("groupToJoin"):  # join group
            groupName = request.form.get("groupToJoin")
            check = db.execute(
                "SELECT * FROM grp WHERE groupName=?", (groupName,))
            if not check:
                return render_template("apology.html",
                                       message="There is no such group to join")
            else:
                id = db.execute(
                    "SELECT groupId FROM grp where groupName=?", (groupName,)).fetchone()
                if not id:
                    return render_template("apology.html",
                                       message="There is no such group to join")
                db.execute(
                    "INSERT INTO members (groupId,userName) VALUES (?, ?)", (id[0], userName))
                return redirect("/group")


@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        if request.form.get("like"):
            likedBy = session["userName"]
            postId = request.form.get("like")
            tada = db.execute(
                "SELECT * FROM liked WHERE postId=? AND likedBy=?", (postId, likedBy))
            if not tada:
                db.execute(
                    "INSERT INTO liked(postId,likedBy) VALUES (?, ?)", (postId, likedBy))
            else:
                db.execute(
                    "DELETE FROM liked WHERE likedBy=? AND postId=?", (postId, likedBy))
            return redirect("/posts")
        elif request.form.get("comment"):
            comment = request.form.get("comment")
            commentedBy = session["userName"]
            commentedPostId = request.form.get("commentedPostId")
            postId = commentedPostId
            db.execute("""INSERT INTO commented(postId, commentedBy, comment)
                                        VALUES (?, ?, ?)""", (postId, commentedBy, comment))
            return redirect("/posts")
        elif request.form.get("comments"):
            postId = request.form.get("comments")
            comments = db.execute(
                "SELECT commentedBy,comment FROM commented WHERE postId=?", (postId))
            return render_template("comments.html",
                                   comments=comments)

        elif request.form.get("post"):
            post = request.form.get("post")
            postedBy = session["userName"]
            groupId = session["groupId"]
            db.execute("""INSERT INTO posts
                        (postedBy,postedAt,groupId,post) 
                        VALUES 
                        (?, DateTime('now'), ?, ?)""",
                       (postedBy, groupId, post))
            return redirect("/posts")
    else:
        likedBy = session["userName"]
        thisUserLikes = db.execute(
            "SELECT postId FROM liked WHERE likedBy=?", (likedBy,))
        likes = db.execute(
            "SELECT COUNT(likedBy) numberOfLikes,postId FROM liked GROUP BY postId")
        groupId=session["groupId"]
        posts_group = db.execute("""SELECT postId,postedBy,postedAt,post
                                FROM  posts  
                                WHERE groupId=?
                                ORDER BY postedAt DESC""", groupId).fetchall() ##
        print("!"*100, posts_group)
        
        
        
        
        
        
        
        
        #err
        return render_template("group.html",
                               posts=posts_group,
                               likes=likes,
                               thisUserLikes=thisUserLikes)
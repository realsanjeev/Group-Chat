import sqlite3
from flask import render_template
from src.logger import logging


class MyDatabase:
    def __init__(self, db_name, check_same_thread=False):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=check_same_thread)
        self.db = self.conn.cursor()


class UserDatabase(MyDatabase):
    def is_registered(self, username: str, email: str):
        flag = False
        get_record_by_email = self.db.execute(
            "SELECT id FROM user WHERE username=?", (username,)
        ).fetchone()
        get_record_by_username = self.db.execute(
            "SELECT user_id FROM userinfo WHERE email=?", (email,)
        ).fetchone()
        if get_record_by_email:
            return render_template(
                "sorry.html", message=f"User with email {email} already exists."
            )
        if get_record_by_username:
            return render_template(
                "sorry.html", message=f"Username '{username}' is already taken."
            )
        return flag

    def get_user_profile(self, user_id: int):
        user_profile = dict()
        user_profile["user_id"] = user_id
        get_record_by_username = self.db.execute(
            "SELECT * FROM userinfo WHERE user_id=?", (user_id,)
        ).fetchone()
        profile_username = self.db.execute(
            "SELECT username FROM user WHERE id=?", (user_id,)
        ).fetchone()[0]

        user_profile["username"] = profile_username
        fields = ["firstname", "middlename", "lastname", "gender", "dob", "email"]
        for index, attribute in enumerate(fields):
            user_profile[attribute] = get_record_by_username[index + 1]
        user_profile["name"] = (
            f"{user_profile['firstname']} {user_profile['middlename']} {user_profile['lastname']}"
        )
        return user_profile

    def register_user(self, user: dict):
        try:
            self.db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (user["username"], user["password"]),
            )
            userid = self.db.execute(
                "SELECT id FROM user WHERE username=?", (user["username"],)
            ).fetchone()[0]
            self.db.execute(
                "INSERT INTO userinfo (user_id, firstName, middlename, lastname, gender, email, dob) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    userid,
                    user["firstname"],
                    user["middlename"],
                    user["lastname"],
                    user["gender"],
                    user["email"],
                    user["dob"],
                ),
            )
            self.conn.commit()
            return render_template("success.html")
        except sqlite3.Error as err:
            logging.error(f"register_user: {err}")
            return render_template("sorry.html", message=err)


class GroupDatabase(MyDatabase):
    def create_group(self, user_id: int, group_name: str):
        group_id = self.db.execute(
            "SELECT id FROM user_group WHERE name = ?", (group_name,)
        ).fetchone()
        print("okcddcssssdxsdsdsdiioiuioaaaaaaaaaaa")
        if group_id:
            return render_template(
                "sorry.html",
                message=f"{group_name} already exists. Please choose a different name or join the existing group.",
            )

        self.db.execute("INSERT INTO user_group (name) VALUES (?)", (group_name,))
        group_id = self.db.execute(
            "SELECT id FROM user_group WHERE name = ?", (group_name,)
        ).fetchone()[0]
        self.db.execute(
            "INSERT INTO group_member (user_id, group_id) VALUES (?, ?)",
            (user_id, group_id),
        )
        self.conn.commit()
        self.join_group(user_id=user_id, group_name=group_name)
        return True

    def join_group(self, user_id, group_name):
        group_id = self.db.execute(
            "SELECT id FROM user_group WHERE name = ?", (group_name,)
        ).fetchone()
        if not group_id:
            return render_template(
                "sorry.html",
                message=f"{group_name} does not exist. Please choose a different name or create a new group.",
            )

        try:
            self.db.execute(
                "INSERT INTO group_member (user_id, group_id) VALUES (?, ?)",
                (user_id, group_id[0]),
            )
            self.conn.commit()
        except sqlite3.Error as err:
            logging.warning(f"[join_group]: {err}")
            return False
        return True

    def get_current_connection(self, user_id: int):
        groups_name = self.db.execute(
            """
                            SELECT user_group.name
                            FROM group_member 
                            JOIN user_group ON user_group.id = group_member.group_id
                            WHERE group_member.user_id=?
                        """,
            (user_id,),
        ).fetchall()
        return groups_name

    def check_group(self, group):
        group_record = self.db.execute(
            "SELECT id FROM user_group WHERE name = ?", (group,)
        ).fetchone()
        return bool(group_record)


class PostDatabase(MyDatabase):
    def create_post(self, user_id, group, post):
        print("[INFO] Creating Post")
        try:
            group_id = self.db.execute(
                "SELECT id FROM user_group WHERE name = ?", (group,)
            ).fetchone()
            self.db.execute(
                "INSERT INTO posts (content, user_id, group_id) VALUES (?, ?, ?)",
                (post, user_id, group_id[0]),
            )
            self.conn.commit()
        except sqlite3.Error:
            return render_template(
                "sorry.html", message=f"Failed to create post in group {group}"
            )

    def get_posts(self, user_id, group):
        try:
            group_id = self.db.execute(
                "SELECT id FROM user_group WHERE name = ?", (group,)
            ).fetchone()
            posts = self.db.execute(
                """
                SELECT user.username, posts.content, posts.doc
                FROM user 
                JOIN posts ON user.id = posts.user_id
                WHERE group_id = ?
            """,
                (group_id[0],),
            ).fetchmany(5)
            print("[INFO] getting all post for group....")
            return posts
        except sqlite3.Error as err:
            print(f"[INFO] Error while retrieving posts: {err}")
            return None

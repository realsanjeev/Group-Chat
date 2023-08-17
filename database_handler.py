import sqlite3
from flask import render_template

from logger import logging

class MyDatabase:
    def __init__(self, db_name,
                 check_same_thread=False):
        self.db_name = db_name
        self.conn = sqlite3.connect("myDatabase.sqlite",
                                    check_same_thread=check_same_thread)
        self.db = self.conn.cursor()


    def is_registered(self, username: str, email: str):
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
        get_record_by_email = self.db.execute("""
                                    SELECT id 
                                    FROM user 
                                    WHERE username=?""", (username,)).fetchone()
        get_record_by_username = self.db.execute("""SELECT user_id
                                                FROM userinfo 
                                                WHERE email=?""", (email,)).fetchone()
        if get_record_by_email:
            return render_template("sorry.html",
                                message=f"User with email {email} already exists.")
        if get_record_by_username:
            return render_template("sorry.html",
                                message=f"Username '{username}' is already taken.")
        return flag


    def get_user_profile(self, user_id: int):
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
        get_record_by_username = self.db.execute("""SELECT *
                                                FROM userinfo 
                                                WHERE 
                                                user_id=?""", (user_id,)).fetchone()
        profile_username = self.db.execute("""
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


    def register_user(self, user: dict):
        """
        Register the user in the database with their personal information and login credentials.

        Args:
            user(dict): A dictionary containing user information with keys\
                "firstname", "middlename","lastname", "dob", "username", \
                    "password", "email", and "gender".

        Returns:
            If the user is successfully saved, this function returns a success message \
            rendered by the Flask template. If the user cannot be saved, \
            it returns a sorry message rendered by the Flask template.
        """
        try:
            self.db.execute("""
                        INSERT INTO user 
                        (username, password) 
                        VALUES (?, ?)""", (user["username"], user["password"]))
            userid = self.db.execute("""SELECT id
                                    FROM user 
                                    WHERE username=?""", (user["username"],)).fetchone()[0]
            self.db.execute("""
                INSERT INTO userinfo 
                (user_id, firstName, middlename, lastname, gender, email, dob)
                values (?,?,?,?,?,?,?)
                """, (userid, user["firstname"], user["middlename"], user["lastname"],
                    user["gender"], user["email"], user["dob"]))
            self.conn.commit()
            return render_template("success.html")
        except sqlite3.Error as err:
            logging.error(f"register_user: {err}")
            return render_template("sorry.html", message=err)


    def create_group(self, user_id: int, group_name: str):
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
        group_id = self.db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group_name,)
        ).fetchone()

        if group_id:
            return render_template("sorry.html",
                                message=f"{group_name} already exists. Please choose a different \
                                    name or join the existing group."
                                )
        # Create new group and add user as member
        self.db.execute(
            """INSERT INTO user_group (name) VALUES (?)""", (group_name,))
        group_id = self.db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group_name,)
        ).fetchone()[0]
        self.db.execute(
            """INSERT INTO group_member 
            (user_id, group_id) 
            VALUES (?, ?)""",
            (user_id, group_id),
        )
        self.conn.commit()
        # join the group if you are creator of group
        self.join_group(user_id=user_id, group_name=group_name)
        return True


    def join_group(self, user_id, group_name):
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
        group_id = self.db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group_name,)
        ).fetchone()

        if not group_id:
            return render_template("sorry.html",
                                message=f"{group_name} already exists. Please choose a different \
                    name or join the existing group."
                                )
        try:
            # Add user as member in given Group
            self.db.execute(
                """INSERT INTO group_member 
                (user_id, group_id) 
                VALUES (?, ?)""",
                (user_id, group_id[0]),
            )
            self.conn.commit()
        except sqlite3.Error as err:
            logging.warning(f"[join_group]: {err}")
            return False
        return True


    def get_current_connection(self, user_id: int):
        """
        Retrieve the names of the groups that a user with the given `user_id` is a member of.

        Args:
            user_id: int - the id of the user to retrieve the group membership for.

        Returns:
            List of tuple - the names of the groups that the \
                user with the given `user_id` is a member of.
        """
        groups_name = self.db.execute("""
                            SELECT user_group.name
                            FROM group_member 
                            JOIN user_group ON user_group.id = group_member.group_id
                            WHERE group_member.user_id=?
                        """, (user_id,)).fetchall()

        return groups_name


    def check_group(self, group):
        group_record = self.db.execute(
            """SELECT id FROM user_group WHERE name = ?""", (group,)
        ).fetchone()
        if group_record:
            return True
        else:
            return False

    def create_post(self, user_id, group, post):
        print("[INFO] Creating Post")
        try:
            group_id = self.db.execute(
                """SELECT id FROM user_group WHERE name = ?""", (group,)
            ).fetchone()
            self.db.execute("""
                        INSERT INTO posts 
                        (content, user_id, group_id) 
                        VALUES (?, ?, ?)""", (post, user_id, group_id[0]))
            self.conn.commit()
        except sqlite3.Error:
            return render_template("sorry.html",
                                    message=f"Failed to create post in group {group}")


    def get_posts(self, user_id, group):
        try:
            group_id = self.db.execute(
                """SELECT id FROM user_group WHERE name = ?""", (group,)
            ).fetchone()
            posts = self.db.execute("""SELECT user.username, posts.content, posts.doc
                    FROM user JOIN posts ON user.id = posts.user_id
                    WHERE group_id = (?)""",
                    (group_id[0],)).fetchmany(5)
            print("[INFO] getting all post for group....")
            return posts

        except sqlite3.Error as err:
            print(f"[INFO] Error wile retriving posts: {err}")
            return None

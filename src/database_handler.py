import sqlite3
from flask import render_template
from src.logger import logging


class MyDatabase:
    def __init__(self, db_name, check_same_thread=False):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=check_same_thread)
        self.db = self.conn.cursor()


class UserDatabase(MyDatabase):
    def is_registered(self, username: str = None, email: str = None):
        """Check if username or email is already registered.
        
        Args:
            username: Username to check (optional)
            email: Email to check (optional)
            
        Returns:
            dict with 'username' and 'email' keys indicating if each exists
        """
        result = {'username': False, 'email': False}
        
        # Check if username exists
        if username:
            get_record_by_username = self.db.execute(
                "SELECT id FROM user WHERE username=?", (username,)
            ).fetchone()
            
            if get_record_by_username:
                logging.warning(f"Registration attempt with existing username: {username}")
                result['username'] = True
        
        # Check if email exists
        if email:
            get_record_by_email = self.db.execute(
                "SELECT user_id FROM userinfo WHERE email=?", (email,)
            ).fetchone()
            
            if get_record_by_email:
                logging.warning(f"Registration attempt with existing email: {email}")
                result['email'] = True
        
        return result

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
                "INSERT INTO userinfo (user_id, firstname, middlename, lastname, gender, email, dob) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
        """Create a new group and add the creator as a member.
        
        Args:
            user_id: ID of the user creating the group
            group_name: Name of the group to create
            
        Returns:
            True if successful, or rendered template with error message
        """
        group_id = self.db.execute(
            "SELECT id FROM user_group WHERE name = ?", (group_name,)
        ).fetchone()
        
        if group_id:
            logging.info(f"Group creation failed - '{group_name}' already exists")
            return render_template(
                "sorry.html",
                message=f"{group_name} already exists. Please choose a different name or join the existing group.",
            )

        try:
            self.db.execute("INSERT INTO user_group (name) VALUES (?)", (group_name,))
            group_id = self.db.execute(
                "SELECT id FROM user_group WHERE name = ?", (group_name,)
            ).fetchone()[0]
            self.db.execute(
                "INSERT INTO group_member (user_id, group_id) VALUES (?, ?)",
                (user_id, group_id),
            )
            self.conn.commit()
            logging.info(f"User {user_id} created group '{group_name}'")
            return True
        except sqlite3.Error as err:
            logging.error(f"create_group: {err}")
            self.conn.rollback()
            return render_template("sorry.html", message="Failed to create group. Please try again.")

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
    def create_post(self, content, user_id, group):
        """Create a new post in a group.
        
        Args:
            content: Post content
            user_id: ID of the user creating the post
            group: Name of the group
            
        Returns:
            bool: True if successful, False or error template otherwise
        """
        try:
            # Get group ID
            group_id = self.db.execute(
                "SELECT id FROM user_group WHERE name=?", (group,)
            ).fetchone()
            
            if not group_id:
                return render_template(
                    "sorry.html", message=f"Group '{group}' not found."
                )
            
            self.db.execute(
                "INSERT INTO posts (content, user_id, group_id) VALUES (?, ?, ?)",
                (content, user_id, group_id[0]),
            )
            self.conn.commit()
            logging.info(f"User {user_id} created post in group '{group}'")
            return True
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error creating post: {e}")
            return False

    def get_posts(self, group):
        """Return all posts from a group with post IDs.
        
        Args:
            group: Name of the group
            
        Returns:
            List of posts (username, content, date, post_id) or None if error
        """
        try:
            group_id = self.db.execute(
                "SELECT id FROM user_group WHERE name = ?", (group,)
            ).fetchone()
            
            if not group_id:
                logging.warning(f"Get posts failed - group '{group}' not found")
                return None
            
            posts = self.db.execute(
                """
                SELECT user.username, posts.content, posts.doc, posts.id
                FROM user 
                JOIN posts ON user.id = posts.user_id
                WHERE group_id = ?
                ORDER BY posts.id DESC
            """,
                (group_id[0],),
            ).fetchall()
            logging.info(f"Retrieved {len(posts)} posts for group '{group}'")
            return posts
        except sqlite3.Error as err:
            logging.error(f"get_posts: {err}")
            return None
    
    def add_comment(self, post_id: int, user_id: int, content: str):
        """Add a comment to a post.
        
        Args:
            post_id: ID of the post to comment on
            user_id: ID of the user making the comment
            content: Comment content
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.db.execute(
                "INSERT INTO comment (comment, post_id, user_id) VALUES (?, ?, ?)",
                (content, post_id, user_id)
            )
            self.conn.commit()
            logging.info(f"User {user_id} commented on post {post_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error adding comment: {e}")
            return False
    
    def get_comments(self, post_id: int):
        """Get all comments for a post.
        
        Args:
            post_id: ID of the post
            
        Returns:
            list: List of tuples (username, comment, timestamp)
        """
        try:
            comments = self.db.execute("""
                SELECT u.username, c.comment, c.commented_on
                FROM comment c
                JOIN user u ON c.user_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.commented_on ASC
            """, (post_id,)).fetchall()
            return comments
        except Exception as e:
            logging.error(f"Error fetching comments: {e}")
            return []
    
    def get_comment_count(self, post_id: int):
        """Get the number of comments on a post.
        
        Args:
            post_id: ID of the post
            
        Returns:
            int: Number of comments
        """
        try:
            count = self.db.execute(
                "SELECT COUNT(*) FROM comment WHERE post_id = ?",
                (post_id,)
            ).fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Error counting comments: {e}")
            return 0
    
    def toggle_like(self, post_id: int, user_id: int):
        """Toggle a like on a post (add if not exists, remove if exists).
        
        Args:
            post_id: ID of the post
            user_id: ID of the user
            
        Returns:
            bool: True if liked, False if unliked
        """
        try:
            # Check if user already liked the post
            existing_like = self.db.execute(
                "SELECT 1 FROM like WHERE post_id = ? AND user_id = ?",
                (post_id, user_id)
            ).fetchone()
            
            if existing_like:
                # Unlike
                self.db.execute(
                    "DELETE FROM like WHERE post_id = ? AND user_id = ?",
                    (post_id, user_id)
                )
                self.conn.commit()
                logging.info(f"User {user_id} unliked post {post_id}")
                return False
            else:
                # Like
                self.db.execute(
                    "INSERT INTO like (post_id, user_id) VALUES (?, ?)",
                    (post_id, user_id)
                )
                self.conn.commit()
                logging.info(f"User {user_id} liked post {post_id}")
                return True
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error toggling like: {e}")
            return False
    
    def get_like_count(self, post_id: int):
        """Get the number of likes on a post.
        
        Args:
            post_id: ID of the post
            
        Returns:
            int: Number of likes
        """
        try:
            count = self.db.execute(
                "SELECT COUNT(*) FROM like WHERE post_id = ?",
                (post_id,)
            ).fetchone()[0]
            return count
        except Exception as e:
            logging.error(f"Error counting likes: {e}")
            return 0
    
    def user_has_liked(self, post_id: int, user_id: int):
        """Check if a user has liked a post.
        
        Args:
            post_id: ID of the post
            user_id: ID of the user
            
        Returns:
            bool: True if user has liked, False otherwise
        """
        try:
            like = self.db.execute(
                "SELECT 1 FROM like WHERE post_id = ? AND user_id = ?",
                (post_id, user_id)
            ).fetchone()
            return like is not None
        except Exception as e:
            logging.error(f"Error checking like status: {e}")
            return False

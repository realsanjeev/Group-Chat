"""
SQL Command for creating Table
"""

USER = """ CREATE TABLE IF NOT EXISTS user (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                username text NOT NULL UNIQUE,
                                password text NOT NULL
                            ); """
USERINFO = """CREATE TABLE IF NOT EXISTS userinfo (
                            user_id integer PRIMARY KEY,
                            firstname TEXT NOT NULL,
                            middlename TEXT,
                            lastname TEXT NOT NULL,
                            gender TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            FOREIGN KEY (user_id) REFERENCES user (id)
                        );"""
PROFILE_PIC = """ CREATE TABLE IF NOT EXISTS profile_pic (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                user_id integer NOT NULL,
                                pics Blob NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES profile_pic (id)
                            ); """
GROUP = """ CREATE TABLE IF NOT EXISTS user_group (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name text NOT NULL UNIQUE
                );"""
MEMBER = """ CREATE TABLE IF NOT EXISTS group_member (
                    user_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (group_id) REFERENCES user_group (id),
                    PRIMARY KEY (user_id, group_id)
                );  """

POST = """ CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    doc DATE DEFAULT CURRENT_DATE,
                    user_id INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (group_id) REFERENCES user_group (id)
                );"""

LIKE = """ CREATE TABLE IF NOT EXISTS like(
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (post_id) REFERENCES posts (id),
                PRIMARY KEY (post_id, user_id)
                );
        """
COMMENT ="""CREATE TABLE IF NOT EXISTS comment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment text NOT NULL,
                    post_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    commented_on Date DEFAULT CURRENT_DATE,
                    FOREIGN KEY (post_id) REFERENCES posts (id),
                    FOREIGN KEY (user_id) REFERENCES user(id)
                    );
                    """
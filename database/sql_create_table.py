"""
SQL Command for creating Table
"""

USER = """ CREATE TABLE IF NOT EXISTS user (
                                id integer PRIMARY KEY,
                                username text NOT NULL,
                                password text NOT NULL
                            ); """
USERINFO = """CREATE TABLE IF NOT EXISTS userinfo (
                            id integer PRIMARY KEY,
                            firstname text NOT NULL,
                            middlename text,
                            lastname text NOT NULL,
                            gender text NOT NULL,
                            dob text NOT NULL,
                            user_id integer NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user (id)
                        );"""
PROFILE_PIC = """ CREATE TABLE IF NOT EXISTS profile_pic (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES profile_pic (id)
                            ); """
GROUP = """ CREATE TABLE IF NOT EXISTS group (
                    id integer PRIMARY KEY,
                    groupname text NOT NULL
                );"""
MEMBER = """ CREATE TABLE IF NOT member (
                    user_id integer NOT NULL,
                    group_id integer NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id),
                    FOREIGN KEY (group_id) REFERENCES group (id),
                    PRIMARY KEY user_id, group_id
                    );
                    """
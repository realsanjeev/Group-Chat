"""Database initialization script for Group Chat application.

This module creates all required tables on fresh startup.
"""

import sqlite3
import logging
from src.logger import logging


def init_database(db_name="myDatabase.sqlite"):
    """Initialize all required database tables.
    
    Args:
        db_name: Name of the SQLite database file
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # 1. User table - stores user account information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        logging.info("Created/verified 'user' table")
        
        # 2. UserInfo table - stores additional user profile information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS userinfo (
                user_id INTEGER PRIMARY KEY,
                firstname TEXT NOT NULL,
                middlename TEXT,
                lastname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                dob TEXT NOT NULL,
                gender TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        logging.info("Created/verified 'userinfo' table")
        
        # 3. User_Group table - stores group/community information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_group (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        logging.info("Created/verified 'user_group' table")
        
        # 4. Group_Member table - junction table for user-group relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_member (
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (group_id) REFERENCES user_group(id),
                PRIMARY KEY (user_id, group_id)
            )
        """)
        logging.info("Created/verified 'group_member' table")
        
        # 5. Posts table - stores posts in groups
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                doc DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (group_id) REFERENCES user_group(id)
            )
        """)
        logging.info("Created/verified 'posts' table")
        
        # 6. Comments table - stores comments on posts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT NOT NULL,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                commented_on DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        logging.info("Created/verified 'comment' table")
        
        # 7. Likes table - stores likes on posts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS like (
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (post_id) REFERENCES posts(id),
                PRIMARY KEY (post_id, user_id)
            )
        """)
        logging.info("Created/verified 'like' table")
        
        conn.commit()
        logging.info("✅ Database initialization completed successfully")
        
    except sqlite3.Error as e:
        logging.error(f"❌ Database initialization failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    # Run initialization when script is executed directly
    init_database()
    print("Database tables created successfully!")

import sqlite3
import re

def connect_database(database):
    conn = None
    try:
        conn = sqlite3.connect(database=database)
        print("Connected to database...")
    except sqlite3.Error as err:
        print(f"Failed to connect Database. Error: {err}")
        conn = None
    return conn

def create_table(conn, sql_command):
    cursor = conn.cursor()
    # search for the word "table name""
    table_name = re.search(r"\b(\w+)\s*\(", sql_command).group(1)
    try:
        cursor.execute(sql_command)
        cursor.commit()
        print(f"Table {table_name.upper()} is created.")
    except sqlite3.Error as err:
        print(f"Failed to execute command for table {table_name.upper()} creation. Error: {err}")

if __name__ == "__main__":
    database_name = "first_db.sqlite"
    sql_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL
                                    ); """
    sql_userinfo_table = """CREATE TABLE IF NOT EXISTS userinfo (
                                    id integer PRIMARY KEY,
                                    firstname text NOT NULL,
                                    middlename text,
                                    lastname text NOT NULL,
                                    gender text NOT NULL,
                                    dob text NOT NULL,
                                    user_id integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES user (id)
                                );"""
    sql_profile_pic_table = """ CREATE TABLE IF NOT EXISTS profile_pic (
                                        id integer PRIMARY KEY,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES profile_pic (id)
                                    ); """
    conn = connect_database(database_name)
    create_table(conn, sql_user_table)
    create_table(conn, sql_userinfo_table)
    

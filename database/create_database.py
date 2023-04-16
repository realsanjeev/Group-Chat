import re
import sqlite3
import sql_create_table as table

def connect_database(database):
    """
    Connects to the specified SQLite database.

    Args:
        database (str): The path to the SQLite database.

    Returns:
        connection (sqlite3.Connection): A connection object if the connection is successful,
                                         None otherwise.
    """
    connection = None
    try:
        connection = sqlite3.connect(database=database)
        print("Connected to database...")
    except sqlite3.Error as err:
        print(f"Failed to connect Database. Error: {err}")
        connection = None
    return connection


def create_table(connect, sql_command):
    """
    Creates a table in a SQLite database using the provided SQL command.

    Args:
        connect: A SQLite database connection object.
        sql_command: A string containing the SQL command to create the table.

    Returns:
        None

    Raises:
        sqlite3.Error: If there is an error executing the SQL command.

    Example:
        create_table(connection, 
        "CREATE TABLE employees (id INTEGER PRIMARY KEY, 
                                name TEXT,
                                age INTEGER)")
    """
    cursor = connect.cursor()
    # search for the word "table name""
    table_name = re.search(r"\b(\w+)\s*\(", sql_command).group(1)
    try:
        cursor.execute(sql_command)
        connect.commit()
        print(f"Table {table_name.upper()} is created.")
    except sqlite3.Error as err:
        print(f"Failed to execute command for table {table_name.upper()} creation. Error: {err}")
        print(sql_command)


if __name__ == "__main__":
    DATABASE = "myDatabase.sqlite"
    conn = connect_database(DATABASE)
    create_table(conn, table.USER)
    create_table(conn, table.USERINFO)
    create_table(conn, table.PROFILE_PIC)
    create_table(conn, table.GROUP)
    create_table(conn, table.MEMBER)
    create_table(conn, table.POST)
    create_table(conn, table.LIKE)
    create_table(conn, table.COMMENT)
    
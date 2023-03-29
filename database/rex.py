import re

text = """CREATE TABLE IF NOT EXISTS user (
                id integer PRIMARY KEY,
                username text NOT NULL,
                password text NOT NULL
            );"""

result = re.search(r"\b(\w+)\s*\(", text)

if result:
    print(result.group(1))
else:
    print("No match found.")

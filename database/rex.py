import sqlite3
from PIL import Image


with open("image.jpg", 'rb') as fp:
    with open("recreate_image.png", "wb") as filep:
        filep.write(fp.read())


# Open the image file
with open('image.jpg', 'rb') as fp:
    img = fp.read()

with open("file_data.png", 'wb') as fp:
    fp.write(img)

# Insert the image into the database
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute( """ CREATE TABLE IF NOT EXISTS images (
                                        id integer NOT NULL PRIMARY KEY,
                                        name text NOT NULL,
                                        data Blob NOT NULL
                                    ); """)
c.execute("INSERT INTO images (name, data) VALUES (?, ?)", ('old_bank', sqlite3.Binary(img)))
conn.commit()


# Retrieve the image from the database
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
c.execute("SELECT name, data FROM images WHERE id=?", (1,))
row = c.fetchone()
# print(f"row ans: {row[1]}")

with open("ok.png", 'wb') as write_image:
    write_image.write(row[1])
# # Save the image to disk
# # with open(row[0], 'wb') as f:
# #     f.write(row[1])

# conn.close()

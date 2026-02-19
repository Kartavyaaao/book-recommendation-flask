import sqlite3

db = sqlite3.connect("users.db")

db.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

db.commit()
db.close()

print("Database created!")

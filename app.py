from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd

app = Flask(__name__)

# ---------------- LOAD CSV ----------------
books = pd.read_csv("book_dataaa.csv")


# ---------------- INIT DATABASE ----------------
def init_db():
    db = sqlite3.connect("users.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    db.commit()
    db.close()

init_db()


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return sqlite3.connect("users.db")


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        db.close()

        if user:
            return redirect("/home")
        else:
            return "Invalid login!"

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("register.html")


# ---------------- HOME ----------------
@app.route("/home")
def home():

    query = request.args.get("search")

    if query:
        filtered_books = books[
            books["Title"].str.contains(query, case=False, na=False)
        ]
    else:
        filtered_books = books

    return render_template(
        "home.html",
        books=filtered_books.to_dict(orient="records")
    )


# ---------------- BOOK DETAIL ----------------
@app.route("/book/<string:upc>")
def book_detail(upc):

    book = books[books["UPC"] == upc].to_dict(orient="records")

    if book:
        return render_template("book_detail.html", book=book[0])
    else:
        return "Book not found"


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)

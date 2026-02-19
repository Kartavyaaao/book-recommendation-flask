from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# ---------------- LOAD CSV ----------------
books = pd.read_csv("book_dataaa.csv")

# ---------------- TEMP USER STORAGE (for Vercel) ----------------
users = {}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
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

        users[username] = password
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

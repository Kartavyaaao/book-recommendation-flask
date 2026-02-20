from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# ---------------- LOAD CSV ----------------
# Added low_memory=False to avoid DtypeWarnings if your CSV is large
books = pd.read_csv("book_dataaa.csv")

# ---------------- TEMP USER STORAGE ----------------
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

# ---------------- HOME (With Search & Sort) ----------------
@app.route("/home")
def home():
    query = request.args.get("search")
    sort_by = request.args.get("sort")

    # Start with all books
    filtered_books = books.copy()

    # 1. Apply Search Filter
    if query:
        filtered_books = filtered_books[
            filtered_books["Title"].str.contains(query, case=False, na=False)
        ]

    # 2. Apply Sorting
    if sort_by:
        # We check if sort_by is a valid column to prevent errors
        if sort_by in filtered_books.columns:
            # If sorting by price, you might need to clean the '$' sign first
            # But for a simple alphabetical/numerical sort:
            filtered_books = filtered_books.sort_values(by=sort_by, ascending=True)

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

if __name__ == "__main__":
    app.run(debug=True)
    

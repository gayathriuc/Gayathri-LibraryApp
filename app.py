from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "library-secret-key"

books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "available": True
    },
    {
        "id": 2,
        "title": "Atomic Habits",
        "author": "James Clear",
        "available": True
    },
    {
        "id": 3,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "available": False
    }
]


@app.route("/")
def home():
    return render_template("index.html", books=books)


@app.route("/add_book", methods=["POST"])
def add_book():

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()

    if not title or not author:
        flash("Fill all fields.", "error")
        return redirect(url_for("home"))

    new_book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "available": True
    }

    books.append(new_book)

    flash(f"Book '{title}' added!", "success")

    return redirect(url_for("home"))


@app.route("/borrow_book/<int:book_id>", methods=["POST"])
def borrow_book(book_id):

    for book in books:

        if book["id"] == book_id:

            book["available"] = False
            flash(f"Book '{book['title']}' borrowed.", "success")
            return redirect(url_for("home"))

    return "Book not found"

@app.route("/return_book/<int:book_id>", methods=["POST"])
def return_book(book_id):

    for book in books:

        if book["id"] == book_id:

            book["available"] = True
            flash(f"Book '{book['title']}' returned.", "success")
            return redirect(url_for("home"))

    return "Book not found"

@app.route("/check_availability", methods=["POST"])
def check_availability():
    title = request.form.get("check_title", "").strip()

    if not title:
        flash("Enter a book title to check availability.", "error")
        return redirect(url_for("home"))

    for book in books:
        if book["title"].lower() == title.lower():
            if book["available"]:
                flash(f"Book '{book['title']}' is Available.", "success")
            else:
                flash(f"Book '{book['title']}' is Borrowed.", "info")
            return redirect(url_for("home"))

    flash(f"Book '{title}' is Not Found.", "error")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
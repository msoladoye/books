import json
# import os
import requests
from db_connection import User, Sessions, Books, Review
from flask import Flask, session, render_template, request, redirect
from flask_session import Session
import requests
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "aUplmCVpqROVhJmlI8BQ", "isbns": "9781632168146"})
# print(res.json())

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/api/<string:isbn>", methods=["GET"])
def getAPI(isbn):
    book = Books(isbn, '', '', '').getBook("isbn", isbn)
    if book is None:
        return {"ERROR": "404 invalid isbn number"}, 555
        # return render_template("error.html", error="404 request not found")
    if book.ratings <= 0:
        ratings = book.ratings
    else:
        ratings = book.ratings/float(book.ratings_count)
    bookApi = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "ratings": ratings,
        "ratings_count": book.ratings_count
    }
    return json.dumps(bookApi)


@app.route("/posting", methods=["POST"])
def post_review():
    if session.get('user_id') is None:
        return render_template('log_in.html', errMsg="Unauthorized access")
    req = request.form
    book_id = session.get('book_id')
    user_id = session.get('user_id')
    review = req.get('comment')
    rating = req.get('rating')
    if review is "" or rating is "":
        pass
    else:
        book = Books('', '', '', '')
        bookValue = book.getBook("id", book_id)
        book.updateBook("ratings", bookValue.ratings+float(rating), book_id)
        book.updateBook("ratings_count", bookValue.ratings_count+1, book_id)
        review = Review(book_id, user_id, review, rating)
        review.set_review()
    return redirect("/books/"+str(session.get('book_id')))


@app.route("/books/<int:book_id>")
def books(book_id):
    # print(session.get('user_id'))
    if session.get('user_id') is None:
        return render_template('log_in.html', errMsg="Unauthorized access")
    books = Books('', '', '', '')
    book = books.getBook("id", book_id)
    if book is None:
        return render_template("error.html", error="Invalid book number")
    session['book_id'] = book_id
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "aUplmCVpqROVhJmlI8BQ", "isbns": book.isbn})
    goodreadsAvg = ""
    goodreadsWRC = ""
    if res.status_code == 200:
        goodreads = res.json()['books']
        goodreadsAvg = goodreads[0]['average_rating']
        goodreadsWRC = goodreads[0]['work_ratings_count']
    review = Review(session.get('book_id'), '', '', '')
    review_details = review.get_review_details()
    enablebutton = ""
    for review in review_details:
        if review.user_id is session.get('user_id'):
            print(review.user_id)
            enablebutton = "disabled"
            break
    if book.ratings <= 0:
        ratings = book.ratings
    else:
        ratings = book.ratings/float(book.ratings_count)
    values = {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "ratings": ratings,
        "ratings_count": book.ratings_count,
        "enablebutton": enablebutton,
        "reviews": review_details,
        "goodreadsAvg": goodreadsAvg,
        "goodreadsWRC": goodreadsWRC
    }
    return render_template("book_review.html", values=values, enablebutton=enablebutton, username=session.get('username'))
    # return render_template("book_review.html", isbn=book.isbn, title=book.title, author=book.author, year=book.year, enablebutton=enablebutton, reviews=review_details)


@app.route("/search", methods=['POST'])
@app.route("/index/search", methods=['POST'])
def searchDb():
    print(session.get('user_id'))
    if session.get('user_id') is None:
        return render_template('log_in.html')
    req = request.form
    isbn = req.get('isbn')
    title = req.get('title')
    author = req.get('author')
    year = req.get('year')

    books = Books(isbn, title, author, year)
    searchMatch = books.getBooks()
    return render_template('index.html', searchMatch=searchMatch, username=session.get('username'))


@app.route("/")
@app.route("/index")
def index():
    _sessions = Sessions('user_id', '').get_session_id()
    if _sessions is None:
        return render_template('log_in.html')
    return render_template('index.html', username=session.get('username'))


@app.route("/signin/", methods=['POST'])
def signin():
    _req = request.form
    _username = _req.get('username').lower()
    _password = _req.get('password')
    if not _username or not _password:
        return render_template('log_in.html', errMsgl="username or password can not be blank")
    # login
    _login = User(_username, _password).login()
    if not _login:
        return render_template('log_in.html', errMsgl="invalid username or password")
        # user.inser()
    else:
        Sessions('user_id', _login.id).set_session_id()
        Sessions('username', _login.username).set_session_id()
    return redirect("/")


@app.route("/signup/", methods=['POST'])
def signup():
    _req = request.form
    _username = _req.get('username').lower()
    _password = _req.get('password')
    if not _username or not _password:
        return render_template('log_in.html', errMsgr="username or password can not be blank")
    # login
    _insert = User(_username, _password).insert()
    if not _insert or _insert is "":
        return render_template('log_in.html', errMsgr="user already exists, Try a new username")
        # user.inser()
    else:
        Sessions('user_id', _insert).set_session_id()
        Sessions('username', _username).set_session_id()
    return redirect("/")


@app.route("/login")
def login():
    return render_template('log_in.html')


@app.route("/logout")
def log_out():
    session['user_id'] = None
    return redirect("/login")

import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import session
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # super().__init__()

    def login(self):
        try:
            return db.execute("SELECT id, username, password FROM users WHERE username=:user and password=:pass", {
                "user": self.username, "pass": self.password}).fetchone()
        finally:
            db.close()

    def insert(self):
        try:
            db.execute("INSERT INTO users(username,password) VALUES(:user, :pass) RETURNING id", {
                "user": self.username, "pass": self.password})
            db.commit()
            return db.execute("SELECT id FROM users ORDER BY id DESC").fetchone()[0]
        except:
            return ""
        finally:
            db.close()


class Sessions():
    def __init__(self, session_name, session_value):
        self.session_name = session_name
        self.session_value = session_value

    def get_session_id(self):
        if session.get('user_id') is None:
            return None
        else:
            try:
                return db.execute("SELECT username, password FROM users WHERE id=:id", {
                    "id": session['user_id']}).fetchone()
            finally:
                db.close()

    def set_session_id(self):
        session[self.session_name] = self.session_value


class Books():
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def setBooks(self):
        try:
            db.execute(
                "INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title,:author,:year)", {"isbn": self.isbn, "title": self.title, "author": self.author, "year": self.year})
            db.commit()
        finally:
            db.close()

    def getBooks(self):
        try:
            return db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :title AND  author LIKE :author",
                              {"isbn": '%'+self.isbn+'%', "title": '%'+self.title+'%', "author": '%'+self.author+'%'}).fetchall()
        finally:
            db.close()

    def getBook(self, column, value):
        try:
            return db.execute("SELECT * FROM books WHERE "+column+" = :value",
                              {"value": value}).fetchone()
        finally:
            db.close()

    def updateBook(self, column, value, id):
        try:
            db.execute("UPDATE books SET "+column+" = :value where id=:id",
                       {"value": value, "id": id})
            db.commit()
        finally:
            db.close()
    # def getBook(self, id):
    #     try:
    #         return db.execute("SELECT * FROM books WHERE id = :id",
    #                         {"id": id}).fetchone()
    #     finally:
    #         db.close()


class Review():
    def __init__(self, book_id, user_id, review, rating):
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.review = review

    def get_review(self):
        try:
            return db.execute("SELECT * FROM book_review WHERE book_id = :book_id",
                              {"book_id": self.book_id}).fetchall()
        finally:
            db.close()

    def set_review(self):
        now = datetime.datetime.now()
        review_date = now.strftime("%m/%d/%Y %H:%M:%S")
        try:
            db.execute(
                "INSERT INTO book_review(book_id, user_id, review, rating,review_date) VALUES(:book_id, :user_id, :review, :rating, :review_date)", {"book_id": self.book_id, "user_id": self.user_id, "review": self.review, "rating": self.rating, "review_date": review_date})
            db.commit()
        finally:
            db.close()

    def get_review_details(self):
        try:
            return db.execute("SELECT * FROM book_review INNER join users ON book_review.user_id = users.id WHERE book_review.book_id = :id", {"id": self.book_id}).fetchall()
        finally:
            db.close()

    #     return db.execute("SELECT * FROM book_review INNER JOIN books ON book_review.book_id = books.id INNER join users ON book_review.user_id = users.id WHERE books.id = :id", {"id": self.book_id}).fetchone()
# AND year = :year
# , "year": self.year

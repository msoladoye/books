# Project 1

# Web Programming with Python and JavaScript
# Description
    This application queries user's search for book and display books details if available with ratings from the site and rating from goodreads.com. Also comments made on the site by other readers
# Postgresql database
    postgres://wziywcawqjwlcj:a5421409bdaadb8623d3130efc018b27e90ff9d4014755d47b58655586caa87f@ec2-34-234-228-127.compute-1.amazonaws.com:5432/d7on3t5f563n0j
# PYTHON
    db_connection.py:
        this file contains python classes that communitcate with my postgresql database. Updating, selection or insertion queries are called from this folder, including setting and getting sessions
    appliction,py:
        this file contains my project main functions and Flask routing
    import.py:
        this contains python code that insert all books into a table 'books' by calling the book class
# HTML
    template/layout.html
        this is a html page with jinja syntax to set a layout for my site
    template/login.html
        this page contains two forms, for login and registration repectively
    template/index.html
        this is the landing page with login or sign up as successfull, also where you can search for books available
    template/book_review.html
        this page shows details about every selected book 
    template/error.html
        get returned if the book searched does not exist


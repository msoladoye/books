import csv
from db_connection import Books


def main():
    file = open("books.csv")
    reader = csv.reader(file)
    for isbn, title, author, year in reader:
        books = Books(isbn, title, author, int(year))
        books.setBooks()
    file.close()

if __name__ == '__main__':
    main()

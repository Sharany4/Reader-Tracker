# In this file I am creating the core functionality for my project
import json
import tkinter as tk


# My initial implementation will be to make the user
# able to add and remove from a tobe read list ,and move to a read list.
# Later this will be expanded so the can create custom lists.


# This class will have a title, author, year
# It will also store what collections it is a part of
# It will also have a to string method to represent itself
class Book:
    def __init__(self, title: str, author: str, year: int):
        if not title or not author or not year:
            raise ValueError("Title, author and year must not be empty")
        # check book is not already in read list
        self.title = title
        self.author = author
        self.year = year
        self.collections = []

    def note_book_as_read(self, storage, user_id: str):
        for coll in self.collections:  # remove book from all collections
            coll.remove_book(self)
        storage.remove_book_from_storage(self, user_id, remove_from_all_collections=True)
        storage.add_book_to_storage(self, user_id, "read")  # add book to read list

    def add_collection(self, coll: "BookCollection"):
        self.collections.append(coll)

    def remove_collection(self, coll: "BookCollection"):
        self.collections.remove(coll)

    def get_book_details(self):
        return f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}"

    def to_dict(self):  # creates the book in dictionary form as it can convert to json easily
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    @staticmethod
    def from_dict(book_dict: dict):
        return Book(book_dict['title'], book_dict['author'], book_dict['year'])

    def book_to_json_string(self):  # makes a string representation o a json object
        return json.dumps(self.to_dict())


# This class will represent a collection of books.
# It will provide functionality to add and remove books, and sort them
# how the user customizes.
class BookCollection:
    def __init__(self, name: str = None):
        if name is None:  # Handle the case where no name is provided
            self.name = "Unnamed Collection"
        elif not name:
            raise ValueError("Collection name must not be empty")
        else:
            self.name = name
        self.books = []  # Initialize the empty list

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be added")
        if book in self.books:
            raise DuplicateError(f" Book {book} is already in the collection")
        self.books.append(book)
        book.add_collection(self)
        self.sort_books()

    def add_book_with_storage(self, book: Book, storage, user_id: str):
        self.add_book(book)
        storage.add_book_to_storage(book, user_id, self.name)

    def remove_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be removed")
        if book not in self.books:
            raise ValueError("The book is not in the collection")
        self.books.remove(book)
        self.sort_books()
        book.remove_collection(self)

    def remove_book_with_storage(self, book: Book, storage, user_id: str):
        self.remove_book(book)
        storage.remove_book_from_storage(book, user_id, self.name)

    def print_collection(self):
        for b in self.books:
            print(b.get_book_details())

    def sort_books(self):
        self.books.sort(key=lambda x: (x.author, x.title))  # Sorts the books everytime another book is added


# TODO: create library class
# Library class works as the headmaster to manage collections and books
class Library:
    def __init__(self, storage: "JsonStorage"):
        self.storage = storage

    def load_gui(self):
        root = tk.Tk()  # create root widget

        # Setting some window properties
        root.title("Reader Tracker")
        pink = "#f39ff5"
        root.config(padx=100, pady=100, bg=pink)  # padding around the window
        root.minsize(200, 200)  # minimum size of the window
        root.maxsize(500, 500)  # maximum size of the window
        root.geometry("1200x900+50+50")  # size and position of the window

        # TODO: create list to let users pick a user or create one
        # TODO: show list of collections of that user
        # TODO: show list of books in that collection
        # TODO: add collection
        # TODO: delete collection
        # TODO: add book to collection
        # TODO: remove book from collection
        # TODO: mark book as read

        root.mainloop()  # runs the main event loop


# load up GUI
# let user pick user or create one ( when created forms them a json folder or add to database)
# let user see collections to view
# let user click collections and books to mark as read
# load collections
# add collection
# delete collection
# add book to this collection
# add book in general to storage
# remove book from this collection
# remove book in general from storage


# class for creating an exception when trying to add a duplicate
class DuplicateError(Exception):
    """Custom exception raised when a duplicate item is added."""
    pass

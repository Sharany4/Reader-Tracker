# In this file I am creating the core functionality for my project


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
        self.title = title
        self.author = author
        self.year = year
        self.collections = []

    # TODO add function that notes a book is read(removes from collections and adds to the read list)
    # To be finished once JSON saving is implemented
    def note_book_as_read(self):
        # add book to json of completed books
        for coll in self.collections:
            coll.remove_book(self)

    def add_collection(self, coll: "BookCollection"):
        self.collections.append(coll)

    def get_book_details(self):
        return f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}"

    # TODO: Create method to serialise and deserialise a book object


# This class will represent a collection of books.
# It will provide functionality to add and remove books, and sort them
# how the user customizes.
# Will need to figure out how to book books from one collection to another ones read
class BookCollection:
    def __init__(self):
        self.books = []  # Initialize the empty list
        # add it to the collections master json file

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be added")
        if book in self.books:
            raise DuplicateError(f" Book {book} is already in the collection")
        self.books.append(book)
        # add to collections json file
        self.books.sort(key=lambda x: (x.author, x.title))  # Sorts the books everytime another book is added

    def remove_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be removed")
        if book not in self.books:
            raise ValueError("The book is not in the collection")
        self.books.remove(book)
        # remove to collections json file

    def print_collection(self):
        for b in self.books:
            print(b.get_book_details())

    # TODO: Create method to serialise and deserialise a book object


# TODO: create library class
# Library class works as the headmaster to manage collections and books
# class Library:
# def __int__(self):
# load up GUI
# let user see collctions to view
# let user click collections and books to makr as read
# load collections
# add collection
# delete collection
# add book to this collection
# remove book from this collection


# class for creating a exception when trying to add a duplicate
class DuplicateError(Exception):
    """Custom exception raised when a duplicate item is added."""
    pass

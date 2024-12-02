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

    # TODO add function that notes a book is read(removes from collections and adds to the read list)

    def get_book_details(self):
        return f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}"


# This class will represent a collection of books.
# It will provide functionality to add and remove books, and sort them
# how the user customizes.
# Will need to figure out how to book books from one collection to another ones read
class BookCollection:
    def __init__(self):
        self.books = []  # Initialize the empty list

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be added")
        self.books.append(book)
        self.books.sort(key=lambda x: x.author)  # Sorts the books everytime another book is added

    # TODO Test this function
    def remove_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be removed")
        if book not in self.books:
            raise ValueError("The book is not in the collection")
        self.books.remove(book)

    def print_collection(self):
        for b in self.books:
            print(b.get_book_details())

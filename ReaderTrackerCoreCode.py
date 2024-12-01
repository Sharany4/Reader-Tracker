# In this file I am creating the core functionality for my project


# My initial implementation will be to make the user
# able to add and remove from a tobe read list ,and move to a read list.
# Later this will be expanded so the can create custom lists.


# TODO Create a Book class
# This class will have a title, author, year
# It will also store what collections it is apart of
# It will also have a to string method to represent itself
class Book:
    def __init__(self, title: str, author: str, year: int):
        if not title or not author or not year:
            raise ValueError("Title, author and year must not be empty")

        self.title = title
        self.author = author
        self.year = year

    def printBook(self):
        print(f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}")

# TODO Create a BookCollection class
# This class will represent a collection of books.
# It will provide functionality to add and remove books, and sort them
# how the user customizes.
# Will need to figure out how to book books from one collection to another ones read

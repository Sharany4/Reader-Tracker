# This class handles the storage if done through json.
from abc import ABC

from ReaderTrackerCoreCode import Book
from Storage import Storage


class JsonStorage(Storage, ABC):
    def __int__(self, base_folder: str):
        self.base_folder = base_folder

    def add_book_to_storage(self, book: Book, user_id: str, collection = "books"):
        """
        Adds a book to the storage for a specific user.
        """
        pass


    def remove_book_from_storage(self, book: Book, user_id: str):
        """
        Removes a book from the storage for a specific user.
        """
        pass

    def add_collection_to_storage(self, collection: list, user_id: str):
        """
        Adds a collection of books to the storage for a specific user.
        """
        pass

    def remove_collection_from_storage(self, collection: list, user_id: str):
        """
        Removes a collection of books from the storage for a specific user.
        """
        pass

    def add_user_to_storage(self, user_id: str):
        """
        Adds a new user to the storage system.
        """
        pass

    def remove_user_from_storage(self, user_id: str):
        """
        Removes a user from the storage system.
        """
        pass


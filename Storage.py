from abc import ABC, abstractmethod

from ReaderTrackerCoreCode import Book, BookCollection


# This class is an abstract class that will have abstract methods
# that each storage type will need to define. I have done this
# because I want to be able to extend this project to incorporate
# databases later on. For the basic functionality, I am using JSON
# as I understand how it works. After the basic function of the
# project is finished, I will focus on incorporating databases.
class Storage(ABC):
    @abstractmethod
    def add_book_to_storage(self, book: Book, user_id: str):
        """
        Adds a book to the storage for a specific user.
        """
        pass

    @abstractmethod
    def remove_book_from_storage(self, book: Book, user_id: str):
        """
        Removes a book from the storage for a specific user.
        """
        pass

    @abstractmethod
    def add_collection_to_storage(self, collection: list, user_id: str, collection_name: str):
        """
        Adds a collection of books to the storage for a specific user.
        """
        pass

    @abstractmethod
    def remove_collection_from_storage(self, collection_name: str, user_id: str):
        """
        Removes a collection of books from the storage for a specific user.
        """
        pass

    @abstractmethod
    def add_user_to_storage(self, user_id: str):
        """
        Adds a new user to the storage system.
        """
        pass

    @abstractmethod
    def remove_user_from_storage(self, user_id: str):
        """
        Removes a user from the storage system.
        """
        pass

    @abstractmethod
    def load_collection_from_storage(self, user_id: str, collection_name: str) -> BookCollection:
        """
        Loads a collection of books from the file
        """
        pass

    @abstractmethod
    def load_all_collections_from_storage(self, user_id: str) -> list:
        """
        Loads all collections for a specific user from storage.
        Returns a dictionary where the keys are collection names and the values are lists of Book objects.
        """
        pass

    @abstractmethod
    def get_list_of_collection_names(self, user_id: str) -> list:
        """
        Get list of collections so the user can pick
        """
        pass

# This class handles the storage if done through json.
import json
import os.path
from abc import ABC

from ReaderTrackerCoreCode import Book
from Storage import Storage


class JsonStorage(Storage, ABC):
    def __int__(self, base_folder: str):
        self.base_folder = base_folder  # folder that contains all users folders
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def get_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return user_folder

    def add_book_to_storage(self, book: Book, user_id: str, collection="books"):
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection}.json")

        # create the collection if it doesn't exist
        if not os.path.exists(collection_path):
            with open(collection_path, 'w') as f:
                json.dump([], f)

        # load the collection data
        with open(collection_path, 'r') as f:
            collection_data = json.load(f)

        if book.to_dict() not in collection_data:
            collection_data.append(book.to_dict())
            with open(collection_path, 'w') as f:
                json.dump(collection_data, f)

    def remove_book_from_storage(self, book: Book, user_id: str, collection='books', remove_from_all_collections=False):
        user_folder = self.get_user_folder(user_id)

        # Get all JSON files in the user's folder (assuming collections are stored as JSON files)
        collection_files = [f for f in os.listdir(user_folder) if f.endswith('.json')]

        # If remove_from_all_collections is True, process all collection files
        if remove_from_all_collections:
            collections = collection_files
        else:
            collections = [f"{collection}.json"]  # Only the specified collection

        for collection in collections:
            collection_path = os.path.join(user_folder, collection)
            if os.path.exists(collection_path):
                with open(collection_path, 'r') as f:
                    collection_data = json.load(f)

                book_dict = book.to_dict()
                if book_dict in collection_data:
                    collection_data.remove(book_dict)
                    with open(collection_path, 'w') as f:
                        json.dump(collection_data, f)

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

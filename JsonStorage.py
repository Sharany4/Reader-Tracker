# This class handles the storage if done through json.
import json
import os.path
from abc import ABC

from ReaderTrackerCoreCode import Book, BookCollection
from Storage import Storage


class JsonStorage(Storage, ABC):
    def __init__(self, base_folder: str):
        self.base_folder = base_folder  # folder that contains all users folders
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def get_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return user_folder

    def add_book_to_storage(self, book: Book, user_id: str, collection="books"): # May be redundant as all books are in collections
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

    def remove_book_from_storage(self, book: Book, user_id: str, collection='books', remove_from_all_collections=False): # Will be useful
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

    def add_collection_to_storage(self, collection: BookCollection, user_id: str):
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection.name}.json")

        # Serialize the collection and write it to the storage file
        try:
            with open(collection_path, 'w') as f:
                # Serialize books in the collection
                collection_data = {
                    "name": collection.name,
                    "books": [book.to_dict() for book in collection.books]
                }
                json.dump(collection_data, f, indent=4)
        except IOError as e:
            print(f"Error saving collection '{collection.name}' to storage: {e}")

    def remove_collection_from_storage(self, collection_name: str, user_id: str):
        user_folder = self.get_user_folder(user_id)
        collection_file = f"{collection_name}.json"
        collection_path = os.path.join(user_folder, collection_file)

        if os.path.exists(collection_path):
            os.remove(collection_path)

    def add_user_to_storage(self, user_id: str):
        self.get_user_folder(user_id)  # Ensure the user's folder is created

    def remove_user_from_storage(self, user_id: str):
        user_folder = self.get_user_folder(user_id)

        if os.path.exists(user_folder):
            for file in os.listdir(user_folder):
                file_path = os.path.join(user_folder, file)
                os.remove(file_path)
            os.rmdir(user_folder)

    def load_collection_from_storage(self, user_id: str, collection_name: str) -> BookCollection:
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        try:
            with open(collection_path, 'r') as f:
                collection_data = json.load(f)

            # Create a new BookCollection object
            collection = BookCollection(collection_name=collection_data["name"])

            # Add each book back into the collection
            for book_data in collection_data["books"]:
                book = Book.from_dict(book_data)  # Recreate the Book object
                collection.add_book(book)  # Add the book back to the collection

            return collection
        except IOError as e:
            print(f"Error loading collection '{collection_name}' from storage: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for collection '{collection_name}': {e}")
            return None

    def get_list_of_collection_names(self, user_id: str) -> list:
        """
        Get list of collections so the user can pick
        """
        pass

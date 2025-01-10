# This class handles the storage if done through json.
import json
import os.path
from abc import ABC

from ReaderTrackerCoreCode import Book, BookCollection
from Storage import Storage

"""
The json storage is a sotrage option for the app.
This will work by a base folder being passed which is based in the prject folder.
In this folder will be a folder for each user.
Then there will be json files to store collections for each user. 
"""


class JsonStorage(Storage, ABC):
    def __init__(self, base_folder: str):
        self.base_folder = base_folder  # folder that contains all users folders
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

        # Create a JSON file for usernames inside the test folder
        self.users_file = os.path.join(self.base_folder, "users.json")
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({"users": []}, f)


    # TODO: test if the user is invalid
    # todo: test that the user folder exists
    # if it is invalid, raise an error
    def get_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if not os.path.exists(user_folder):
            raise FileNotFoundError(f"User '{user_id}' does not exist")
        return user_folder

    # test that the user folder is created
    # test the folder wased created before
    def create_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if os.path.exists(user_folder):
            raise FileExistsError(f"User '{user_id}' already exists")
        os.makedirs(user_folder)
        return user_folder

    # test that he user is not already in the storage
    # test that the user is added to the user file
    def add_user_to_storage(self, user_id: str):
        if os.path.exists(os.path.join(self.base_folder, user_id)):
            raise FileExistsError(f"User '{user_id}' already exists")
        user_folder = self.create_user_folder(user_id)  # Ensure the user's folder is created

        # Create a JSON file for the names of collections
        # I dont think this is needed as we can get the names from the files in the folder
        collections_file = os.path.join(user_folder, 'collections.json')
        with open(collections_file, 'w') as f:
            json.dump([], f)  # Initialize with an empty list

        # Create a JSON file for books
        books_file = os.path.join(user_folder, 'books.json')
        with open(books_file, 'w') as f:
            json.dump({"name": "books", "books": []}, f)  # Initialize with the correct format

        # Create a JSON file for read books
        read_file = os.path.join(user_folder, 'read.json')
        with open(read_file, 'w') as f:
            json.dump({"name": "read", "books": []}, f)  # Initialize with the correct format

        # Add the user to the users file
        with open(self.users_file, 'r') as f:
            users_data = json.load(f)
        if user_id not in users_data["users"]:
            users_data["users"].append(user_id)
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=4)






    # TODO: needs to be tested
    # TODO: test that the names can be used to get collections from files
    # TODO: if invalid user, raise an error
    def get_list_of_collection_names(self, user_id: str) -> list:
        user_folder = self.get_user_folder(user_id)
        collection_files = [f for f in os.listdir(user_folder) if f.endswith('.json')]
        collection_names = [os.path.splitext(f)[0] for f in collection_files]
        return collection_names

    # TODO: test that the user is valid
    def remove_user_from_storage(self, user_id: str):
        user_folder = self.get_user_folder(user_id)

        if os.path.exists(user_folder):
            for file in os.listdir(user_folder):
                file_path = os.path.join(user_folder, file)
                os.remove(file_path)
            os.rmdir(user_folder)

    # TODO: test that the book gets added to collection and books, even if no collection is specified
    # TODO: test that the book is not added to the collection if it is already there
    def add_book_to_storage(self, book: Book, user_id: str,
                            collection_name="books"):  # May be redundant as all books are in collections
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        # create the collection if it doesn't exist
        if not os.path.exists(collection_path):
            with open(collection_path, 'w') as f:
                json.dump({"name": collection_name, "books": []}, f)

        # load the collection data
        try:
            with open(collection_path, 'r') as f:
                collection_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON for collection '{collection_name}': {e}")

        # Ensure collection_data is a list of dictionaries
        if not isinstance(collection_data["books"], list):
            raise ValueError("Collection data should be a list, the type is: " + str(type(collection_data["books"])))

        # Check if the book is already in the collection
        if book.to_dict() not in collection_data["books"]:
            collection_data["books"].append(book.to_dict())
            with open(collection_path, 'w') as f:
                json.dump(collection_data, f, indent=4)

    # TODO: test the book is removed from the collections and the books
    # TODO: test error is raised if the book is not in the collection
    # TODO: test that error is raised is collection path is invalid
    def remove_book_from_storage(self, book: Book, user_id: str, collection_name='books',
                                 remove_from_all_collections=False):  # Will be useful
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        # Check if the collection exists
        if not os.path.exists(collection_path):
            raise FileNotFoundError(f"Collection '{collection_name}' does not exist for user '{user_id}'")

        # Extract the book data from the collection
        try:
            with open(collection_path, 'r') as f:
                collection_data = json.load(f)

            # Ensure collection_data is a dictionary with a "books" key

            if not isinstance(collection_data, dict) or "books" not in collection_data:
                raise ValueError("Collection data should be a dictionary with a 'books' key")

            # Remove the book from the collection
            book_dict = book.to_dict()
            if book_dict in collection_data["books"]:
                collection_data["books"].remove(book_dict)

            # Write the updated collection data back to the JSON file
            with open(collection_path, 'w') as f:
                json.dump(collection_data, f, indent=4)

            # Remove the book from all collections if specified
            if remove_from_all_collections:
                for collection_file in os.listdir(user_folder):
                    if collection_file.endswith('.json') and collection_file != f"{collection_name}.json":
                        collection_path = os.path.join(user_folder, collection_file)
                        with open(collection_path, 'r') as f:
                            collection_data = json.load(f)

                        if isinstance(collection_data, dict) and "books" in collection_data:
                            if book_dict in collection_data["books"]:
                                collection_data["books"].remove(book_dict)

                            with open(collection_path, 'w') as f:
                                json.dump(collection_data, f, indent=4)

        except IOError as e:
            raise IOError(f"Error removing book from collection '{collection_name}' for user '{user_id}': {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON for collection '{collection_name}': {e}")

    # TODO: test that the collection is added to the collections folder
    # TODO: test that error is raised if the collection already exists
    # TODO: test collection can be converted back to a collection object
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
            raise IOError(f"Error saving collection '{collection.name}' to storage: {e}")

    # TODO: test that the collection is removed from the user folder
    # TODO: test that error is raised if the collection does not exist
    def remove_collection_from_storage(self, collection_name: str, user_id: str):
        user_folder = self.get_user_folder(user_id)
        collection_file = f"{collection_name}.json"
        collection_path = os.path.join(user_folder, collection_file)

        if os.path.exists(collection_path):
            os.remove(collection_path)

    # TODO: test that the collection is loaded correctly into a collection object
    # TODO: test that error is raised if the collection does not exist
    # TODO: test that error is raised if the JSON data is invalid
    # TODO: test that the books are the same
    def load_collection_from_storage(self, user_id: str, collection_name: str) -> BookCollection:
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        try:
            with open(collection_path, 'r') as f:
                collection_data = json.load(f)

            # Create a new BookCollection object
            collection = BookCollection(collection_data["name"])

            # Add each book back into the collection
            for book_data in collection_data["books"]:
                book = Book.from_dict(book_data)  # Recreate the Book object
                collection.add_book(book)  # Add the book back to the collection

            return collection
        except IOError as e:
            raise IOError(f"Error loading collection '{collection_name}' from storage: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON for collection '{collection_name}': {e}")

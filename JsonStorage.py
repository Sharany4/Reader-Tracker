# This class handles the storage if done through json.
import json
import os.path
from abc import ABC

from ReaderTrackerCoreCode import Book, BookCollection
from Storage import Storage

"""
The json storage is a storage option for the app.
This will work by a base folder being passed which is based in the project folder.
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

    def get_user_list(self):
        with open(self.users_file, 'r') as f:
            users_data = json.load(f)
        return users_data["users"]

    def get_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if not os.path.exists(user_folder):
            raise FileNotFoundError(f"User '{user_id}' does not exist")
        return user_folder

    def create_user_folder(self, user_id: str):
        user_folder = os.path.join(self.base_folder, user_id)
        if os.path.exists(user_folder):
            raise FileExistsError(f"User '{user_id}' already exists")
        os.makedirs(user_folder)
        return user_folder

    def add_user_to_storage(self, user_id: str):
        if os.path.exists(os.path.join(self.base_folder, user_id)):
            raise FileExistsError(f"User '{user_id}' already exists")
        user_folder = self.create_user_folder(user_id)  # Ensure the user's folder is created

        # Create a JSON file for the names of collections
        # I dont think this is needed as we can get the names from the files in the folder
        collections_file = os.path.join(user_folder, 'collections.json')
        with open(collections_file, 'w') as f:
            json.dump({"names": []}, f)  # Initialize with an empty list

        # Create a JSON file for books
        books_file = os.path.join(user_folder, 'books.json')
        with open(books_file, 'w') as f:
            json.dump({"name": "books", "books": []}, f)  # Initialize with the correct format
        # The books file and read file wiull not be added to collections file to prevent user from deleting them

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

    def remove_user_from_storage(self, user_id: str):
        user_folder = self.get_user_folder(user_id)

        if not os.path.exists(user_folder):
            raise FileNotFoundError(f"User '{user_id}' does not exist")

        # Remove the user from the users file
        for file in os.listdir(user_folder):
            file_path = os.path.join(user_folder, file)
            os.remove(file_path)
        os.rmdir(user_folder)

        # Remove the user from the users file
        with open(self.users_file, 'r') as f:
            users_data = json.load(f)
        if user_id not in users_data["users"]:
            raise ValueError(f"User '{user_id}' is not in the users file")
        else:
            users_data["users"].remove(user_id)
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=4)

    def add_book_to_storage(self, book: Book, user_id: str,
                            collection_name="books"):  # May be redundant as all books are in collections
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        if not os.path.exists(os.path.join(self.base_folder, user_id)):
            raise FileNotFoundError(f"User '{user_id}' does not exist")

        if not os.path.exists(collection_path):
            raise FileNotFoundError(f"Collection '{collection_name}' does not exist for user '{user_id}'")

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
        for b in collection_data["books"]:
            if b["title"] == book.title and b["author"] == book.author and b["year"] == book.year:
                raise ValueError(f"Book '{book.title}' is already in the collection '{collection_name}'")

        collection_data["books"].append(book.to_dict())
        with open(collection_path, 'w') as f:
            json.dump(collection_data, f, indent=4)
        # The collection is added to the book in AppFunctionCode 'on_add_book' function

    def remove_book_from_storage(self, book: Book, user_id: str, collection_name='books',
                                 remove_from_all_collections=False):  # Will be useful
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection_name}.json")

        if not os.path.exists(os.path.join(self.base_folder, user_id)):
            raise FileNotFoundError(f"User '{user_id}' does not exist")

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
            # book.add_collection(collection_name)
            book_dict = book.to_dict()  # From before changing the data
            '''if book_dict not in collection_data["books"]:
                print("collection_data", collection_data)
                raise ValueError(f"Book '{book.title}' is not in the collection", collection_name)
            collection_data["books"].remove(book_dict)'''

            # Remove the book from the collection
            book_found = False
            for stored_book in collection_data["books"]:
                if stored_book["title"] == book.title and stored_book["author"] == book.author and stored_book[
                    "year"] == book.year:
                    collection_data["books"].remove(stored_book)
                    book_found = True
                    break
            if not book_found:
                print("collection_data, book not found", collection_data)
                raise ValueError(f"Book '{book.title}' is not in the collection '{collection_name}'")

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
                            for b in collection_data["books"]:
                                if b["title"] == book.title and b["author"] == book.author and b["year"] == book.year:
                                    collection_data["books"].remove(book_dict)

                            with open(collection_path, 'w') as f:
                                json.dump(collection_data, f, indent=4)

        except IOError as e:
            raise IOError(f"Error removing book from collection '{collection_name}' for user '{user_id}': {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON for collection '{collection_name}': {e}")

        # TODO: remove the collection to the book in the books file

    def add_collection_to_storage(self, collection: BookCollection, user_id: str):
        user_folder = self.get_user_folder(user_id)
        collection_path = os.path.join(user_folder, f"{collection.name}.json")

        if os.path.exists(collection_path):
            raise FileExistsError(f"Collection '{collection.name}' already exists for user '{user_id}'")

        users_collections_names_file = os.path.join(user_folder, 'collections.json')
        with open(users_collections_names_file, 'r') as f:
            collection_names = json.load(f)
            if collection.name in collection_names:
                raise ValueError(f"Collection '{collection.name}' already exists for user '{user_id}'")
            collection_names["names"].append(collection.name)
        with open(users_collections_names_file, 'w') as f:
            json.dump(collection_names, f, indent=4)

        # Add any missing books to storage
        for book in collection.books:
            try:
                self.add_book_to_storage(book, user_id)
            except ValueError:
                # Book is already in storage, continue
                pass

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

    def remove_collection_from_storage(self, collection_name: str, user_id: str):
        user_folder = self.get_user_folder(user_id)
        collection_file = f"{collection_name}.json"
        collection_path = os.path.join(user_folder, collection_file)

        if not os.path.exists(collection_path):
            raise FileNotFoundError(f"Collection '{collection_name}' does not exist for user '{user_id}'")

        os.remove(collection_path)
        users_collections_names_file = os.path.join(user_folder, 'collections.json')
        with open(users_collections_names_file, 'r') as f:
            collection_names = json.load(f)
            if collection_name not in collection_names["names"]:
                raise ValueError(f"Collection '{collection_name}' does not exist for user '{user_id}'")
            collection_names["names"].remove(collection_name)
        with open(users_collections_names_file, 'w') as f:
            json.dump(collection_names, f, indent=4)

        # TODO: remove the collection from the books file for the books
        '''
        if a collection is removed from storage, we also have to remove it from the book thati s tracking it
        Since the list of the collections for that books are only in books.json, this is the only place it needs to be removed
        '''

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

    def get_list_of_collection_names(self, user_id: str) -> list:
        # get the collection names from the collections file
        user_folder = self.get_user_folder(user_id)
        collections_file = os.path.join(user_folder, 'collections.json')
        with open(collections_file, 'r') as f:
            collection_names = json.load(f)
        print(collection_names["names"])
        return collection_names["names"]

    def add_collection_to_book_storage(self, book: Book, coll_name: str, user_id: str):
        user_folder = self.get_user_folder(user_id)
        books_file = os.path.join(user_folder, 'books.json')
        with open(books_file, 'r') as f:
            books_data = json.load(f)
            # print("from add collection to book storage, the books in file", books_data["books"])

        for b in books_data["books"]:
            if b["title"] == book.title and b["author"] == book.author and b["year"] == book.year:
                print("found book" + book.get_book_details() + " in books file")
                print(b["collections"])
                b["collections"].append(coll_name)
                with open(books_file, 'w') as f:
                    json.dump(books_data, f, indent=4)
                return True

        print("didnt find the book" + book.get_book_details())
        print(books_data["books"])
        return False

        # check to see if the book is in , if so, throw error
        # else, add the coll

    def get_books_collections(self, book: Book, user_id: str):
        user_folder = self.get_user_folder(user_id)
        books_file = os.path.join(user_folder, 'books.json')
        with open(books_file, 'r') as f:
            books_data = json.load(f)

        for b in books_data["books"]:
            if b["title"] == book.title and b["author"] == book.author and book.year:
                print("found book" + book.get_book_details() + " in books file")
                print("the books collections: ", b["collections"])
                return b["collections"]

        raise ValueError("book is not in storage but are trying to get its collections")

        # print("the books data" + books_data["books"])
        # print("the book colls: " + books_data["collections"])
        # return books_data["collections"]

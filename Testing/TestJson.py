# This file is for all the testing for converting to and from JSON
import json
import os
import shutil
import unittest

from JsonStorage import JsonStorage
from ReaderTrackerCoreCode import Book, BookCollection


class TestingJSON(unittest.TestCase):

    # This method is called before each test to create the necessary files and folders
    def setUp(self):
        # Create a temporary folder for testing
        self.test_folder = 'test_folder'
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)
        os.makedirs(self.test_folder)

        # Initialize the JSON storage with the test folder
        self.storage = JsonStorage(self.test_folder)

        # Create user folder inside the test folder and add user to the JSON file
        self.storage.add_user_to_storage("test_user")

        # Initialize test data

    # self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
    # self.test_book = Book("Fake title", "Fake author", 1000)
    # self.storage.add_book_to_storage(self.test_book, "test_user", "test_collection")

    def tearDown(self):
        # Remove the temporary folder after tests
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_can_create_json_storage(self):
        test_storage = JsonStorage("test_folder")

    def test_json_storage_has_correct_files(self):
        # Check that the users file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "users.json")))


    def test_getting_user_folder_with_invalid_username(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.get_user_folder("non_existent_user")

    def test_getting_user_folder_with_valid_username_returns_path(self):
        user_folder = self.storage.get_user_folder("test_user")
        self.assertEqual(user_folder, os.path.join(self.test_folder, "test_user"))

    def test_can_add_a_book_to_storage(self):
        # seeing what was in it before
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")
        test_book = Book("Fake title", "Fake author", 1000)
        with open(user_books_path, 'r') as f:
            books_data_before = json.load(f)
        print("Before adding book: ", books_data_before)
        self.assertNotIn(test_book.to_dict(), books_data_before["books"])

        self.storage.add_book_to_storage(test_book, "test_user", "books")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data_after = json.load(f)
        print("After adding book: ", books_data_after)

        # Check that the book's details are in the books data
        self.assertIn(test_book.to_dict(), books_data_after["books"])

    def test_create_user_folder(self):
        user_folder = self.storage.get_user_folder("test_user")
        self.assertTrue(os.path.exists(user_folder))

    # -------------------------------------------------------------
    def test_create_user_folder_with_existing_folder_raises_error(self):
        with self.assertRaises(FileExistsError):
            self.storage.create_user_folder("test_user")

    def test_create_user_folder_returns_correct_path(self):
        user_folder = self.storage.create_user_folder("new_user")
        self.assertEqual(user_folder, os.path.join(self.test_folder, "new_user"))

    def test_add_user_to_storage_creates_user_folder(self):
        self.storage.add_user_to_storage("new_user")
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "new_user")))

    def test_can_create_a_user_with_correct_initial_files(self):
        # Check that the user folder was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user")))

        # Check that the collections file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "collections.json")))

        # Check that the books file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "books.json")))

    def test_add_user_to_storage_raised_error_if_user_exists(self):
        with self.assertRaises(FileExistsError):
            self.storage.add_user_to_storage("test_user")

    def test_add_user_to_storage_adds_user_to_users_file(self):
        # Check that the user is in the users file
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        self.assertIn("test_user", users_data["users"])

    # -------------------------------------------------------------
    def test_can_remove_a_book_from_storage(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")

        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_book_to_storage(test_book, "test_user", "books")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        print("After adding book: ", books_data)

        # Check that the book's details are in the books data
        self.assertIn(test_book.to_dict(), books_data["books"])

        # Remove the book from the storage
        self.storage.remove_book_from_storage(test_book, "test_user")

        with open(user_books_path, 'r') as f:
            books_data_rem = json.load(f)
        print("After removing book: ", books_data_rem)
        self.assertNotIn(test_book.to_dict(), books_data_rem["books"])

    # TODO: test what happens with invalid username

    def test_can_add_a_collection_to_storage(self):
        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "test_collection.json")))

    # TODO: test what happens with invalid username

    def test_can_remove_a_collection_from_storage(self):
        collection_path = os.path.join(self.test_folder, "test_user", "test_collection.json")

        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
        self.assertTrue(os.path.exists(collection_path))

        self.storage.remove_collection_from_storage("test_collection", "test_user")
        self.assertFalse(os.path.exists(collection_path))

    # TODO: test what happens with invalid username

    def test_can_load_a_collection_from_storage(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)

        self.storage.add_collection_to_storage(test_collection, "test_user")

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")

        # Check that the loaded collection is the same as the original
        self.assertEqual(loaded_collection.name, test_collection.name)
        self.assertEqual(loaded_collection.books[0].to_dict(), test_collection.books[0].to_dict())

    # TODO: test what happens with invalid username

    def test_to_load_a_collection_not_present(self):
        with self.assertRaises(IOError):
            self.storage.load_collection_from_storage("test_user", "non_existent_collection")

    def test_json_decoder_error(self):
        # Create a file with invalid JSON data
        invalid_json_path = os.path.join(self.test_folder, "test_user", "invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("Invalid JSON data")

        # Try to load the invalid JSON file
        with self.assertRaises(ValueError):
            self.storage.load_collection_from_storage("test_user", "invalid")

    # Needs to be fixed
    def test_read_book_adds_to_read_and_removed_from_collections(self):
        # Create a collection and add a book to it
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)

        # Add the collection to the storage
        self.storage.add_collection_to_storage(test_collection, "test_user")

        # Test the book is in the collection
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        loaded_read_books = self.storage.load_collection_from_storage("test_user", "read")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_read_books.books])

        # Mark the book as read
        test_book.note_book_as_read(self.storage, "test_user")

        # Load the collection from storage
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        loaded_read_books = self.storage.load_collection_from_storage("test_user", "read")

        # Check that the book is in the read list
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_read_books.books])

        # Check that the book is not in the collection
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])

    # Tests to be done are written in the json storage file


if __name__ == '__main__':
    unittest.main()

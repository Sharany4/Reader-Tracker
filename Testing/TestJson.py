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

    def tearDown(self):
        # Remove the temporary folder after tests
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def test_can_create_json_storage(self):
        test_storage = JsonStorage("test_folder")

    def test_json_storage_has_correct_files(self):
        # Check that the users file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "users.json")))

    # ----------------------------------------------------------------

    def test_getting_user_folder_with_invalid_username_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.get_user_folder("non_existent_user")

    def test_getting_user_folder_with_valid_username_returns_path(self):
        user_folder = self.storage.get_user_folder("test_user")
        self.assertEqual(user_folder, os.path.join(self.test_folder, "test_user"))
        self.assertTrue(os.path.exists(user_folder))

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

    def test_user_added_to_user_file_after_add_user_to_storage(self):
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        self.assertNotIn("new_user", users_data["users"])
        self.storage.add_user_to_storage("new_user")
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        self.assertIn("new_user", users_data["users"])

    # -------------------------------------------------------------

    def test_remove_user_from_storage_removes_user_folder(self):
        user_folder = self.storage.get_user_folder("test_user")

        # print out content of user file
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        print("Before removing user: ", users_data)
        self.assertTrue(os.path.exists(user_folder))

        self.storage.remove_user_from_storage("test_user")

        # print out content of user file
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        print("After removing user: ", users_data)
        self.assertFalse(os.path.exists(user_folder))

    def test_remove_user_from_storage_removes_user_from_users_file(self):
        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        self.assertIn("test_user", users_data["users"])

        self.storage.remove_user_from_storage("test_user")

        with open(os.path.join(self.test_folder, "users.json"), 'r') as f:
            users_data = json.load(f)
        self.assertNotIn("test_user", users_data["users"])

    def test_remove_user_from_storage_raises_error_if_user_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.remove_user_from_storage("non_existent_user")

    # -------------------------------------------------------------

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

    def test_book_added_to_books_file_if_no_collection_specified(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")
        test_book = Book("Fake title", "Fake author", 1000)

        # Check the book is not in the books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertNotIn(test_book.to_dict(), books_data["books"])

        self.storage.add_book_to_storage(test_book, "test_user")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertIn(test_book.to_dict(), books_data["books"])

    def test_add_book_to_storage_book_raises_error_if_already_present(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")
        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_book_to_storage(test_book, "test_user")

        # Check the book is in the books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertIn(test_book.to_dict(), books_data["books"])
        print("After adding book once: ", books_data)

        # Try to add the book again
        with self.assertRaises(ValueError):
            self.storage.add_book_to_storage(test_book, "test_user")

    def test_book_added_if_not_present(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")
        test_book = Book("Fake title", "Fake author", 1000)

        # Check the book is not in the books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertNotIn(test_book.to_dict(), books_data["books"])

        self.storage.add_book_to_storage(test_book, "test_user")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertIn(test_book.to_dict(), books_data["books"])
        print("After adding book once: ", books_data)

    def test_add_book_to_storage_raises_error_if_invalid_user(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.add_book_to_storage(Book("Fake title", "Fake author", 1000), "non_existent_user")

    def test_add_book_to_storage_raises_error_if_invalid_collection(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.add_book_to_storage(Book("Fake title", "Fake author", 1000), "test_user",
                                             "non_existent_collection")

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

    def test_remove_book_from_storage_throws_error_if_book_not_present(self):
        with self.assertRaises(ValueError):
            self.storage.remove_book_from_storage(Book("Fake title", "Fake author", 1000), "test_user")

    def test_remove_book_from_storage_raises_error_if_invalid_user(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.remove_book_from_storage(Book("Fake title", "Fake author", 1000), "non_existent_user")

    def test_remove_book_from_storage_raises_error_if_invalid_collection(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.remove_book_from_storage(Book("Fake title", "Fake author", 1000), "test_user",
                                                  "non_existent_collection")

    def test_remove_book_from_storage_removes_book_if_present(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")

        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_book_to_storage(test_book, "test_user", "books")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertIn(test_book.to_dict(), books_data["books"])

        # Remove the book from the storage
        self.storage.remove_book_from_storage(test_book, "test_user")

        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        self.assertNotIn(test_book.to_dict(), books_data["books"])

    # TODO: make sure test works still after testing add collection to storage
    def test_remove_book_from_storage_can_remove_book_from_all_collections(self):
        # Create a collection and add a book to it
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        # Check that the book is not present in both collections
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])
        loaded_book_collection = self.storage.load_collection_from_storage("test_user", "books")
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_book_collection.books])

        # Add the book to the collection
        self.storage.add_book_to_storage(test_book, "test_user")  # adds to books.json
        test_collection.add_book_with_storage(test_book, self.storage, "test_user")  # adds to test_collection.json

        # Check that the book is in both collections
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])
        loaded_book_collection = self.storage.load_collection_from_storage("test_user", "books")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_book_collection.books])

        # Remove the book from the storage
        self.storage.remove_book_from_storage(test_book, "test_user", "books", remove_from_all_collections=True)

        # Check that the book is not in both collections
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])
        loaded_book_collection = self.storage.load_collection_from_storage("test_user", "books")
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_book_collection.books])

    # -------------------------------------------------------------

    def test_can_add_a_collection_to_storage(self):
        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "test_collection.json")))

    def test_add_collection_to_storage_raises_error_if_collection_already_present(self):
        with self.assertRaises(FileExistsError):
            self.storage.add_collection_to_storage(BookCollection("books"), "test_user")

    def test_add_collection_to_storage_raises_error_if_invalid_user(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.add_collection_to_storage(BookCollection("test_collection"), "non_existent_user")

    def test_add_collection_to_storage_adds_collection_to_collections_file(self):
        with open(os.path.join(self.test_folder, "test_user", "collections.json"), 'r') as f:
            collections_names_data = json.load(f)
        self.assertNotIn("test_collection", collections_names_data["names"])

        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")

        with open(os.path.join(self.test_folder, "test_user", "collections.json"), 'r') as f:
            collections_data = json.load(f)
        self.assertIn("test_collection", collections_data["names"])

    def test_add_collection_updates_if_books_are_added(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_collection_to_storage(test_collection, "test_user")
        # Cant call add book to storage if collection is not added to storage
        test_collection.add_book_with_storage(test_book, self.storage, "test_user")

        # Check that the book is in the collection
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])

    def test_add_collection_to_storage_will_add_books_already_in_collection(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        # Check that the book is in the collection
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])

    def test_add_collection_will_update_if_books_are_removed(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        # Check that the book is in the collection
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])

        # Remove the book from the collection
        test_collection.remove_book_with_storage(test_book, self.storage, "test_user")

        # Check that the book is not in the collection
        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertNotIn(test_book.to_dict(), [book.to_dict() for book in loaded_collection.books])

    def test_add_collection_to_storage_raises_error_if_invalid_collection_name(self):
        with self.assertRaises(ValueError):
            self.storage.add_collection_to_storage(BookCollection(""), "test_user")

    def test_add_collection_to_storage_raises_error_if_invalid_username(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.add_collection_to_storage(BookCollection("test_collection"), "non_existent_user")

    def test_add_collection_to_storage_raises_error_if_collection_already_exists(self):
        with self.assertRaises(FileExistsError):
            self.storage.add_collection_to_storage(BookCollection("books"), "test_user")

    def test_add_collection_to_storage_can_let_us_extract_the_data(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)

        test_collection.add_book(test_book)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        with open(os.path.join(self.test_folder, "test_user", "test_collection.json"), 'r') as f:
            collection_data = json.load(f)
        self.assertEqual(collection_data["name"], "test_collection")
        self.assertEqual(collection_data["books"][0], test_book.to_dict())

    def test_add_collection_throws_error_if_collection_name_empty(self):
        with self.assertRaises(ValueError):
            self.storage.add_collection_to_storage(BookCollection(""), "test_user")

    # -------------------------------------------------------------

    def test_can_remove_a_collection_from_storage(self):
        collection_path = os.path.join(self.test_folder, "test_user", "test_collection.json")

        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
        self.assertTrue(os.path.exists(collection_path))

        self.storage.remove_collection_from_storage("test_collection", "test_user")
        self.assertFalse(os.path.exists(collection_path))

    def test_remove_collection_from_storage_raises_error_if_invalid_user(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.remove_collection_from_storage("test_collection", "non_existent_user")

    def test_remove_collection_from_storage_raises_error_if_invalid_collection(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.remove_collection_from_storage("non_existent_collection", "test_user")

    def test_remove_collection_from_storage_removes_collection_from_collections_file(self):
        self.storage.add_collection_to_storage(BookCollection("test_collection"), "test_user")
        with open(os.path.join(self.test_folder, "test_user", "collections.json"), 'r') as f:
            collections_data = json.load(f)
        self.assertIn("test_collection", collections_data["names"])

        self.storage.remove_collection_from_storage("test_collection", "test_user")

        with open(os.path.join(self.test_folder, "test_user", "collections.json"), 'r') as f:
            collections_data = json.load(f)
        self.assertNotIn("test_collection", collections_data["names"])

    # -------------------------------------------------------------
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
    def test_load_a_collection_from_storage_raises_error_if_invalid_user(self):
        with self.assertRaises(FileNotFoundError):
            self.storage.load_collection_from_storage("non_existent_user", "test_collection")

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

    def test_load_collection_from_storage_returns_correct_collection(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)
        self.storage.add_collection_to_storage(test_collection, "test_user")
        user_books_collections = os.path.join(self.test_folder, "test_user", "books.json")
        with open(user_books_collections, 'r') as f:
            books_data = json.load(f)
        self.assertIn(test_book.to_dict(), books_data["books"])

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")

        self.assertEqual(loaded_collection.name, test_collection.name)
        self.assertEqual(loaded_collection.books[0].to_dict(), test_collection.books[0].to_dict())

    def test_load_collection_from_storage_returns_correct_collection_with_multiple_books(self):
        test_collection = BookCollection("test_collection")
        test_book_a = Book("Fake title", "Fake author", 1000)
        test_book_b = Book("Fake title 2", "Fake author 2", 2000)
        test_collection.add_book(test_book_a)
        test_collection.add_book(test_book_b)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")

        self.assertEqual(loaded_collection.name, test_collection.name)
        self.assertEqual(loaded_collection.books[0].to_dict(), test_collection.books[0].to_dict())
        self.assertEqual(loaded_collection.books[1].to_dict(), test_collection.books[1].to_dict())

    def test_load_collection_from_storage_returns_correct_collection_with_no_books(self):
        test_collection = BookCollection("test_collection")
        self.storage.add_collection_to_storage(test_collection, "test_user")

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")

        self.assertEqual(loaded_collection.name, test_collection.name)
        self.assertEqual(loaded_collection.books, test_collection.books)

    def test_load_collection_from_stroage_throws_error_if_data_is_invalid(self):
        # Create a file with invalid JSON data
        invalid_json_path = os.path.join(self.test_folder, "test_user", "invalid.json")
        with open(invalid_json_path, 'w') as f:
            f.write("Invalid JSON data")

        # Try to load the invalid JSON file
        with self.assertRaises(ValueError):
            self.storage.load_collection_from_storage("test_user", "invalid")

    # -------------------------------------------------------------
    def test_can_get_list_of_collection_names(self):
        test_collection = BookCollection("test_collection")
        self.storage.add_collection_to_storage(test_collection, "test_user")

        collection_names = self.storage.get_list_of_collection_names("test_user")
        self.assertIn("test_collection", collection_names)

    def test_list_of_collection_names_gives_names_that_can_be_used_to_load_collections(self):
        test_collection = BookCollection("test_collection")
        self.storage.add_collection_to_storage(test_collection, "test_user")

        collection_names = self.storage.get_list_of_collection_names("test_user")
        self.assertIn("test_collection", collection_names)

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertEqual(loaded_collection.name, "test_collection")

    def test_list_of_collection_names_gives_names_that_can_be_used_to_load_collections_with_multiple_collections(self):
        test_collection_a = BookCollection("test_collection_a")
        test_collection_b = BookCollection("test_collection_b")
        self.storage.add_collection_to_storage(test_collection_a, "test_user")
        self.storage.add_collection_to_storage(test_collection_b, "test_user")

        collection_names = self.storage.get_list_of_collection_names("test_user")
        self.assertIn("test_collection_a", collection_names)
        self.assertIn("test_collection_b", collection_names)

        loaded_collection_a = self.storage.load_collection_from_storage("test_user", "test_collection_a")
        self.assertEqual(loaded_collection_a.name, "test_collection_a")

        loaded_collection_b = self.storage.load_collection_from_storage("test_user", "test_collection_b")
        self.assertEqual(loaded_collection_b.name, "test_collection_b")

    def test_list_of_collection_names_gives_names_that_can_be_used_to_load_collections_with_books(self):
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)
        self.storage.add_collection_to_storage(test_collection, "test_user")

        collection_names = self.storage.get_list_of_collection_names("test_user")
        self.assertIn("test_collection", collection_names)

        loaded_collection = self.storage.load_collection_from_storage("test_user", "test_collection")
        self.assertEqual(loaded_collection.name, "test_collection")
        self.assertEqual(loaded_collection.books[0].to_dict(), test_book.to_dict())

    # -------------------------------------------------------------
    def test_read_book_adds_to_read_and_removed_from_collections(self):
        # Create a collection and add a book to it
        test_collection = BookCollection("test_collection")
        test_book = Book("Fake title", "Fake author", 1000)
        test_collection.add_book(test_book)

        # Add the collection to the storage self.storage.add_book_to_storage(test_book, "test_user") # don't have to
        # do this anymore, taken care of in add collection to storage
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

    # --------------------------------------------------------------
    def test_that_if_new_json_storage_made_data_from_the_folder_persists(self):
        # Create a new JSON storage
        new_storage = JsonStorage(self.test_folder)

        # Check that the user folder is present
        user_folder = new_storage.get_user_folder("test_user")
        self.assertTrue(os.path.exists(user_folder))

        # Check that the collections file is present
        collections_file = os.path.join(user_folder, "collections.json")
        self.assertTrue(os.path.exists(collections_file))

        # Check that the books file is present
        books_file = os.path.join(user_folder, "books.json")
        self.assertTrue(os.path.exists(books_file))

    # --------------------------------------------------------------
    #TODO: adding new function to map the collections to the books in the books file
    # like how the title is stored in the book, have another key in the book that stores the collection names
    # then update the books file when a book is added to a collection
    # in the normal collecton files, the books remain the same
    # the book can then be found in the books file which would have the collection names
if __name__ == '__main__':
    unittest.main()

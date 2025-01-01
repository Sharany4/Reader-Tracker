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
        os.makedirs(self.test_folder, exist_ok=True)

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

    def test_can_create_a_user_with_correct_initial_files(self):
        # Check that the user folder was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user")))

        # Check that the collections file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "collections.json")))

        # Check that the books file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "test_user", "books.json")))

    def test_can_add_a_book_to_storage(self):
        # seeing what was in it before
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")
        with open(user_books_path, 'r') as f:
            books_data_before = json.load(f)
        print("Before adding book: ", books_data_before)

        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_book_to_storage(test_book, "test_user", "books")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data_after = json.load(f)
        print("After adding book: ", books_data_after)

        # Check that the book's details are in the books data
        self.assertIn(test_book.to_dict(), books_data_after)

    def test_can_remove_a_book_from_storage(self):
        user_books_path = os.path.join(self.test_folder, "test_user", "books.json")

        test_book = Book("Fake title", "Fake author", 1000)
        self.storage.add_book_to_storage(test_book, "test_user", "books")

        # Read the contents of the user's books file
        with open(user_books_path, 'r') as f:
            books_data = json.load(f)
        print("After adding book: ", books_data)

        # Check that the book's details are in the books data
        self.assertIn(test_book.to_dict(), books_data)

        # Remove the book from the storage
        self.storage.remove_book_from_storage(test_book, "test_user")

        with open(user_books_path, 'r') as f:
            books_data_rem = json.load(f)
        print("After removing book: ", books_data_rem)

        self.assertNotIn(test_book.to_dict(), books_data_rem)

    # def test_can_add_a_collection_to_storage(self):

    # def test_can_remove_a_collection_from_storage(self):

    # todo: test that json storage is open and closed, data persists

    # TODO : Test that the books serialise properly
    # TODO : Test the the books deserialize properly
    # TODO : Test that a serialised then deserialize book is same as original
    # TODO : Test that a read book is added to the read list ( will use a test json file)
    # TODO : Test that the collection serialises properly
    # TODO : Test the the collection deserializes properly
    # TODO : Test that a serialised then deserialize collection is same as original
    # TODO : Test that a book can be added to a collection and in storage
    # TODO : Test that a book can be removed from a collection and in storage
    # TODO : Test what happens if the book is invalid when serialising
    # TODO : Test what happens if the book is invalid when deserialising
    # TODO : Test when a book is removed, it the book removes the collection from its list
    # TODO : Test that the collection is sorted correctly
    # TODO : Test that the collection is sorted correctly after a book is removed
    # TODO : Test that the collection is sorted correctly after a book is added

    # Once the library is created, the user can add a collection to the library and will be tested here


if __name__ == '__main__':
    unittest.main()

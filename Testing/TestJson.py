# This file is for all the testing for converting to and from JSON
import unittest

from ReaderTrackerCoreCode import Book


class TestingJSON(unittest.TestCase):
    def test_print_in_JSON(self):
        test_book = Book("Test Book", "Sharanya", 2024)
        print(test_book.book_to_json())

    # TODO : Test that the books serialise properly
    # TODO : Test the the books deserialize properly
    # TODO : Test that a serialised then deserialize book is same as original
    # TODO : Test that a read book is added to the read list ( will use a test json file)
    # TODO : Test that the collection serialises properly
    # TODO : Test the the collection deserializes properly
    # TODO : Test that a serialised then deserialize collection is same as original


if __name__ == '__main__':
    unittest.main()

# This file is for all the testing for converting to and from JSON
import unittest

from ReaderTrackerCoreCode import Book


class TestingJSON(unittest.TestCase):
    def test_print_in_JSON(self):
        test_book = Book("Test Book", "Sharanya", 2024)
        print(test_book.book_to_json())


if __name__ == '__main__':
    unittest.main()

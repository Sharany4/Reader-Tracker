# This file will contain tests to test the function of the core code

# Imports
import unittest

from ReaderTrackerCoreCode import Book


# Class for testing the book functionality
class TestBookCreation(unittest.TestCase):
    def test_can_create_a_book(self):
        book = Book("The Alchemist", "Paolo Coelho", 1988)
        book.printBook()

    def test_book_must_have_correct_amount_of_parameters(self):
        # Too few arguments
        with self.assertRaises(TypeError):
            Book("1984", "George Orwell")  # Missing 'year'

        # Too many arguments
        with self.assertRaises(TypeError):
            Book("1984", "George Orwell", 1949, "Extra Param")  # Extra argument

    def test_book_has_all_fields_filled(self):
        with self.assertRaises(ValueError):
            Book("", "", 0)


# TODO: Write tests for book collection
# TODO: Write tests for books with book collection
if __name__ == '__main__':
    unittest.main()

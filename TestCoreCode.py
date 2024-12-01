# This file will contain tests to test the function of the core code

# Imports
import unittest

from ReaderTrackerCoreCode import Book, BookCollection


# Class for testing the book functionality
class TestBookCreation(unittest.TestCase):
    def test_can_create_a_book(self):
        book = Book("The Alchemist", "Paolo Coelho", 1988)
        print(book.get_book_details())

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


# Class for testing the book collection functionality
class TestBookCollection(unittest.TestCase):
    test_book = Book("Fake title", "Fake author", 1000)
    test_book_a = Book("Fake title a", "aaaa", 1000)
    test_book_b = Book("Fake title b", "bbbb", 1000)
    test_book_c = Book("Fake title c", "cccc", 1000)
    correct_list_ab = [test_book_a, test_book_b]
    correct_list_abc = [test_book_a, test_book_b, test_book_c]

    def test_can_create_a_collection(self):
        book_coll = BookCollection()
        book_coll.print_collection()

    def test_collection_takes_no_args(self):
        with self.assertRaises(TypeError):
            test_coll = BookCollection(TestBookCollection.test_book)

    def test_coll_can_add_books(self):
        test_coll = BookCollection()
        test_coll.add_book(TestBookCollection.test_book)
        test_coll.print_collection()

    def test_coll_of_2_is_alphabetical_added_correct_order(self):
        test_coll = BookCollection()
        test_coll.add_book(TestBookCollection.test_book_a)  # 'aaaa' added first
        test_coll.add_book(TestBookCollection.test_book_b)
        self.assertEqual(test_coll.books, TestBookCollection.correct_list_ab)
        test_coll.print_collection()

    def test_coll_of_2_is_alphabetical_added_wrong_order(self):
        test_coll = BookCollection()
        test_coll.add_book(TestBookCollection.test_book_b)  # 'bbbb' added first
        test_coll.add_book(TestBookCollection.test_book_a)
        self.assertEqual(test_coll.books, TestBookCollection.correct_list_ab)
        test_coll.print_collection()

    def test_coll_of_3_is_alphabetical_added_wrong_order(self):
        test_coll = BookCollection()
        test_coll.add_book(TestBookCollection.test_book_c)  # 'cccc' added first
        test_coll.add_book(TestBookCollection.test_book_b)
        test_coll.add_book(TestBookCollection.test_book_a)
        self.assertEqual(test_coll.books, TestBookCollection.correct_list_abc)
        test_coll.print_collection()


# TODO: Write tests for book collection
# TODO: Write tests for books with book collection
if __name__ == '__main__':
    unittest.main()

# This is where the program starts. It is the main file that will be run to start the program.
import os

from JsonStorage import JsonStorage
from ReaderTrackerCoreCode import Book, Library

if __name__ == '__main__':
    # Define the base folder for JSON storage
    base_folder = os.path.join(os.getcwd(), 'user_data')

    # Initialize the JsonStorage with the base folder
    storage = JsonStorage(base_folder)

    # Initialize the Library with the storage
    library = Library(storage)

    # Load the GUI
    library.load_gui()



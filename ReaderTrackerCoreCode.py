# In this file I am creating the core functionality for my project
import json
import tkinter as tk
from tkinter import messagebox


# My initial implementation will be to make the user
# able to add and remove from a tobe read list ,and move to a read list.
# Later this will be expanded so the can create custom lists.


# This class will have a title, author, year
# It will also store what collections it is a part of
# It will also have a to string method to represent itself
class Book:
    def __init__(self, title: str, author: str, year: int):
        if not title or not author or not year:
            raise ValueError("Title, author and year must not be empty")
        # check book is not already in read list
        self.title = title
        self.author = author
        self.year = year
        self.collections = []

    def note_book_as_read(self, storage, user_id: str):
        for coll in self.collections:  # remove book from all collections
            coll.remove_book(self)
        storage.remove_book_from_storage(self, user_id, remove_from_all_collections=True)
        storage.add_book_to_storage(self, user_id, "read")  # add book to read list

    def add_collection(self, coll: "BookCollection"):
        self.collections.append(coll)

    def remove_collection(self, coll: "BookCollection"):
        self.collections.remove(coll)

    def get_book_details(self):
        return f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}"

    def to_dict(self):  # creates the book in dictionary form as it can convert to json easily
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year
        }

    @staticmethod
    def from_dict(book_dict: dict):
        return Book(book_dict['title'], book_dict['author'], book_dict['year'])

    def book_to_json_string(self):  # makes a string representation o a json object
        return json.dumps(self.to_dict())


# This class will represent a collection of books.
# It will provide functionality to add and remove books, and sort them
# how the user customizes.
class BookCollection:
    def __init__(self, name: str = None):
        if name is None:  # Handle the case where no name is provided
            self.name = "Unnamed Collection"
        elif not name:
            raise ValueError("Collection name must not be empty")
        else:
            self.name = name
        self.books = []  # Initialize the empty list

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be added")
        if book in self.books:
            raise DuplicateError(f" Book {book} is already in the collection")
        self.books.append(book)
        book.add_collection(self)
        self.sort_books()

    def add_book_with_storage(self, book: Book, storage, user_id: str):
        self.add_book(book)
        storage.add_book_to_storage(book, user_id, self.name)

    def remove_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only books can be removed")
        if book not in self.books:
            raise ValueError("The book is not in the collection")
        self.books.remove(book)
        self.sort_books()
        book.remove_collection(self)

    def remove_book_with_storage(self, book: Book, storage, user_id: str):
        self.remove_book(book)
        storage.remove_book_from_storage(book, user_id, self.name)

    def print_collection(self):
        for b in self.books:
            print(b.get_book_details())

    def sort_books(self):
        self.books.sort(key=lambda x: (x.author, x.title))  # Sorts the books everytime another book is added


# TODO: create library class
# Library class works as the headmaster to manage collections and books
class Library:
    def __init__(self, storage: "JsonStorage"):
        self.storage = storage
        self.current_user = None
        self.selected_user_label = None

    def load_gui(self):
        root = tk.Tk()  # create root widget

        # Setting some window properties
        root.title("Reader Tracker")
        pink = "#f39ff5"
        root.config(padx=20, pady=20, bg=pink)  # padding around the window
        root.minsize(200, 200)  # minimum size of the window
        root.maxsize(500, 500)  # maximum size of the window
        root.geometry("1200x900")  # size and position of the window

        # Let them pick base folder
        # TODO: create a button to let them pick a base folder
        pick_base_folder_button = tk.Button(root, text="Pick Base Folder")
        pick_base_folder_button.place(x=0, y=0)

        # let them add or remove a user
        # Button to open the "add user" dialog
        add_user_button = tk.Button(root, text="Add User", command=self.open_add_user_dialog)
        add_user_button.place(x=0, y=30)

        remove_user_button = tk.Button(root, text="Remove User", command=self.open_remove_user_dialog)
        remove_user_button.place(x=70, y=30)

        # let them pick a user
        pick_user_button = tk.Button(root, text="Pick User", command=self.open_pick_user_dialog)
        pick_user_button.place(x=0, y=100)

        # label to show user
        # Label to display the selected user
        self.selected_user_label = tk.Label(root, text=f"Selected User: {self.current_user}")
        self.selected_user_label.place(x=90, y=100)

        # let them add a collection
        add_collection_button = tk.Button(root, text="Add Collection", command=self.open_add_collection_dialog)
        add_collection_button.place(x=0, y=130)

        # let them remove a collection
        remove_collection_button = tk.Button(root, text="Remove Collection", command=self.open_remove_collection_dialog)
        remove_collection_button.place(x=0, y=160)

        # let them add a book to a collection
        add_book_to_collection_button = tk.Button(root, text="Add Book to Collection", command=self.open_add_book_to_collection_dialog)
        add_book_to_collection_button.place(x=0, y=190)

        # let them remove a book from a collection
        remove_book_from_collection_button = tk.Button(root, text="Remove Book from Collection")
        remove_book_from_collection_button.place(x=0, y=220)

        # TODO: show list of collections of that user
        # TODO: show list of books in that collection
        # TODO: add collection
        # TODO: delete collection
        # TODO: add book to collection
        # TODO: remove book from collection
        # TODO: mark book as read

        root.mainloop()  # runs the main event loop

    def open_add_user_dialog(self):
        # Create a new window for the dialog
        add_user_window = tk.Toplevel()
        add_user_window.title("Add User")

        # Create a entry for the username
        user_label = tk.Label(add_user_window, text="User username:")
        user_label.pack(padx=10, pady=5)
        # user_entry = tk.Entry(add_user_window)

        # Create an entry for the user ID
        user_id_entry = tk.Entry(add_user_window)
        user_id_entry.pack(padx=10, pady=5)

        # create the add user button
        def on_add_user():
            user_name = user_id_entry.get()
            if not user_name:  # if it is entered
                messagebox.showerror("Input Error", "Please enter a user name")
                return

            try:
                self.storage.add_user_to_storage(user_name)
                messagebox.showinfo("User Added", f"User '{user_name}' has been added successfully.")
                print("added the user to storage")
                add_user_window.destroy()
            except FileExistsError:
                messagebox.showerror("User Exists", f"User '{user_name}' already exists.")

        add_button = tk.Button(add_user_window, text="Add User", command=on_add_user)
        add_button.pack()

    def open_remove_user_dialog(self):
        # Create a new window for the dialog
        remove_user_window = tk.Toplevel()
        remove_user_window.title("Remove User")

        # Load the list of users from the users.json file
        user_list = self.storage.get_user_list()

        if not user_list:
            messagebox.showerror("No Users", "There are no users to remove.")
            remove_user_window.destroy()
            return

        # Create a label for the dropdown menu
        user_label = tk.Label(remove_user_window, text="Select a user to remove:")
        user_label.pack(padx=10, pady=5)

        # Create a dropdown menu for the user list
        user_var = tk.StringVar(remove_user_window)
        user_var.set(user_list[0])  # default is the first user
        user_dropdown = tk.OptionMenu(remove_user_window, user_var, *user_list)
        user_dropdown.pack(padx=10, pady=5)

        # create the remove user button
        def on_remove_user():
            user_name = user_var.get()
            if not user_name:  # if it is entered
                messagebox.showerror("Input Error", "Please enter a user name")

            try:
                self.storage.remove_user_from_storage(user_name)
                messagebox.showinfo("User Removed", f"User '{user_name}' has been removed successfully.")
                print("removed the user to storage")
                remove_user_window.destroy()
            except FileNotFoundError:
                messagebox.showerror("User Not Found", f"User '{user_name}' does not exist.")

        remove_button = tk.Button(remove_user_window, text="Remove User", command=on_remove_user)
        remove_button.pack()

    def open_pick_user_dialog(self):
        # Create a new window for the dialog
        pick_user_window = tk.Toplevel()
        pick_user_window.title("Pick User")

        # Load the list of users from the users.json file
        user_list = self.storage.get_user_list()

        if not user_list:
            messagebox.showerror("No Users", "There are no users to pick.")
            pick_user_window.destroy()
            return

        # Create a label for the dropdown menu
        user_label = tk.Label(pick_user_window, text="Select a user:")
        user_label.pack(padx=10, pady=5)

        # Create a dropdown menu for the user list
        user_var = tk.StringVar(pick_user_window)
        user_var.set(user_list[0])
        user_dropdown = tk.OptionMenu(pick_user_window, user_var, *user_list)
        user_dropdown.pack(padx=10, pady=5)

        # create the remove user button
        def on_pick_user():
            user_name = user_var.get()
            if not user_name:  # if it is entered
                messagebox.showerror("Input Error", "Please enter a user name")

            self.current_user = user_name
            self.selected_user_label.config(text=f"Selected User: {self.current_user}")
            messagebox.showinfo("User Picked", f"User '{user_name}' has been picked successfully.")
            pick_user_window.destroy()

        pick_button = tk.Button(pick_user_window, text="Pick User", command=on_pick_user)
        pick_button.pack()

    def open_add_collection_dialog(self):
        # Create a new window for the dialog
        add_coll_window = tk.Toplevel()
        add_coll_window.title("Add Collection: ")

        # Create a label for the collection name
        coll_label = tk.Label(add_coll_window, text="Collection name:")
        coll_label.pack(padx=10, pady=5)

        # Create an entry for the collection name
        coll_entry = tk.Entry(add_coll_window)
        coll_entry.pack(padx=10, pady=5)

        # Create the add collection button
        def on_add_collection():
            coll_name = coll_entry.get()
            if not coll_name:
                messagebox.showerror("Input Error", "Please enter a collection name")
                return

            # Check if the user already has a collection with the same name
            if coll_name in self.storage.get_list_of_collection_names(self.current_user):
                messagebox.showerror("Duplicate Collection", f"Collection '{coll_name}' already exists.")
                return

            if self.current_user is None:
                messagebox.showerror("No User Selected", "Please select a user first.")
                return

            # Add the collection to the storage
            new_coll = BookCollection(coll_name)
            self.storage.add_collection_to_storage(new_coll, self.current_user)
            messagebox.showinfo("Collection Added", f"Collection '{coll_name}' has been added successfully.")
            add_coll_window.destroy()

        # Create the add collection button
        add_button = tk.Button(add_coll_window, text="Add Collection", command=on_add_collection)
        add_button.pack()

    def open_remove_collection_dialog(self):
        # Create a new window for the dialog
        remove_coll_window = tk.Toplevel()
        remove_coll_window.title("Remove Collection")

        # Load the list of collections from the collections.json file
        try:
            coll_list = self.storage.get_list_of_collection_names(self.current_user)
            # remove the books and read collections as they should not be removed
            # coll_list.remove("books")
            # coll_list.remove("read")
            if not coll_list:
                messagebox.showerror("No Collections", "There are no collections to remove.")
                remove_coll_window.destroy()
                return
        except TypeError:
            messagebox.showerror("No User Selected", "Please select a user first")
            remove_coll_window.destroy()
            return

        # Create label
        coll_label = tk.Label(remove_coll_window, text="Select a collection to remove:")
        coll_label.pack(padx=10, pady=5)

        # Create a dropdown menu for the collection list
        coll_var = tk.StringVar(remove_coll_window)
        coll_var.set(coll_list[0])
        coll_dropdown = tk.OptionMenu(remove_coll_window, coll_var, *coll_list)
        coll_dropdown.pack(padx=10, pady=5)

        # Create the remove collection button
        def on_remove_collection():
            coll_name = coll_var.get()
            if not coll_name:
                messagebox.showerror("Input Error", "Please enter a collection name")
                return

            try:
                self.storage.remove_collection_from_storage(coll_name, self.current_user)
                messagebox.showinfo("Collection Removed", f"Collection '{coll_name}' has been removed successfully.")
                remove_coll_window.destroy()
            except FileNotFoundError:
                messagebox.showerror("Collection Not Found", f"Collection '{coll_name}' does not exist.")

        # Create the button
        remove_button = tk.Button(remove_coll_window, text="Remove Collection", command=on_remove_collection)
        remove_button.pack()


    def open_add_book_to_collection_dialog(self):
        #todo: add a checkbox to let them choose wehich collections to add to.
        # automatically have books picked if it is present

        # Create a new window for the dialog
        add_book_to_coll_window = tk.Toplevel()
        add_book_to_coll_window.title("Add Book to Collection")



# load up GUI
# let user pick user or create one ( when created forms them a json folder or add to database)
# let user see collections to view
# let user click collections and books to mark as read
# load collections
# add collection
# delete collection
# add book to this collection
# add book in general to storage
# remove book from this collection
# remove book in general from storage


# class for creating an exception when trying to add a duplicate
class DuplicateError(Exception):
    """Custom exception raised when a duplicate item is added."""
    pass

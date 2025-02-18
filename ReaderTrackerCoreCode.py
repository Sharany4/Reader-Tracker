# In this file I am creating the core functionality for my project
import json
import tkinter as tk
from tkinter import messagebox, BOTH


# My initial implementation will be to make the user
# able to add and remove from a tobe read list ,and move to a read list.
# Later this will be expanded so the can create custom lists.


# This class will have a title, author, year
# It will also store what collections it is a part of
# It will also have a to string method to represent itself

# todo: change the way collections are stored. wen wanting the collection, get from storage
# when wanting to add and remove, done for storage, and them array is updated
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
            storage.remove_book_from_storage(self, user_id, coll)
        storage.remove_book_from_storage(self, user_id,
                                         remove_from_all_collections=True)  # should remove from all colls
        storage.add_book_to_storage(self, user_id, "read")  # add book to read list

    def add_collection(self, coll: str):  # change to take str, use to ad collections from file or new
        # todo: change so it will change add book to collection, add collection to book
        self.collections.append(coll)
        # change in the books file collections for this book
        # eg json add collection to book, or should it be does when addthe book to coll

    def add_collection_with_storage(self, coll: str, storage, user_id):
        storage.add_collection_to_book_storage(self, coll, user_id)
        # where will the collection add the book?
        # self.collections = #collections for book from books file, method to get collections from storage
        self.collections = storage.get_books_collections(self, user_id)

    def remove_collection(self, coll: str):  # change to take str
        self.collections.remove(coll)
        # change in the books file collections for this book

    def get_book_details(self):
        return f"Book Details: Title: {self.title}, Author: {self.author}, Year: {self.year}"

    def to_dict(self):  # creates the book in dictionary form as it can convert to json easily
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            # "collections": [self.collections]
            "collections": []
            # '''
            # It doesnt understand how to put both colls in, like books and test coll.
            # It doesnt see them as equal as they dont have the same collections. but we need a way to not check the
            # collections, as they are different objects. Perhaps add mthod to jsut check the title, author and year?
            # '''
        }

        # TODO: add collections dictionary to this

    @staticmethod
    def from_dict(book_dict: dict):
        return Book(book_dict['title'], book_dict['author'], book_dict['year'])
        # if the book has collections, add them to the book

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
        book.add_collection(self.name)  # str
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
        book.remove_collection(self.name)  # str

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
        self.current_collection = None
        self.selected_coll_label = None
        self.book_listbox = None

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
        self.selected_user_label.place(x=105, y=100)

        # let them select a collection to view from a dropdown
        select_collection_button = tk.Button(root, text="Select Collection", command=self.open_select_collection_dialog)
        select_collection_button.place(x=0, y=130)

        # label to show collection
        self.selected_coll_label = tk.Label(root, text=f"Selected Collection: {self.current_collection}")
        self.selected_coll_label.place(x=105, y=130)

        # let them add a collection
        add_collection_button = tk.Button(root, text="Add Collection", command=self.open_add_collection_dialog)
        add_collection_button.place(x=0, y=180)

        # let them remove a collection
        remove_collection_button = tk.Button(root, text="Remove Collection", command=self.open_remove_collection_dialog)
        remove_collection_button.place(x=0, y=210)

        # let them add a book to a collection
        add_book_to_collection_button = tk.Button(root, text="Add Book",
                                                  command=self.open_add_book_dialog)
        add_book_to_collection_button.place(x=0, y=240)

        # let them remove a book from a collection, will be added to right side bar instead
        remove_book_from_collection_button = tk.Button(root, text="Remove Book from Collection",
                                                       command=self.open_remove_book_dialog)
        remove_book_from_collection_button.place(x=0, y=270)

        # Let them move a book, or mark as read

        # TODO: will be done after can add and remove a book
        # Create a listbox to display books
        self.book_listbox = tk.Listbox(root)
        self.book_listbox.place(x=250, y=30, width=300, height=400)
        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)

        # TODO: show list of collections of that user
        # TODO: show list of books in that collection
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

    def open_select_collection_dialog(self):
        # Create a new window for the dialog
        select_coll_window = tk.Toplevel()
        select_coll_window.title("Select Collection")

        # Load the list of collections from the collections.json file
        try:
            coll_list = self.storage.get_list_of_collection_names(self.current_user)
            # Add the books and read collections
            coll_list.append("books")
            coll_list.append("read")
            if not coll_list:
                messagebox.showerror("No Collections", "There are no collections to select.")
                select_coll_window.destroy()
                return
        except TypeError:
            messagebox.showerror("No User Selected", "Please select a user first")
            select_coll_window.destroy()
            return

        # Create a label for the dropdown menu
        coll_label = tk.Label(select_coll_window, text="Select a collection:")
        coll_label.pack(padx=10, pady=5)

        # Create a dropdown menu for the collection list
        coll_var = tk.StringVar(select_coll_window)
        coll_var.set(coll_list[0])
        coll_dropdown = tk.OptionMenu(select_coll_window, coll_var, *coll_list)
        coll_dropdown.pack(padx=10, pady=5)

        # Create the select collection button
        def on_select_collection():
            coll_name = coll_var.get()
            if not coll_name:
                messagebox.showerror("Input Error", "Please enter a collection name")
                return

            self.current_collection = coll_name
            self.selected_coll_label.config(text=f"Selected Collection: {self.current_collection}")
            messagebox.showinfo("Collection Selected", f"Collection '{coll_name}' has been selected successfully.")
            select_coll_window.destroy()

        # Create the button
        select_button = tk.Button(select_coll_window, text="Select Collection", command=on_select_collection)
        select_button.pack()

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

            if self.current_user is None:
                messagebox.showerror("No User Selected", "Please select a user first.")
                return

            # Check if the user already has a collection with the same name
            if coll_name in self.storage.get_list_of_collection_names(self.current_user):
                messagebox.showerror("Duplicate Collection", f"Collection '{coll_name}' already exists.")
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

    def open_add_book_dialog(self):
        # todo: when a book is added to a collection, add it ot the collecton dict aswell
        # Create a new window for the dialog
        add_book_window = tk.Toplevel()
        add_book_window.title("Add Book to Collection")

        if self.current_user is None:
            messagebox.showerror("No User Selected", "Please select a user first.")
            add_book_window.destroy()
            return

        # Create a label
        add_book_label = tk.Label(add_book_window, text="Book to add: (Auto added to 'books' collection)")
        add_book_label.pack(padx=10, pady=5)

        # Create an entry and label for the title
        title_label = tk.Label(add_book_window, text="Title:")
        title_label.pack(padx=10, pady=5)
        title_entry = tk.Entry(add_book_window)
        title_entry.pack(padx=20, pady=5)

        # Create an entry and label for the author
        author_label = tk.Label(add_book_window, text="Author:")
        author_label.pack(padx=10, pady=5)
        author_entry = tk.Entry(add_book_window)
        author_entry.pack(padx=10, pady=5)

        # Create an entry and label for the year
        year_label = tk.Label(add_book_window, text="Year:")
        year_label.pack(padx=10, pady=5)
        year_entry = tk.Entry(add_book_window)
        year_entry.pack(padx=10, pady=5)

        # Select the collections to add to using listbox
        collections_to_add_to_listbox = tk.Listbox(add_book_window, selectmode=tk.MULTIPLE)
        collections_to_add_to_listbox.pack(padx=10, pady=5)
        # Get list of collections
        collections = self.storage.get_list_of_collection_names(self.current_user)
        for coll in collections:
            collections_to_add_to_listbox.insert(tk.END, coll)

        def on_add_book():
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()
            picked_collections = collections_to_add_to_listbox.curselection()
            if not title or not author or not year:
                messagebox.showerror("Input Error", "Please enter a title, author, and year")
                return

            if not year.isdigit():
                messagebox.showerror("Input Error", "Year must be a number")

            new_book = Book(title, author, int(year))
            try:
                self.storage.add_book_to_storage(new_book, self.current_user, "books")
                for col in picked_collections:
                    coll_name = collections_to_add_to_listbox.get(col)
                    print("coll name pucked " + coll_name)
                    self.storage.add_book_to_storage(new_book, self.current_user, coll_name)
                    self.storage.add_collection_to_book_storage(new_book, coll_name, self.current_user)
            except ValueError:
                messagebox.showerror("Book Exists", f"Book '{title}' already exists in the storage. To change or mark "
                                                    f"as read, find the mbook in storage and right click")
                return

            messagebox.showinfo("Book Added", f"Book '{title}' has been added successfully.")
            add_book_window.destroy()

        add_button = tk.Button(add_book_window, text="Add Book", command=on_add_book)
        add_button.pack()

    def open_remove_book_dialog(self):
        # Create a new window for the dialog
        remove_book_window = tk.Toplevel()
        remove_book_window.minsize(300, 500)
        remove_book_window.title("Remove Book from Collection")
        # remove_book_window.geometry("500x500")

        if self.current_user is None:
            messagebox.showerror("No User Selected", "Please select a user first.")
            remove_book_window.destroy()
            return

        # Create a label
        remove_book_label = tk.Label(remove_book_window, text="Book to remove")
        remove_book_label.pack(padx=10, pady=5)

        # Let them search books using title
        books_collection = self.storage.load_collection_from_storage(self.current_user, "books")

        # Select the book to add to using listbox
        books_listbox = tk.Listbox(remove_book_window)
        books_listbox.pack(padx=10, pady=5, fill=BOTH, expand=True)
        # Get list of books
        books = books_collection.books
        for b in books:
            book_string = b.title + " by " + b.author + " " + str(b.year)
            print(book_string)
            # print(b.title)
            books_listbox.insert(tk.END, book_string)

        def get_book_from_description(book_string: str):
            res = book_string.split(" ") # to store the words
            last_index_of_title = None # use this index to extract data
            title_string = ""
            author_string = ""
            year = -1
            for i in range(len(res)):  # go through elements
                if res[i] == "by":
                    last_index_of_title = i
                    for j in range(last_index_of_title): # add the title parts to title string
                        # print("title " + res[j])
                        title_string += res[j] + " " # to add space

                    for r in range(i + 1, len(res) - 1):# add the author parts to author string
                        # print("author " + res[r])
                        author_string += res[r] + " "

                    print("title: " + title_string)
                    print("author: " + author_string)
                    print("year " + res[len(res) - 1])
                    year = res[len(res)-1] # assign data
                    title_string = title_string[:len(title_string)-1] # remove last character so the strings are correct
                    author_string = author_string[:len(author_string)-1]
            return Book(title_string, author_string, year)


        def on_remove_book():
            selected_indices = books_listbox.curselection()
            if selected_indices:
                selected_index = selected_indices[0]
                selected_item = books_listbox.get(selected_index)
                print("Selected item: " + selected_item)
                get_book_from_description(selected_item)

                # opens a window of collections it is it, can select multiple to remove

        remove_button = tk.Button(remove_book_window, text="Remove Book", command=on_remove_book)
        remove_button.pack()
        # todo: extract the details correctly from the chosen book

        # let them search for a book by title

        # them let them right click the book, and opens window.
        # new window lets them selections to remove from
        # let them pick multiple
        # have a check bo to remove from storage, if checked, will rmeove from books file to

    # TODO: make this work after can add and remove a book
    def update_book_listbox(self):
        if self.current_user and self.current_collection:
            try:
                collection = self.storage.load_collection_from_storage(self.current_user, self.current_collection)
                self.book_listbox.delete(0, tk.END)
                for book in collection.books:
                    self.book_listbox.insert(tk.END, book.get_book_details())
            except FileNotFoundError:
                messagebox.showerror("Error",
                                     f"Collection '{self.current_collection}' not found for user '{self.current_user}'")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # TODO: make this work after can add and remove a book
    def on_book_select(self, event):
        selected_index = self.book_listbox.curselection()
        if selected_index:
            selected_book = self.current_collection.books[selected_index[0]]


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

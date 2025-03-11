# This file will contain the code needed for the GUI components to function correctly in the app
from tkinter import messagebox, StringVar, Listbox, BooleanVar
from tkinter.ttk import Entry, Label


class GUICode:

    @staticmethod
    def on_add_user(library, user_id_entry: Entry, add_user_window: "Tk TopLevel"):
        user_name = user_id_entry.get()
        if not user_name:  # if it is entered
            messagebox.showerror("Input Error", "Please enter a user name")
            return

        try:
            library.storage.add_user_to_storage(user_name)
            messagebox.showinfo("User Added", f"User '{user_name}' has been added successfully.")
            print("added the user to storage")
            add_user_window.destroy()
        except FileExistsError:
            messagebox.showerror("User Exists", f"User '{user_name}' already exists.")

    @staticmethod
    def on_remove_user(library, user_var: Entry, remove_user_window: "TK TopLevel"):
        user_name = user_var.get()
        if not user_name:  # if it is entered
            messagebox.showerror("Input Error", "Please enter a user name")

        try:
            library.storage.remove_user_from_storage(user_name)
            messagebox.showinfo("User Removed", f"User '{user_name}' has been removed successfully.")
            print("removed the user to storage")
            remove_user_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("User Not Found", f"User '{user_name}' does not exist.")

    @staticmethod
    def on_pick_user(library, user_var: StringVar, pick_user_window: "TK TopLevel"):
        user_name = user_var.get()
        if not user_name:  # if it is entered
            messagebox.showerror("Input Error", "Please enter a user name")

        library.current_user = user_name
        library.selected_user_label.config(text=f"Selected User: {library.current_user}")
        messagebox.showinfo("User Picked", f"User '{user_name}' has been picked successfully.")
        pick_user_window.destroy()

    @staticmethod
    def on_select_collection(library, coll_var: StringVar, select_coll_window):
        coll_name = coll_var.get()
        if not coll_name:
            messagebox.showerror("Input Error", "Please enter a collection name")
            return

        library.current_collection = coll_name
        library.selected_coll_label.config(text=f"Selected Collection: {library.current_collection}")
        messagebox.showinfo("Collection Selected", f"Collection '{coll_name}' has been selected successfully.")
        select_coll_window.destroy()

    @staticmethod
    def on_add_collection(library, coll_entry: Entry, add_coll_window):
        from ReaderTrackerCoreCode import BookCollection
        coll_name = coll_entry.get()
        if not coll_name:
            messagebox.showerror("Input Error", "Please enter a collection name")
            return

        if library.current_user is None:
            messagebox.showerror("No User Selected", "Please select a user first.")
            return

        # Check if the user already has a collection with the same name
        if coll_name in library.storage.get_list_of_collection_names(library.current_user):
            messagebox.showerror("Duplicate Collection", f"Collection '{coll_name}' already exists.")
            return

        # Add the collection to the storage
        new_coll = BookCollection(coll_name)
        library.storage.add_collection_to_storage(new_coll, library.current_user)
        messagebox.showinfo("Collection Added", f"Collection '{coll_name}' has been added successfully.")
        add_coll_window.destroy()

    @staticmethod
    def on_remove_collection(library, coll_var: StringVar, remove_coll_window):
        coll_name = coll_var.get()
        if not coll_name:
            messagebox.showerror("Input Error", "Please enter a collection name")
            return

        try:
            library.storage.remove_collection_from_storage(coll_name, library.current_user)
            messagebox.showinfo("Collection Removed", f"Collection '{coll_name}' has been removed successfully.")
            remove_coll_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("Collection Not Found", f"Collection '{coll_name}' does not exist.")

    @staticmethod
    def on_add_book(library, title_entry: Entry, author_entry: Entry, year_entry: Entry,
                    collections_to_add_to_listbox: Listbox, add_book_window):

        from ReaderTrackerCoreCode import Book

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
            library.storage.add_book_to_storage(new_book, library.current_user, "books")
            for col in picked_collections:
                coll_name = collections_to_add_to_listbox.get(col)
                print("coll name pucked " + coll_name)
                library.storage.add_book_to_storage(new_book, library.current_user, coll_name)
                library.storage.add_collection_to_book_storage(new_book, coll_name, library.current_user)
        except ValueError:
            messagebox.showerror("Book Exists", f"Book '{title}' already exists in the storage. To change or mark "
                                                f"as read, find the mbook in storage and right click")
            return

        messagebox.showinfo("Book Added", f"Book '{title}' has been added successfully.")
        add_book_window.destroy()

    @staticmethod
    def get_book_from_description(book_string: str):

        from ReaderTrackerCoreCode import Book

        res = book_string.split(" ")  # to store the words
        last_index_of_title = None  # use this index to extract data
        title_string = ""
        author_string = ""
        year = -1
        for i in range(len(res)):  # go through elements
            if res[i] == "by":
                last_index_of_title = i
                for j in range(last_index_of_title):  # add the title parts to title string
                    # print("title " + res[j])
                    title_string += res[j] + " "  # to add space

                for r in range(i + 1, len(res) - 1):  # add the author parts to author string
                    # print("author " + res[r])
                    author_string += res[r] + " "

                print("title: " + title_string)
                print("author: " + author_string)
                print("year " + res[len(res) - 1])
                year = res[len(res) - 1]  # assign data
                title_string = title_string[
                               :len(title_string) - 1]  # remove last character so the strings are correct
                author_string = author_string[:len(author_string) - 1]

                # assert(title_string == books[1].title)
                # assert(author_string == books[1].author)
                # assert(int(year) == books[1].year)
        return Book(title_string, author_string, int(year))

    @staticmethod
    def on_remove_book(library, books_listbox: Listbox, remove_from_all_storage: BooleanVar, remove_book_window):
        boxmessage = "The book was not removed"
        # todo: remove from some collections(lets see what cols its in,and selcted to remove)
        selected_indices = books_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_item = books_listbox.get(selected_index)
            print("Selected item: " + selected_item)
            book_to_remove = GUICode.get_book_from_description(selected_item)
            # self.storage.remove_book_from_storage(book_to_remove, self.current_user,
            #                                     remove_from_all_collections=True)
            # todo: let the user right click on the book, pick what collections they want to remove from with list box

            if remove_from_all_storage.get() == True:
                print("You want to remove the book from all of storage")
                library.storage.remove_book_from_storage(book_to_remove, library.current_user,
                                                         remove_from_all_collections=True)
                boxmessage = f"Book '{book_to_remove.title}' has been removed successfully."
            else:
                print("You do not want to remove the book from all of storage")

            # boxmessage = f"Book '{book_to_remove.title}' has been removed successfully."

        messagebox.showinfo("Book Removed", boxmessage)
        remove_book_window.destroy()

        # opens a window of collections it is it, can select multiple to remove

        # let them search for a book by title

        # them let them right click the book, and opens window.
        # new window lets them selections to remove from
        # let them pick multiple
        # have a check bo to remove from storage, if checked, will rmeove from books file to

    @staticmethod
    def on_right_click_book(event, list_box):
        eventstring = "event string: " + str(event) + str(list_box.curselection())
        print(eventstring)

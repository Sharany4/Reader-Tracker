# This file will contain the code needed for the GUI components to function correctly in the app
from tkinter import messagebox, StringVar
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

import tkinter as tk
from tkinter import messagebox
from books import Books  
import pandas as pd
class Reader:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.books_instance = Books(self.root)  # Initialize Books instance for book operations

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def username_password_verification(self, username, password):
        """Check if the username and password match the database."""
        try:
            usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv")
            user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
            if not user_info.empty:
                return user_info['password'].values[0] == password
            return False
        except FileNotFoundError:
            messagebox.showerror("Error", "Passwords file not found.")
            return False

    def login_screen(self):
        """Display login screen for username and password."""
        self.clear_window()

        tk.Label(self.root, text="Reader Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        password_entry = tk.Entry(self.root, show='*')
        password_entry.pack(pady=5)

        def verify_login():
            username = username_entry.get()
            password = password_entry.get()
            if self.username_password_verification(username, password):
                self.username = username
                self.password = password
                messagebox.showinfo("Success", "Login successful!")
                self.show_menu()  # Show reader's menu after successful login
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        tk.Button(self.root, text="Login", command=verify_login).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def show_menu(self):
        """Reader's menu after successful login."""
        self.clear_window()

        tk.Label(self.root, text="Reader Menu", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="View Available Books", command=self.books_instance.show_books).pack(pady=10)
        tk.Button(self.root, text="Find a Book", command=self.search_for_book).pack(pady=10)
        tk.Button(self.root, text="Show Borrowing History", command=self.show_history).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def search_for_book(self):
        """Search for a book by title, author, or ISBN."""
        self.clear_window()

        tk.Label(self.root, text="Search for Book", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Enter Book Title, Author, or ISBN").pack(pady=5)
        search_entry = tk.Entry(self.root)
        search_entry.pack(pady=5)

        def search():
            search_query = search_entry.get()
            search_results = self.books_instance.find_book(search_query)

            if not search_results.empty:
                for index, row in search_results.iterrows():
                    book_info = f"Title: {row['knygos_pavadinimas']}, Author: {row['autorius']}, ISBN: {row['ISBN']}"
                    book_label = tk.Label(self.root, text=book_info)
                    book_label.pack(pady=5)

                    # Add click event to show book profile
                    book_label.bind("<Button-1>", lambda e, book=row: self.books_instance.show_book_profile(book))
            else:
                tk.Label(self.root, text="No books found.").pack(pady=5)

        tk.Button(self.root, text="Search", command=search).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_menu).pack(pady=10)

    def show_history(self):
        """Show the reader's borrowing history (can be implemented later)."""
        # You can implement this functionality later, based on a reader's borrowing history
        pass

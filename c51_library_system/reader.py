import tkinter as tk
from tkinter import messagebox
from books import Books  
import pandas as pd


class Reader:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.books_instance = Books(self.root)

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()



    def login_screen(self):
        """Display login screen for username and password."""
        self.clear_window()

        tk.Label(self.root, text="Reader Login", font=("Arial", 20)).pack(pady=20)

        

    def show_menu(self):
        """Reader's menu after successful login."""
        self.clear_window()

        tk.Label(self.root, text="Reader Menu", font=("Arial", 20)).pack(pady=20)

        self.add_button("Peržiūrėti knygas", 250, 200, self.books_instance.show_books)  
        self.add_button("Surasti knygą", 250, 500, self.books_instance.search_for_book)  
        self.add_button("Skaitymo istorija", 750, 200, self.show_history)
        self.add_button("Rezervuoti knygą", 750, 500, self.book_reservation)
          
        self.add_button("Atgal į prisijungimo langą", 1250, 200, self.go_back_to_login)  
        self.add_button("Išeiti iš sistemos", 1250, 500, self.root.quit) 

    def show_history(self):
        """Show the reader's borrowing history (can be implemented later)."""
        # You can implement this functionality later, based on a reader's borrowing history
        pass
    
    
    def book_reservation(self):
        pass

    def go_back_to_login(self):
        from reader_login import ReaderLogin
        reader_login = ReaderLogin(self.root)
        reader_login.reader_login_screen(back_function=self.go_back_to_login)
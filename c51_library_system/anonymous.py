import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from books import Books

class AnonymousUser:
    def __init__(self, root):
        self.root = root
        self.books_instance = Books(self.root, is_anonymous=True)

    def search_books(self):
        self.books_instance.show_books()

    def view_books(self):
        self.books_instance.show_books()

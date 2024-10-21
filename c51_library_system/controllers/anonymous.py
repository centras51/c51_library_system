import tkinter as tk
from .books import Books
from PIL import Image, ImageTk
from .reader_registration import ReaderRegistration
from utils.validation_helpers import Validator
from ui.ui_helpers import set_background
from utils.general_helpers import Generator
from utils.csv_helpers import CsvProcessor
from utils.navigation_helpers import Navigator


class AnonymousUser:
    def __init__(self, root):
        self.root = root
        self.validator = Validator()
        self.generator = Generator()
        self.csvprocessor = CsvProcessor()
        self.navigator = Navigator()
        self.canvas = None
        self.background_image = None
        self.books_instance = Books(self.root, is_anonymous=True)
        self.readerregistration_instance = ReaderRegistration(self.root)
        self.button_width = 30
        self.button_height = 3

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.canvas, self.background_image = set_background(self.root)

    def show_menu(self):
        self.clear_window()

        self.canvas.create_text(350, 50, text=f"Knygos išduodamos bibliotekoje su skaitytojo registracija",
                                font=("Arial", 15, "bold"), fill="white", anchor="nw")

        self.add_button("Peržiūrėti knygas", 700, 200, self.books_instance.show_books)
        self.add_button("Skaitytojo registracija", 700, 350, self.readerregistration_instance.register)
        self.add_button("Atgal į pagrindinį langą", 700, 500, command=lambda: self.navigator.go_back_to_login(self.root))
        self.add_button("Išeiti iš sistemos", 700, 650, command=lambda: self.root.quit)
                                
    def add_button(self, text, x_position, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                           command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    

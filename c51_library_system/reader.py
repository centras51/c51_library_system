import tkinter as tk
from tkinter import messagebox
from books import Books  
import pandas as pd
from PIL import Image, ImageTk


class Reader:
    def __init__(self, root, reader_card_number):
        self.root = root
        self.username = None
        self.password = None
        self.reader_card_number = reader_card_number  # Skaitytojo kortelės numeris
        self.books_instance = Books(self.root, is_reader=True)
        self.button_width = 30  
        self.button_height = 3 

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        
        self.show_menu()

    def clear_window(self):
        """Clear all widgets from the window and recreate the canvas."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate the canvas after clearing the window
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def show_menu(self):
        """Reader's menu after successful login."""
        self.clear_window()

        self.canvas.create_text(250, 50, text=f"Skaitytojas: , Tel: , El. paštas: ", font=("Arial", 15, "bold"), fill="yellow", anchor="nw")
        
        # Patikrinti dėl vėluojamų knygų, naudojant Books klasę
        if self.books_instance.check_late_books(self.reader_card_number):
            messagebox.showwarning("Įspėjimas", "Turite vėluojančių knygų! Prašome jas kuo greičiau grąžinti.")

        tk.Label(self.root, text="Skaitytojo aplinka", font=("Arial", 20)).pack(pady=20)

        self.add_button("Peržiūrėti knygas", 700, 200, self.books_instance.show_books)  
        self.add_button("Skaitymo istorija", 700, 350, self.show_history)
        self.add_button("Atgal į prisijungimo langą", 700, 500, self.go_back_to_login)  
        self.add_button("Išeiti iš sistemos", 700, 650, self.root.quit) 

    def show_history(self):
        """Rodo skaitytojo skaitymo ir rezervacijų istoriją."""
        history = self.books_instance.get_reader_history(self.reader_card_number)

        history_window = tk.Toplevel(self.root)
        history_window.title("Jūsų skaitymo ir rezervacijų istorija")

        # Sukuriame sąrašą knygų istorijai
        tk.Label(history_window, text="Skaitymo ir rezervacijų istorija:", font=("Arial", 15)).pack(pady=10)

        for book in history:
            tk.Label(history_window, text=book, font=("Arial", 12)).pack(pady=5)

    def add_button(self, text, x_position, y_position, command):
        """Sukurti mygtuką ir pridėti jį į `canvas`."""
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def go_back_to_login(self):
        from reader_login import ReaderLogin
        reader_login = ReaderLogin(self.root)
        reader_login.reader_login_screen(back_function=self.go_back_to_login)

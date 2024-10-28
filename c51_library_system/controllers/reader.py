import tkinter as tk
from tkinter import messagebox
from ui.ui_helpers import set_background
from .books import Books
from utils.navigation_helpers import Navigator


class Reader:
    def __init__(self, root, reader_card_number):
        self.root = root
        self.username = None
        self.password = None
        self.reader_card_number = reader_card_number 
        self.books_instance = Books(self.root, is_reader=True)
        self.navigator = Navigator()
        self.button_width = 30  
        self.button_height = 3 

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.canvas, self.background_image = set_background(self.root)
        
    def show_menu(self):
        self.clear_window()

        self.canvas.create_text(250, 50, text=f"Skaitytojas: , Tel: , El. paštas: ", font=("Arial", 15, "bold"), fill="yellow", anchor="nw")
        
        if self.books_instance.check_late_books(self.reader_card_number):
            messagebox.showwarning("Įspėjimas", "Turite vėluojančių knygų! Prašome jas kuo greičiau grąžinti.")

        tk.Label(self.root, text="Skaitytojo aplinka", font=("Arial", 20)).pack(pady=20)

        self.add_button("Peržiūrėti knygas", 700, 200, self.books_instance.show_books)  
        self.add_button("Skaitymo istorija", 700, 350, self.show_history)
        self.add_button("Atgal į prisijungimo langą", 700, 500, lambda: self.navigator.go_back_to_login(self.root))  
        self.add_button("Išeiti iš sistemos", 700, 650, self.root.quit) 

    def show_history(self):
        history = self.books_instance.get_reader_history(self.reader_card_number)

        history_window = tk.Toplevel(self.root)
        history_window.title("Jūsų skaitymo ir rezervacijų istorija")

        tk.Label(history_window, text="Skaitymo ir rezervacijų istorija:", font=("Arial", 15)).pack(pady=10)

        for book in history:
            tk.Label(history_window, text=book, font=("Arial", 12)).pack(pady=5)

    def add_button(self, text, x_position, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def go_back_to_login(self):
        from reader_login import ReaderLogin
        reader_login = ReaderLogin(self.root)
        reader_login.reader_login_screen(back_function=self.go_back_to_login)

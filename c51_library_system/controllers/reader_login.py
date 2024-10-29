import tkinter as tk
import sqlite3
from tkinter import messagebox
from .reader import Reader
from ui.ui_helpers import set_background
from utils.navigation_helpers import Navigator
from utils.authenticators import Authenticator

class ReaderLogin:
    def __init__(self, root, db_path="D:\\CodeAcademy\\c51_library_system\\data_bases\\library_db.db"):
        self.root = root
        self.navigator = Navigator()
        self.authenticator = Authenticator()
        self.canvas = None
        self.background_image = None
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30
        self.entry_font = ("Arial", 18)
        self.reader = None
        self.db_path = db_path

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas, self.background_image = set_background(self.root)

    def reader_login_screen(self, back_function):
        self.clear_window()

        if not self.canvas:
            messagebox.showerror("Klaida", "Nepavyko sukurti `canvas` elemento.")
            return

        self.canvas.create_text(700, 100, text="Skaitytojo prisijungimas", font=("Arial", 30, "bold"), fill="white")

        self.canvas.create_text(700, 200, text="Vartotojo vardas", font=("Arial", 20, "bold"), fill="white")
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.canvas.create_window(700, 250, window=self.username_entry)

        self.canvas.create_text(700, 300, text="Slaptažodis", font=("Arial", 20, "bold"), fill="white")
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.canvas.create_window(700, 350, window=self.password_entry)

        self.add_button("Prisijungti", 500, self.verify_reader)
        self.add_button("Atgal", 650, lambda: back_function())
        self.add_button("Išeiti iš sistemos", 800, self.root.quit)

    def add_button(self, text, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                           command=command)

        if self.canvas:
            self.canvas.create_window(700, y_position, window=button)
        else:
            messagebox.showerror("Klaida", "`canvas` elementas nėra sukurtas.")

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def verify_reader(self):
        reader_username = self.username_entry.get()
        reader_password = self.password_entry.get()

        if self.authenticator.username_password_verification(reader_username, reader_password):
            reader_info = self.get_reader_info(reader_username)
            if reader_info:
                reader_card_number, reader_id, reader_name, reader_last_name = reader_info
                self.reader = Reader(self.root, reader_card_number, reader_id)
                
                messagebox.showinfo("Prisijungta", f"Prisijungimas sėkmingas! Sveiki, {reader_name} {reader_last_name}.")
                
                self.reader.show_menu()
            else:
                messagebox.showerror("Klaida", "Skaitytojo kortelės numeris nerastas.")
        else:
            messagebox.showerror("Klaida", "Neteisingas vartotojo vardas arba slaptažodis.")
            
    def get_reader_info(self, username):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT 
                                    skaitytojo_id, skaitytojo_kortele, vardas, pavarde 
                                FROM 
                                    readers 
                                WHERE 
                                    username = ?""", (username,))
                result = cursor.fetchone()

            return result if result else None
        except sqlite3.Error as e:
            messagebox.showerror("Klaida", f"Duomenų bazės klaida: {e}")
            return None

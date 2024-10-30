import sqlite3
import tkinter as tk
from tkinter import messagebox
from .librarian import Librarian
from ui.ui_helpers import set_background
from utils.navigation_helpers import Navigator
from utils.authenticators import Authenticator


class LibrarianLogin:
    def __init__(self, root, back_function=None):  # Pridedame `back_function` kaip parametrą
        self.root = root
        self.navigator = Navigator()
        self.authenticator = Authenticator()
        self.canvas = None
        self.background_image = None
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30
        self.entry_font = ("Arial", 18)
        self.back_function = back_function  # Išsaugome `back_function` kaip klasės atributą

    def clear_window(self):
            """
            Išvalo visus elementus pagrindiniame `root` lange.
            """
            for widget in self.root.winfo_children():
                widget.destroy()

            # Jei naudojate `canvas` fono nustatymui, galite jį atkurti čia
            result = set_background(self.root)
            if result:
                self.canvas, self.background_image = result
            else:
                messagebox.showerror("Klaida", "Nepavyko sukurti `canvas` elemento.")

    def librarian_login_screen(self):
        self.clear_window()

        if not self.canvas:
            messagebox.showerror("Klaida", "Nepavyko sukurti `canvas` elemento.")
            return

        # Tekstų ir laukelių išdėstymas naudojant `canvas`
        self.canvas.create_text(700, 100, text="Bibliotekininko prisijungimas", font=("Arial", 30, "bold"),
                                fill="white")

        self.canvas.create_text(700, 200, text="Vartotojo vardas", font=("Arial", 20, "bold"), fill="white")
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.canvas.create_window(700, 250, window=self.username_entry)

        self.canvas.create_text(700, 300, text="Slaptažodis", font=("Arial", 20, "bold"), fill="white")
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.canvas.create_window(700, 350, window=self.password_entry)

        # Pridedame mygtukus prisijungimui, grįžimui ir išeiti iš programos
        self.add_button("Prisijungti", 500, self.verify_librarian)
        # Grįžimo mygtukas naudoja `back_function` per klasės atributą
        self.add_button("Atgal", 650, self.back_to_main)
        self.add_button("Išeiti iš sistemos", 800, self.root.quit)

    def verify_librarian(self):
        librarian_username = self.username_entry.get()
        librarian_password = self.password_entry.get()

        if self.authenticator.librarian_username_password_verification(librarian_username, librarian_password):
            librarian_info = self.get_librarian_info(librarian_username)
            if librarian_info:
                # Išsklaidome `librarian_info` į reikiamus laukus
                librarian_id, librarian_name, librarian_last_name, librarian_phone, librarian_email = librarian_info
                
                # Kuriame `Librarian` objektą su `librarian_id` ir likusia `librarian_info` dalimi
                self.librarian = Librarian(self.root, (librarian_name, librarian_last_name, librarian_phone, librarian_email), librarian_id)
                
                messagebox.showinfo("Prisijungta", f"Prisijungimas sėkmingas! Sveiki, {librarian_name} {librarian_last_name}.")
                
                self.librarian.show_menu()
        else:
            messagebox.showerror("Prisijungimas nepavyko",
                                f"Neteisingas vartotojo {librarian_username} vardas arba slaptažodis.")

    def get_librarian_info(self, username):
        try:
            with sqlite3.connect(self.authenticator.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT 
                                    bibliotekininko_id, vardas, pavarde, telefonas, email 
                                FROM 
                                    librarians 
                                WHERE 
                                    username = ?""", (username,))
                result = cursor.fetchone()

            return result if result else None
        except sqlite3.Error as e:
            messagebox.showerror("Klaida", f"Duomenų bazės klaida: {e}")
            return None

    def add_button(self, text, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                           command=command)

        self.canvas.create_window(700, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def back_to_main(self):
        """Grąžina į pagrindinį langą, kviesdamas `back_function`"""
        if self.back_function:
            self.clear_window()
            self.back_function()

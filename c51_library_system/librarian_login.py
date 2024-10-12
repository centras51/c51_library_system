import tkinter as tk
from tkinter import messagebox, Toplevel
from librarian import Librarian
import pandas as pd

class LibrarianLogin:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30  
        self.entry_font = ("Arial", 18)

    def username_password_verification(self, username, password):
        try:
            usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
            user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
            if not user_info.empty:
                return user_info['password'].values[0] == password
            return False
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Duomenų bazė nerasta")
            return False

    def librarian_login_screen(self, back_function):
        self.clear_window()

        tk.Label(self.root, text="Bibliotekininko prisijungimas", font=("Arial", 30)).pack(pady=20)

        tk.Label(self.root, text="Vartotojo vardas", font=("Arial", 20)).pack(pady=5)
        username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Slaptažodis", font=("Arial", 20)).pack(pady=5)
        password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        password_entry.pack(pady=5)

        librarian = Librarian(self.root)

        def verify_librarian():
            username = username_entry.get()
            password = password_entry.get()

            if self.username_password_verification(username, password):
                self.show_custom_popup(f"Sveiki, {username.capitalize}!")  
                librarian.show_menu()
            else:
                messagebox.showerror("Prisijungimas nepavyko", f"Neteisingas vartotojo {username} vardas arba slaptažodis.")

        tk.Button(self.root, text="Prisijungti", font=("Arial", 15), width=self.button_width, height=self.button_height, command=verify_librarian).pack(pady=10)
        tk.Button(self.root, text="Atgal", font=("Arial", 15), width=self.button_width, height=self.button_height, command=back_function).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=10)

    def show_custom_popup(self, message):
        """Sukuriamas pritaikytas iššokantis langas su didesniu dydžiu"""
        popup = Toplevel(self.root)
        popup.title("Prisijungimas sėkmingas")

        popup.geometry("400x200")  
        tk.Label(popup, text=message, font=("Arial", 24)).pack(pady=50)
        
        tk.Button(popup, text="Gerai", font=("Arial", 15), command=popup.destroy).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

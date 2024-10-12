import tkinter as tk
from tkinter import messagebox
from reader import Reader
import pandas as pd

class ReaderLogin:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30  
        self.entry_font = ("Arial", 18)  
        self.reader = None  

    def reader_login_screen(self, back_function):
        self.clear_window()

        tk.Label(self.root, text="Skaitytojo prisijungimas", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Vartotojo vardas", font=("Arial", 15)).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Slaptažodis", font=("Arial", 15)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Prisijungti", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.verify_reader).pack(pady=10)
        tk.Button(self.root, text="Atgal", font=("Arial", 15), width=self.button_width, height=self.button_height, command=back_function).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=10)

    def username_password_verification(self, username, password):
        try:
            usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv")
            user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
            if not user_info.empty:
                return user_info['password'].values[0] == password
            return False
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Nepavyksta patikrinti slaptažodžio")
            return False

    def verify_reader(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.username_password_verification(username, password):
            messagebox.showinfo("Sėkmingai prisijungėte", f"Sveiki atvykę, {username.capitalize()}!")
            self.reader = Reader(self.root)  
            self.reader.show_menu()
        else:
            messagebox.showerror("Prisijungimas nepavyko", f"Neteisingas vartotojo {username} vardas arba slaptažodis.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

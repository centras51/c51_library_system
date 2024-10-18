import tkinter as tk
from tkinter import messagebox
from reader import Reader
import pandas as pd
from PIL import Image, ImageTk


class ReaderLogin:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30
        self.entry_font = ("Arial", 18)
        self.reader = None

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def reader_login_screen(self, back_function):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Skaitytojo prisijungimas", font=("Arial", 30, "bold"), fill="white")

        self.canvas.create_text(700, 200, text="Vartotojo vardas", font=("Arial", 20, "bold"), fill="white")
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.canvas.create_window(700, 250, window=self.username_entry)

        self.canvas.create_text(700, 300, text="Slaptažodis", font=("Arial", 20, "bold"), fill="white")
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.canvas.create_window(700, 350, window=self.password_entry)

        self.add_button("Prisijungti", 500, self.verify_reader)
        self.add_button("Atgal", 650, back_function)
        self.add_button("Išeiti iš sistemos", 800, self.root.quit)

    def add_button(self, text, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                           command=command)

        self.canvas.create_window(700, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def verify_reader(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.username_password_verification(username, password):
            reader_card_number = self.get_reader_card_number(username)

            if reader_card_number:
                self.reader = Reader(self.root, reader_card_number)
            else:
                messagebox.showerror("Klaida", "Skaitytojo kortelės numeris nerastas.")
        else:
            messagebox.showerror("Klaida", "Neteisingas vartotojo vardas arba slaptažodis.")

    def get_reader_card_number(self, username):
        try:
            readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            reader_info = readers_df[readers_df['username'] == username]
            if not reader_info.empty:
                return reader_info['skaitytojo_kortele'].values[0]
            else:
                return None
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Skaitytojų duomenų bazės failas nerastas.")
            return None

    def username_password_verification(self, username, password):
        try:
            usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
            if not user_info.empty:
                return user_info['password'].values[0] == password
            return False
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Nepavyksta patikrinti slaptažodžio")
            return False

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

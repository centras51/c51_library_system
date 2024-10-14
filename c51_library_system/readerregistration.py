import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import re
from PIL import Image, ImageTk

class ReaderRegistration:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30  
        self.entry_font = ("Arial", 18)

        # Įkeliamas paveikslėlis ir nustatomas jo fiksuotas dydis 1400x800
        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Canvas nustatymas
        self.canvas = None

    def clear_window(self):
        """Išvalyti visus esamus lango valdiklius."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def register(self):
        """Naujo skaitytojo registracijos forma naudojant Tkinter."""
        self.clear_window()

        # Sukuriame naują „Canvas“ po lango išvalymo
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 50, text="Naujo skaitytojo registracija", font=("Arial", 30, "bold"), fill="green")

        tk.Label(self.root, text="Vardas", font=("Arial", 20)).pack(pady=5)
        reader_name = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        reader_name.pack(pady=5)

        tk.Label(self.root, text="Pavardė", font=("Arial", 20)).pack(pady=5)
        reader_last_name = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        reader_last_name.pack(pady=5)

        tk.Label(self.root, text="El. paštas", font=("Arial", 20)).pack(pady=5)
        reader_email = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        reader_email.pack(pady=5)

        tk.Label(self.root, text="Telefono numeris (+370)", font=("Arial", 20)).pack(pady=5)
        reader_phone = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        reader_phone.pack(pady=5)

        tk.Label(self.root, text="Prisijungimo vardas", font=("Arial", 20)).pack(pady=5)
        new_username = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        new_username.pack(pady=5)

        tk.Label(self.root, text="Slaptažodis", font=("Arial", 20)).pack(pady=5)
        new_password = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        new_password.pack(pady=5)

        tk.Label(self.root, text="Pakartokite slaptažodį", font=("Arial", 20)).pack(pady=5)
        new_password2 = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        new_password2.pack(pady=5)

        def submit_registration():
            if not reader_name.get().isalpha() or not reader_last_name.get().isalpha():
                messagebox.showerror("Klaida", "Vardą ir pavardę turi sudaryti tik raidės!")
            elif not self.is_valid_email(reader_email.get()):
                messagebox.showerror("Klaida", "Neteisingas el. pašto formatas!")
            elif not self.is_valid_phone(reader_phone.get()):
                messagebox.showerror("Klaida", "Neteisingas telefono numeris! Numeris turi būti 8 skaitmenų, prasidedantis 6.")
            elif new_password.get() != new_password2.get():
                messagebox.showerror("Klaida", "Slaptažodžiai nesutampa!")
            else:
                reader_card_number = self.reader_card_number_generator()
                self.save_reader_datas(
                    reader_name.get(), 
                    reader_last_name.get(), 
                    reader_email.get(), 
                    "+370" + reader_phone.get(), 
                    reader_card_number
                )
                self.save_reader_password(
                    reader_name.get(), 
                    reader_last_name.get(), 
                    reader_email.get(), 
                    "+370" + reader_phone.get(), 
                    reader_card_number, 
                    new_username.get(), 
                    new_password.get()
                )
                messagebox.showinfo("Naujas skaitytojas užregistruotas", f"Sėkmingai užregistruotas {reader_name.get()} {reader_last_name.get()}. Jūsų skaitytojo kortelės numeris: {reader_card_number}")
        
        tk.Button(self.root, text="Registruotis", font=("Arial", 15), width=self.button_width, height=self.button_height, command=submit_registration).pack(pady=20)

        # Atgal ir Išeiti mygtukai
        tk.Button(self.root, text="Atgal", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.go_back_to_login).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=10)

    def is_valid_email(self, reader_email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, reader_email) is not None
    
    def is_valid_phone(self, reader_phone):
        return reader_phone.isdigit() and len(reader_phone) == 8 and reader_phone.startswith("6")

    def reader_card_number_generator(self):
        """Generuoti unikalų skaitytojo kortelės numerį."""
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        existing_reader_card_numbers = reader_df['skaitytojo_kortele'].to_list()
        while True:
            reader_card_number = random.randint(10000000, 99999999)
            if reader_card_number not in existing_reader_card_numbers:
                return reader_card_number

    def save_reader_datas(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number):
        new_reader_line = {
            'vardas': reader_name, 
            'pavarde': reader_last_name, 
            'email': reader_email, 
            'telefonas': reader_phone, 
            'skaitytojo_kortele': reader_card_number
        }
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding='utf-8')

    def save_reader_password(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number, new_username, new_password):
        new_reader_line = {
            'vardas': reader_name, 
            'pavarde': reader_last_name, 
            'email': reader_email, 
            'telefonas': reader_phone, 
            'skaitytojo_kortele': reader_card_number, 
            'username': new_username, 
            'password': new_password
        }
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding='utf-8')

    def go_back_to_login(self):
        """Grįžti į prisijungimo ekraną."""
        from main import LibraryApp
        self.clear_window()
        LibraryApp(self.root)

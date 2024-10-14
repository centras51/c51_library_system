import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import re
from PIL import Image, ImageTk

class ReaderRegistration:
    def __init__(self, root):
        self.root = root
        self.button_width = 30
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

        # Pavadinimas
        self.canvas.create_text(700, 50, text="Naujo skaitytojo registracija", font=("Arial", 30, "bold"), fill="green")

        # Vardas
        self.canvas.create_text(200, 150, text="Vardas", font=("Arial", 20, "bold"), fill="green")
        self.reader_name_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 150, window=self.reader_name_entry)

        # Pavardė
        self.canvas.create_text(200, 200, text="Pavardė", font=("Arial", 20, "bold"), fill="green")
        self.reader_last_name_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 200, window=self.reader_last_name_entry)

        # El. paštas
        self.canvas.create_text(200, 250, text="El. paštas", font=("Arial", 20, "bold"), fill="green")
        self.reader_email_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 250, window=self.reader_email_entry)

        # Telefono numeris
        self.canvas.create_text(200, 300, text="Telefono numeris (+370)", font=("Arial", 20, "bold"), fill="green")
        self.reader_phone_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 300, window=self.reader_phone_entry)

        # Prisijungimo vardas
        self.canvas.create_text(200, 350, text="Prisijungimo vardas", font=("Arial", 20, "bold"), fill="green")
        self.new_username_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 350, window=self.new_username_entry)

        # Slaptažodis
        self.canvas.create_text(200, 400, text="Slaptažodis", font=("Arial", 20, "bold"), fill="green")
        self.new_password_entry = tk.Entry(self.root, font=("Arial", 18), width=30, show='*')
        self.canvas.create_window(700, 400, window=self.new_password_entry)

        # Pakartokite slaptažodį
        self.canvas.create_text(200, 450, text="Pakartokite slaptažodį", font=("Arial", 20, "bold"), fill="green")
        self.new_password2_entry = tk.Entry(self.root, font=("Arial", 18), width=30, show='*')
        self.canvas.create_window(700, 450, window=self.new_password2_entry)

        # Mygtukas Registruotis
        self.register_button = tk.Button(self.canvas, text="Registruotis", font=("Arial", 18), width=28, height=2, command=self.save_reader_datas)
        self.canvas.create_window(700, 550, window=self.register_button)

        # Mygtukas Atgal
        back_button = tk.Button(self.canvas, text="Atgal", font=("Arial", 15), width=16, height=2, command=self.go_back_to_login)
        self.canvas.create_window(600, 700, window=back_button)

        # Mygtukas Išeiti
        exit_button = tk.Button(self.canvas, text="Išeiti iš sistemos", font=("Arial", 15), width=16, height=2, command=self.root.quit)
        self.canvas.create_window(800, 700, window=exit_button)


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

    def save_reader_datas(self):
        """Išsaugoti skaitytojo registracijos duomenis."""
        reader_name = self.reader_name_entry.get()
        reader_last_name = self.reader_last_name_entry.get()
        reader_email = self.reader_email_entry.get()
        reader_phone = self.reader_phone_entry.get()
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_password2 = self.new_password2_entry.get()
        reader_card_number = self.reader_card_number_generator()

        # Validacijos tikrinimas
        if not reader_name or not reader_last_name:
            messagebox.showerror("Klaida", "Vardas ir pavardė privalomi.")
            return

        if not self.is_valid_email(reader_email):
            messagebox.showerror("Klaida", "Neteisingas el. pašto formatas.")
            return

        if not self.is_valid_phone(reader_phone):
            messagebox.showerror("Klaida", "Neteisingas telefono numeris. Turėtų prasidėti su '6' ir turėti 8 skaitmenis.")
            return

        if new_password != new_password2:
            messagebox.showerror("Klaida", "Slaptažodžiai nesutampa.")
            return

        # Išsaugoti duomenis
        new_reader_line = {
            'vardas': reader_name,
            'pavarde': reader_last_name,
            'email': reader_email,
            'telefonas': reader_phone,
            'skaitytojo_kortele': reader_card_number,
            'username': new_username,
            'password': new_password
        }

        try:
            reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
            reader_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding='utf-8')
            messagebox.showinfo("Registracija baigta", f"Skaitytojas {new_reader_line['vardas']} {new_reader_line['pavarde']} sėkmingai užregistruotas!")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Nepavyko rasti skaitytojų duomenų failo.")

    def go_back_to_login(self):
        """Grįžti į prisijungimo ekraną."""
        from main import LibraryApp
        self.clear_window()
        LibraryApp(self.root)

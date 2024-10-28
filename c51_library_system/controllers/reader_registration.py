import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from utils.validation_helpers import Validator
from ui.ui_helpers import set_background
from utils.general_helpers import Generator
from utils.csv_helpers import CsvProcessor
from utils.navigation_helpers import Navigator


class ReaderRegistration:
    def __init__(self, root, is_librarian=False):
        self.root = root
        self.is_librarian = is_librarian
        self.validator = Validator()
        self.generator = Generator()
        self.csvprocessor = CsvProcessor()
        self.navigator = Navigator()
        self.canvas = None
        self.background_image = None
        self.button_width = 30
        self.button_height = 3
        self.entry_width = 30
        self.entry_font = ("Arial", 18)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register(self):
        self.clear_window()
        
        self.canvas, self.background_image = set_background(self.root)

        self.canvas.create_text(700, 50, text="Naujo skaitytojo registracija", font=("Arial", 30, "bold"), fill="white")

        self.canvas.create_text(200, 150, text="Vardas", font=("Arial", 20, "bold"), fill="white")
        self.reader_name_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 150, window=self.reader_name_entry)

        self.canvas.create_text(200, 200, text="Pavardė", font=("Arial", 20, "bold"), fill="white")
        self.reader_last_name_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 200, window=self.reader_last_name_entry)

        self.canvas.create_text(200, 250, text="El. paštas", font=("Arial", 20, "bold"), fill="white")
        self.reader_email_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 250, window=self.reader_email_entry)

        self.canvas.create_text(200, 300, text="Telefono numeris (+370)", font=("Arial", 20, "bold"), fill="white")
        self.reader_phone_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
        self.canvas.create_window(700, 300, window=self.reader_phone_entry)

        if not self.is_librarian:
            self.canvas.create_text(200, 350, text="Prisijungimo vardas", font=("Arial", 20, "bold"), fill="white")
            self.new_username_entry = tk.Entry(self.root, font=("Arial", 18), width=30)
            self.canvas.create_window(700, 350, window=self.new_username_entry)

            self.canvas.create_text(200, 400, text="Slaptažodis", font=("Arial", 20, "bold"), fill="white")
            self.new_password_entry = tk.Entry(self.root, font=("Arial", 18), width=30, show='*')
            self.canvas.create_window(700, 400, window=self.new_password_entry)

            self.canvas.create_text(200, 450, text="Pakartokite slaptažodį", font=("Arial", 20, "bold"), fill="white")
            self.new_password2_entry = tk.Entry(self.root, font=("Arial", 18), width=30, show='*')
            self.canvas.create_window(700, 450, window=self.new_password2_entry)

        self.add_button("Registruoti", 700, 550, self.save_reader_datas)
        self.add_button("Atgal į \npagrindinį langą", 200, 550, lambda: self.navigator.go_back_to_login(self.root))
        self.add_button("Išeiti iš sistemos", 1200, 550, self.root.quit)

    def save_reader_datas(self):
        reader_name = self.reader_name_entry.get()
        reader_last_name = self.reader_last_name_entry.get()
        reader_email = self.reader_email_entry.get()
        reader_phone = self.reader_phone_entry.get()
        reader_card_number = self.generator.reader_card_number_generator()

        if self.is_librarian:
            new_username, new_password = self.generator.generate_username_password()
        else:
            new_username = self.new_username_entry.get()
            new_password = self.new_password_entry.get()
            new_password2 = self.new_password2_entry.get()

            if new_password != new_password2:
                messagebox.showerror("Klaida", "Slaptažodžiai nesutampa.")
                return
    
        if not reader_name or not reader_last_name:
            messagebox.showerror("Klaida", 
                                 "Vardas ir pavardė privalomi.")
            return

        if not self.validator.is_valid_reader_name(reader_name):
            messagebox.showerror("Klaida",
                                 "Neteisingas vardas. Vardo negali sudaryti skaičiai ar specialieji simboliai.")
            return           
        
        if not self.validator.is_valid_reader_last_name(reader_last_name):
            messagebox.showerror("Klaida",
                                 "Neteisinga Pavardė. Pavardės negali sudaryti skaičiai ar specialieji simboliai.")
            return 

        if not self.validator.is_valid_email(reader_email):
            messagebox.showerror("Klaida", 
                                 "Neteisingas el. pašto formatas.")
            return

        if not self.validator.is_valid_phone(reader_phone):
            messagebox.showerror("Klaida",
                                 "Neteisingas telefono numeris. Turėtų prasidėti su '6' ir turėti 8 skaitmenis.")
            return

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
            reader_df = self.csvprocessor.read_readers_csv()
            reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
            self.csvprocessor.write_reader_csv(reader_df)
            try:
                messagebox.showinfo("Registracija baigta",
                                f"Skaitytojas {new_reader_line['vardas']} {new_reader_line['pavarde']} sėkmingai užregistruotas!")
                self.navigator.go_back_to_login(self.root)
            except Exception as e:
                messagebox.showerror("Klaida", f"Nepavyko užregistruoti: {str(e)}")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Nepavyko rasti skaitytojų duomenų failo.")
            
    def add_button(self, text, x_position, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                        bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                        command=command)

        # Naudojame x_position ir y_position
        self.canvas.create_window(x_position, y_position, window=button)

        # Pridedame hover efektus
        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

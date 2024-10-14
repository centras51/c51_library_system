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

        # Įkeliamas paveikslėlis ir nustatomas jo fiksuotas dydis 1400x800
        self.original_image = Image.open(r"D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Sukuriame Canvas ir nustatome paveikslėlį kaip foną
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Nustatome paveikslėlį kaip fono paveikslėlį
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def reader_login_screen(self, back_function):
        self.clear_window()

        # Sukuriame naują „Canvas“ po lango išvalymo
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Skaitytojo prisijungimas", font=("Arial", 30), fill="black")

        self.canvas.create_text(700, 200, text="Vartotojo vardas", font=("Arial", 20), fill="black")
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.canvas.create_window(700, 250, window=self.username_entry)

        self.canvas.create_text(700, 300, text="Slaptažodis", font=("Arial", 20), fill="black")
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.canvas.create_window(700, 350, window=self.password_entry)

        # Mygtukų su hover efektais pridėjimas
        self.add_button("Prisijungti", 400, self.verify_reader)
        self.add_button("Atgal", 500, back_function)
        self.add_button("Išeiti iš sistemos", 600, self.root.quit)

    def add_button(self, text, y_position, command):
        """Sukurti mygtuką su efektais"""
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        # Įdedame mygtuką į drobę (canvas)
        self.canvas.create_window(700, y_position, window=button)

        # Pridedame "hover" efektus
        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def username_password_verification(self, username, password):
        try:
            usr_psw_df = pd.read_csv(r"D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv")
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

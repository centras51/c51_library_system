import tkinter as tk
from tkinter import messagebox, Toplevel
from librarian import Librarian
import pandas as pd
from PIL import Image, ImageTk

class LibrarianLogin:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30  
        self.entry_font = ("Arial", 18)

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def username_password_verification(self, username, password):
        try:
            usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
            user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
            if not user_info.empty and user_info['password'].values[0] == password:
                return user_info[['vardas', 'pavarde', 'telefonas', 'email']].values[0] # Grąžina bibliotekininko informaciją
            return None
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Duomenų bazė nerasta")
            return None

    def librarian_login_screen(self, back_function):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Bibliotekininko prisijungimas", font=("Arial", 30, "bold"), fill="white")

        self.canvas.create_text(700, 200, text="Vartotojo vardas", font=("Arial", 20, "bold"), fill="white")
        self.username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        self.canvas.create_window(700, 250, window=self.username_entry)

        self.canvas.create_text(700, 300, text="Slaptažodis", font=("Arial", 20, "bold"), fill="white")
        self.password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        self.canvas.create_window(700, 350, window=self.password_entry)

        def verify_librarian():
            username = self.username_entry.get()
            password = self.password_entry.get()

            librarian_info = self.username_password_verification(username, password)
            if librarian_info is not None and librarian_info.size > 0:  
                self.clear_window()  
                librarian = Librarian(self.root, librarian_info)  
                librarian.show_menu()  
            else:
                messagebox.showerror("Prisijungimas nepavyko", f"Neteisingas vartotojo {username} vardas arba slaptažodis.")

        self.add_button("Prisijungti", 500, verify_librarian)
        self.add_button("Atgal", 650, back_function)  
        self.add_button("Išeiti iš sistemos", 800, self.root.quit)

    def add_button(self, text, y_position, command):
        """Sukurti mygtuką su efektais"""
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(700, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def clear_window(self):
        """Išvalyti visus lango elementus"""
        for widget in self.root.winfo_children():
            widget.destroy()

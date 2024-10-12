import tkinter as tk
from tkinter import messagebox
from reader import Reader

class ReaderLogin:
    def __init__(self, root):
        self.root = root
        self.button_width = 60
        self.button_height = 3
        self.entry_width = 30  
        self.entry_font = ("Arial", 18)  
        
    def reader_login_screen(self, back_function):
        self.clear_window()

        tk.Label(self.root, text="Skaitytojo prisijungimas", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Vartotojo vardas", font=("Arial", 15)).pack(pady=5)
        username_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Slaptažodis", font=("Arial", 15)).pack(pady=5)
        password_entry = tk.Entry(self.root, font=self.entry_font, width=self.entry_width, show='*')
        password_entry.pack(pady=5)

        reader = Reader(self.root)  

        def verify_reader():
            username = username_entry.get()
            password = password_entry.get()

            if reader.username_password_verification(username, password):
                messagebox.showinfo("Sėkmingai prisijungėte", f"Sveiki atvykę, {username}!")
                reader.show_menu()
            else:
                messagebox.showerror("Prisijungimas nepavyko", f"Neteisingas vartotojo {username} vardas arba slaptažodis.")

        tk.Button(self.root, text="Prisijungti", font=("Arial", 15), width=self.button_width, height=self.button_height, command=verify_reader).pack(pady=10)
        tk.Button(self.root, text="Atgal", font=("Arial", 15), width=self.button_width, height=self.button_height, command=back_function).pack(pady=10)  
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

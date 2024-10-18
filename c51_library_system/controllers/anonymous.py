import tkinter as tk
from books import Books
from PIL import Image, ImageTk
from readerregistration import ReaderRegistration


class AnonymousUser:
    def __init__(self, root):
        self.root = root
        self.books_instance = Books(self.root, is_anonymous=True)
        self.readerregistration_instance = ReaderRegistration(self.root)
        self.button_width = 30
        self.button_height = 3

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.show_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(350, 50, text=f"Knygos išduodamos bibliotekoje su skaitytojo registracija",
                                font=("Arial", 15, "bold"), fill="white", anchor="nw")

        self.add_button("Peržiūrėti knygas", 700, 200, self.books_instance.show_books)
        self.add_button("Skaitytojo registracija", 700, 350, self.readerregistration_instance.register)
        self.add_button("Atgal į prisijungimo langą", 700, 500, self.go_back_to_login)
        self.add_button("Išeiti iš sistemos", 700, 650, self.root.quit)

    def add_button(self, text, x_position, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white",
                           command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def go_back_to_login(self):
        from main import LibraryApp
        library_app = LibraryApp(self.root)
        library_app.login_menu()

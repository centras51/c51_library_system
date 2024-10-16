import tkinter as tk
from PIL import Image, ImageTk
from controllers.anonymous import AnonymousUser
from controllers.librarian_login import LibrarianLogin
from controllers.reader_login import ReaderLogin
from controllers.reader_registration import ReaderRegistration


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BIBLIOTEKOS SISTEMA")
        self.root.geometry("1400x800")
        self.readerregistration_instance = ReaderRegistration(self.root)
        self.button_width = 60
        self.button_height = 3

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1600, 1000), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.login_menu()

    def login_menu(self):
        self.clear_window()
        
        self.canvas.create_text(700, 100, text="BIBLIOTEKOS SISTEMA", font=("Arial", 30, "bold"), fill="white")

        self.add_button("Bibliotekininko prisijungimas", 200, self.librarian_login)
        self.add_button("Skaitytojo prisijungimas", 300, self.reader_login)
        self.add_button("Dirbti neprisijungus", 400, self.anonymous_environment)
        self.add_button("Naujo skaitytojo registracija", 500, self.readerregistration_instance.register)
        self.add_button("Išeiti iš sistemos", 600, self.root.quit)

    def add_button(self, text, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(700, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def librarian_login(self):
        self.clear_window()
        login = LibrarianLogin(self.root)
        login.librarian_login_screen(self.login_menu)

    def reader_login(self):
        self.clear_window()
        login = ReaderLogin(self.root)
        login.reader_login_screen(self.login_menu)

    def anonymous_environment(self):
        self.clear_window()
        anonymous = AnonymousUser(self.root)
        anonymous.show_menu()

    def register_reader(self):
        self.clear_window()

        tk.Label(self.root, text="Skaitytojo registracija", font=("Arial", 20)).pack(pady=20)

        registration = ReaderRegistration()
        registration.register(self.root) 

        tk.Button(self.root, text="Atgal", command=self.login_menu).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Canvas):  
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

import tkinter as tk
from readerregistration import ReaderRegistration
from librarian_login import LibrarianLogin
from reader_login import ReaderLogin

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C51 BIBLIOTEKOS SISTEMA")
        self.root.geometry("1400x800")
        self.button_width = 60
        self.button_height = 3
        self.login_menu()
        

    def login_menu(self):
        """Pagrindinis langas"""
        self.clear_window()
        tk.Label(self.root, text="C51 BIBLIOTEKOS SISTEMA", font=("Arial", 30)).pack(pady=20)

        tk.Button(self.root, text="Bibliotekininko prisijungimas", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.librarian_login).pack(pady=8)
        tk.Button(self.root, text="Skaitytojo prisijungimas", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.reader_login).pack(pady=8)
        tk.Button(self.root, text="Dirbti neprisijungus", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.anonymous_environment).pack(pady=8)
        tk.Button(self.root, text="Naujo skaitytojo registracija", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.register_reader).pack(pady=8)
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=8)

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

        tk.Label(self.root, text="Anoniminė peržiūra", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Atgal", command=self.login_menu).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", command=self.root.quit).pack(pady=10)

    def register_reader(self):
        self.clear_window()

        tk.Label(self.root, text="Skaitytojo registracija", font=("Arial", 20)).pack(pady=20)

        registration = ReaderRegistration()
        registration.register(self.root) 

        tk.Button(self.root, text="Back", command=self.login_menu).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

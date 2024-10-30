import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

# Nustatome kelią, kad galėtume importuoti modulį iš aukštesnio lygio katalogo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importuojame įvairias klases iš kitų failų
from controllers.anonymous import AnonymousUser
from controllers.librarian_login import LibrarianLogin
from controllers.reader_login import ReaderLogin
from controllers.reader_registration import ReaderRegistration
from ui.ui_helpers import set_background


class LibraryApp:
    def __init__(self, root):
        """
        Klasės inicializacija, apibrėžianti pagrindinį langą, foną ir nustatanti programos struktūrą.
        """
        self.root = root
        self.root.title("BIBLIOTEKOS SISTEMA")
        self.root.geometry("1400x800")
        
        # Skaitytojo registracijos instancijos sukūrimas, kad galėtume kviesti ją iš meniu
        self.readerregistration_instance = ReaderRegistration(self.root)
        
        # Nustatome mygtukų dydį
        self.button_width = 60
        self.button_height = 3

        self.canvas, self.background_image = set_background(self.root)

        # Sukuriame pradinį prisijungimo meniu
        self.login_menu()

    def login_menu(self):
        """
        Pagrindinio prisijungimo meniu kūrimas su pasirinkimais bibliotekininko, skaitytojo, anoniminio vartotojo 
        ir naujo skaitytojo registracijos prisijungimui.
        """
        self.clear_window()
        
        # Pagrindinio meniu tekstas
        self.canvas.create_text(700, 100, text="BIBLIOTEKOS SISTEMA", font=("Arial", 30, "bold"), fill="white")

        # Meniu mygtukų pridėjimas
        self.add_button("Bibliotekininko prisijungimas", 200, self.librarian_login)
        self.add_button("Skaitytojo prisijungimas", 300, self.reader_login)
        self.add_button("Dirbti neprisijungus", 400, self.anonymous_environment)
        self.add_button("Naujo skaitytojo registracija", 500, self.readerregistration_instance.register)
        self.add_button("Išeiti iš sistemos", 600, self.root.quit)

    def add_button(self, text, y_position, command):
        """
        Mygtukų kūrimas, priskiriant jiems poziciją, tekstą, komandą ir spalvų efektus.
        """
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)
        
        # Mygtuko pridėjimas į `canvas` nurodytoje vietoje
        self.canvas.create_window(700, y_position, window=button)

        # Hover efektas mygtukui
        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def librarian_login(self):
        self.clear_window()
        login = LibrarianLogin(self.root, back_function=self.login_menu)  # `self.login_menu` priskiriamas per `__init__`
        login.librarian_login_screen()

    def reader_login(self):
        """
        Skaitytojo prisijungimo lango inicijavimas, su `ReaderLogin` objektu.
        """
        self.clear_window()
        login = ReaderLogin(self.root)
        # Sukuriame skaitytojo prisijungimo ekraną, perduodant `login_menu` kaip „Atgal“ mygtuko funkciją
        login.reader_login_screen(self.login_menu)

    def anonymous_environment(self):
        """
        Anoniminės aplinkos rodymas, kurioje galima naudotis sistema neprisijungus.
        """
        self.clear_window()
        anonymous = AnonymousUser(self.root)
        anonymous.show_menu()

    def register_reader(self):
        """
        Skaitytojo registracijos lango inicijavimas ir nustatymas.
        """
        self.clear_window()

        # Pridedame pavadinimą ir mygtukus registracijai
        tk.Label(self.root, text="Skaitytojo registracija", font=("Arial", 20)).pack(pady=20)

        registration = ReaderRegistration()
        registration.register(self.root)

        tk.Button(self.root, text="Atgal", command=self.login_menu).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        """
        Išvalo visus `root` lango elementus, išskyrus `canvas`, kad foninis paveikslėlis liktų vietoje.
        """
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Canvas):  
                widget.destroy()

if __name__ == "__main__":
    # Programos pradžia
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

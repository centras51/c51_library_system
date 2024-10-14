import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
from books import Books
from readerregistration import ReaderRegistration

class Librarian:
    def __init__(self, root, librarian_info):
        self.root = root
        self.librarian_info = librarian_info  # Gauta informacija iš prisijungimo: vardas, pavardė, telefonas, email
        self.books_instance = Books(self.root)
        self.readerregistration_instance = ReaderRegistration(self.root)
        self.button_width = 35  
        self.button_height = 3  

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Pridedame bibliotekininko informaciją apačioje
        self.add_librarian_info()

        # Pagrindinio meniu iškvietimas paleidus klasę
        self.show_menu()

    def add_librarian_info(self):
        """Prideda bibliotekininko informaciją apačioje."""
        librarian_info_text = f"Bibliotekininkas: {self.librarian_info[0]} {self.librarian_info[1]}, Tel: {self.librarian_info[2]}, El. paštas: {self.librarian_info[3]}"
        librarian_label = tk.Label(self.root, text=librarian_info_text, font=("Arial", 12), bg="lightgray", fg="black")
        
        # Lipdukas apačioje
        self.canvas.create_window(700, 780, window=librarian_label, anchor="center")

    def clear_window(self):
        """Ši funkcija išvalo visus valdiklius langelyje."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self):
        """Bibliotekininko pagrindinis meniu."""
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Bibliotekininko aplinka", font=("Arial", 30, "bold"), fill="green")

        self.add_button("Peržiūrėti knygas", 250, 200, self.books_instance.show_books)  
        self.add_button("Pridėti knygą", 250, 350, self.books_instance.add_book)  
        self.add_button("Surasti knygą", 250, 500, self.books_instance.search_for_book)  
        self.add_button("Pašalinti knygą", 250, 650, self.books_instance.remove_book)  
        self.add_button("Išduoti knygą", 250, 750, self.lend_book)  

        self.add_button("Skaitytojų sąrašas", 750, 200, self.reader_list)  
        self.add_button("Surasti skaitytoją", 750, 350, self.find_reader)  
        self.add_button("Pridėti skaitytoją", 750, 500, self.readerregistration_instance.register)  
        self.add_button("Pašalinti skaitytoją", 750, 650, self.remove_reader)  

        self.add_button("Peržiūrėti darbuotojus", 1250, 200, self.show_librarians)  
        self.add_button("Atgal į prisijungimo langą", 1250, 350, self.go_back_to_login)  
        self.add_button("Išeiti iš sistemos", 1250, 500, self.root.quit)  

    def add_button(self, text, x_position, y_position, command):
        """Sukurti mygtuką ir pridėti jį į `canvas`."""
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                        bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def go_back_to_login(self):
        """Grįžti į prisijungimo langą."""
        from librarian_login import LibrarianLogin
        librarian_login = LibrarianLogin(self.root)
        librarian_login.librarian_login_screen(back_function=self.go_back_to_login)

    def lend_book(self):
        """Placeholder funkcija knygai išduoti."""
        messagebox.showinfo("Išduoti knygą", "Funkcija dar neįgyvendinta.")

    def reader_list(self):
        """Placeholder funkcija skaitytojų sąrašui peržiūrėti."""
        messagebox.showinfo("Skaitytojų sąrašas", "Funkcija dar neįgyvendinta.")

    def find_reader(self):
        """Surasti skaitytoją pagal tam tikrus kriterijus."""
        messagebox.showinfo("Surasti skaitytoją", "Skaitytojo paieška neįgyvendinta.")

    def remove_reader(self):
        """Pašalinti skaitytoją."""
        messagebox.showinfo("Pašalinti skaitytoją", "Funkcija dar neįgyvendinta.")

    def show_librarians(self):
        """Parodyti bibliotekininkų sąrašą."""
        try:
            librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
            selected_columns = librarians_df[['vardas', 'pavarde', 'email', 'telefonas']]
            selected_columns = selected_columns.reset_index(drop=True)

            self.clear_window()
            self.canvas = tk.Canvas(self.root, width=1400, height=800)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

            self.canvas.create_text(700, 100, text="Bibliotekininkų sąrašas", font=("Arial", 30), fill="black")

            for index, row in selected_columns.iterrows():
                librarian_info = f"Vardas: {row['vardas']}, Pavardė: {row['pavarde']}, El. paštas: {row['email']}, Telefonas: {row['telefonas']}"
                tk.Label(self.root, text=librarian_info).pack(pady=5)

            self.add_button("Atgal", 500, self.show_menu)

        except FileNotFoundError:
            messagebox.showerror("Klaida", "Bibliotekininkų sąrašas nerastas.")

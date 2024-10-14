import tkinter as tk
from tkinter import messagebox
import pandas as pd
from readerregistration import ReaderRegistration
from books import Books
from PIL import Image, ImageTk

readerregistration = ReaderRegistration()

class Librarian:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.books_instance = Books(self.root)
        self.button_width = 40  
        self.button_height = 4  

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

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

        self.canvas.create_text(700, 100, text="Bibliotekininko aplinka", font=("Arial", 30), fill="black")

        self.add_button("Peržiūrėti knygas", 250, 200, self.books_instance.show_books)  
        self.add_button("Pridėti knygą", 250, 350, self.add_book)  
        self.add_button("Surasti knygą", 250, 500, self.search_for_book)  
        self.add_button("Pašalinti knygą", 250, 650, self.remove_book)  
        self.add_button("Išduoti knygą", 250, 650, self.lend_book)  

        self.add_button("Skaitytojų sąrašas", 750, 200, self.reader_list)  
        self.add_button("Surasti skaitytoją", 750, 350, self.find_reader)  
        self.add_button("Pridėti skaitytoją", 750, 500, self.add_reader)  
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
        from librarian_login import LibrarianLogin
        librarian_login = LibrarianLogin(self.root)
        librarian_login.librarian_login_screen(back_function=self.go_back_to_login)

    def show_books(self):
        """Parodo visų knygų sąrašą."""
        books = Books()    
        books.show_books()

    def search_for_book(self):
        """Ieškoti knygos pagal pavadinimą, autorių ar ISBN."""
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Paieškos langas", font=("Arial", 30), fill="black")
        self.canvas.create_text(700, 200, text="Įveskite knygos pavadinimą, autorių, metus arba ISBN", font=("Arial", 20), fill="black")
        search_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=search_entry)

        def search():
            search_query = search_entry.get()
            search_results = self.books_instance.find_book(search_query)
            if not search_results.empty:
                for index, row in search_results.iterrows():
                    book_info = f"Knygos pavadinimas: {row['knygos_pavadinimas']}, Rašytojas: {row['autorius']}, ISBN: {row['ISBN']}, Metai: {row['metai']}"
                    book_label = tk.Label(self.root, text=book_info)
                    book_label.pack(pady=5)
                    book_label.bind("<Button-1>", lambda e, book=row: self.books_instance.show_book_profile(book))
            else:
                tk.Label(self.root, text="Knygų nerasta.").pack(pady=5)

        self.add_button("Ieškoti", 400, search)
        self.add_button("Atgal", 500, self.show_menu)

        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Pašalinti knygą", font=("Arial", 30), fill="black")
        self.canvas.create_text(700, 200, text="Įveskite ISBN numerį", font=("Arial", 20), fill="black")
        isbn_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=isbn_entry)

        isbn = isbn_entry.get()
        if not isbn.isnumeric():
            messagebox.showerror("Klaida", "ISBN numerį sudaro tik skaičiai.")
            return

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų bazė nerasta")
            return

        book_to_delete = books_df[books_df["ISBN"] == isbn]
        books_df_filtered = books_df[books_df["ISBN"] != isbn]

        if book_to_delete.empty:
            messagebox.showwarning("Įspėjimas", f"Knyga su ISBN {isbn} nerasta.")
        else:
            try:
                deleted_books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\deleted_books_db.csv")
            except FileNotFoundError:
                deleted_books_df = pd.DataFrame(columns=books_df.columns)

            deleted_books_df = pd.concat([deleted_books_df, book_to_delete], ignore_index=True)
            deleted_books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\deleted_books_db.csv", index=False, encoding="UTF-8")

            books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding="UTF-8")
            messagebox.showinfo("Sėkmė", f"Knyga su ISBN {isbn} sėkmingai ištrinta ir perkelta į ištrintų knygų sąrašą.")

    def lend_book():
        pass
    
    def add_book(self):
        """Pridėti naują knygą į sistemą."""
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Pridėti naują knygą į sistemą", font=("Arial", 30), fill="black")

        self.canvas.create_text(700, 200, text="Knygos autorius", font=("Arial", 20), fill="black")
        author_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=author_entry)

        self.canvas.create_text(700, 300, text="Knygos pavadinimas", font=("Arial", 20), fill="black")
        title_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 350, window=title_entry)

        self.canvas.create_text(700, 400, text="Knygos išleidimo metai", font=("Arial", 20), fill="black")
        year_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 450, window=year_entry)

        self.canvas.create_text(700, 500, text="Knygos ISBN", font=("Arial", 20), fill="black")
        isbn_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 550, window=isbn_entry)

        self.canvas.create_text(700, 600, text="Knygos žanras", font=("Arial", 20), fill="black")
        genre_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 650, window=genre_entry)

        self.canvas.create_text(700, 700, text="Trumpas knygos aprašymas", font=("Arial", 20), fill="black")
        about_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 750, window=about_entry)

        def submit_book():
            author = author_entry.get()
            title = title_entry.get()
            year = year_entry.get()
            isbn = isbn_entry.get()
            genre = genre_entry.get()
            about = about_entry.get()

            new_book = {'autorius': author, 'knygos_pavadinimas': title, 'metai': year, 'ISBN': isbn, 'zanras': genre, 'pastabos': about}

            try:
                books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
                books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
                books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')
                messagebox.showinfo("Sėkmė", f"Knyga '{title}' sėkmingai pridėta!")
            except FileNotFoundError:
                messagebox.showerror("Klaida", "Knygų duomenų failas nerastas.")

        self.add_button("Patvirtinti pridėjimą", 800, submit_book)
        self.add_button("Atgal", 850, self.show_menu)

    def reader_list(self):
        """Placeholder funkcija skaitytojų sąrašui peržiūrėti."""
        messagebox.showinfo("Skaitytojų sąrašas", "Funkcija dar neįgyvendinta.")

    def find_reader(self):
        """Surasti skaitytoją pagal tam tikrus kriterijus."""
        messagebox.showinfo("Surasti skaitytoją", "Skaitytojo paieška neįgyvendinta.")

    def add_reader(self):
        """Pridėti naują skaitytoją."""
        readerregistration.register()

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



import tkinter as tk
from tkinter import messagebox
import pandas as pd
from readerregistration import ReaderRegistration
from books import Books

class Librarian:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.password = None
        self.books_instance = Books(self.root)
        self.button_width = 20
        self.button_height = 2

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    

    def show_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Bibliotekininko aplinka", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Peržiūrėti knygas", width=self.button_width, height=self.button_height, command=self.books_instance.show_books).pack(pady=10)
        tk.Button(self.root, text="Pridėti knygą", width=self.button_width, height=self.button_height, command=self.add_book).pack(pady=10)
        tk.Button(self.root, text="Surasti knygą", width=self.button_width, height=self.button_height, command=self.search_for_book).pack(pady=10)
        tk.Button(self.root, text="Surasti skaitytoją", width=self.button_width, height=self.button_height, command=self.find_reader).pack(pady=10)
        tk.Button(self.root, text="Pašalinti knygą", width=self.button_width, height=self.button_height, command=self.remove_book).pack(pady=10)
        tk.Button(self.root, text="Pridėti skaitytoją", width=self.button_width, height=self.button_height, command=lambda: ReaderRegistration(self.root)).pack(pady=10)
        tk.Button(self.root, text="Skaitytojų sąrašas", width=self.button_width, height=self.button_height, command=self.reader_list).pack(pady=10)
        tk.Button(self.root, text="Pašalinti skaitytoją", width=self.button_width, height=self.button_height, command=self.remove_reader).pack(pady=10)
        tk.Button(self.root, text="Peržiūrėti darbuotojus", width=self.button_width, height=self.button_height, command=self.show_librarians).pack(pady=10)
        tk.Button(self.root, text="Atgal", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.go_back_to_login).pack(pady=10)
        tk.Button(self.root, text="Išeiti iš sistemos", font=("Arial", 15), width=self.button_width, height=self.button_height, command=self.root.quit).pack(pady=10)

    def go_back_to_login(self):
        from login import LibrarianLogin
        librarian_login = LibrarianLogin(self.root)
        librarian_login.librarian_login_screen(back_function=self.go_back_to_login)

    def search_for_book(self):
        self.clear_window()
        tk.Label(self.root, text="Paieškos langas", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Įveskite knygos pavadinimą, autorių, metus arba ISBN").pack(pady=5)
        search_entry = tk.Entry(self.root)
        search_entry.pack(pady=5)

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

        tk.Button(self.root, text="Ieškoti", width=self.button_width, height=self.button_height, command=search).pack(pady=10)
        tk.Button(self.root, text="Atgal", width=self.button_width, height=self.button_height, command=self.show_menu).pack(pady=10)

    def find_reader(self):
        messagebox.showinfo("Surasti skaitytoją", "Skaitytojo paieška neįgyvendinta.")

    def remove_book(self):
        self.clear_window()
        tk.Label(self.root, text="Pašalinti knygą", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Įveskite ISBN numerį").pack(pady=10)
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack(pady=10)

        def delete_book():
            isbn = isbn_entry.get()
            if not isbn.isnumeric():
                messagebox.showerror("Klaida", "ISBN numerį sudaro tik skaičiai.")
                return

            try:
                books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            except FileNotFoundError:
                messagebox.showerror("Klaida", "Knygų duomenų bazė nerasta")
                return

            books_df_filtered = books_df[books_df["ISBN"] != isbn]
            if len(books_df_filtered) == len(books_df):
                messagebox.showwarning("Įspėjimas", f"Knyga su ISBN {isbn} nerasta.")
            else:
                books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding="UTF-8")
                messagebox.showinfo("Sėkmė", f"Knyga su ISBN {isbn} sėkmingai ištrinta.")

        tk.Button(self.root, text="Ištrinti knygą", width=self.button_width, height=self.button_height, command=delete_book).pack(pady=10)
        tk.Button(self.root, text="Atgal", width=self.button_width, height=self.button_height, command=self.show_menu).pack(pady=10)

    def add_book(self):
        self.clear_window()
        tk.Label(self.root, text="Pridėti naują knygą į sistemą", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Knygos autorius").pack(pady=5)
        author_entry = tk.Entry(self.root)
        author_entry.pack(pady=5)
        tk.Label(self.root, text="Knygos pavadinimas").pack(pady=5)
        title_entry = tk.Entry(self.root)
        title_entry.pack(pady=5)
        tk.Label(self.root, text="Knygos išleidimo metai").pack(pady=5)
        year_entry = tk.Entry(self.root)
        year_entry.pack(pady=5)
        tk.Label(self.root, text="Knygos ISBN").pack(pady=5)
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack(pady=5)
        tk.Label(self.root, text="Knygos žanras").pack(pady=5)
        genre_entry = tk.Entry(self.root)
        genre_entry.pack(pady=5)
        tk.Label(self.root, text="Trumpas knygos aprašymas").pack(pady=5)
        about_entry = tk.Entry(self.root)
        about_entry.pack(pady=5)

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

        tk.Button(self.root, text="Patvirtinti pridėjimą", width=self.button_width, height=self.button_height, command=submit_book).pack(pady=10)
        tk.Button(self.root, text="Atgal", width=self.button_width, height=self.button_height, command=self.show_menu).pack(pady=10)

    def show_librarians(self):
        try:
            librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
            selected_columns = librarians_df[['vardas', 'pavarde', 'email', 'telefonas']]
            selected_columns = selected_columns.reset_index(drop=True)

            self.clear_window()
            tk.Label(self.root, text="Bibliotekininkų sąrašas", font=("Arial", 20)).pack(pady=20)

            for index, row in selected_columns.iterrows():
                librarian_info = f"Vardas: {row['vardas']}, Pavardė: {row['pavarde']}, El. paštas: {row['email']}, Telefonas: {row['telefonas']}"
                tk.Label(self.root, text=librarian_info).pack(pady=5)

            tk.Button(self.root, text="Atgal", width=self.button_width, height=self.button_height, command=self.show_menu).pack(pady=10)

        except FileNotFoundError:
            messagebox.showerror("Klaida", "Bibliotekininkų sąrašas nerastas.")

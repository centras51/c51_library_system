import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime

class Books:
    def __init__(self, root, is_anonymous=False):
        self.root = root
        self.is_anonymous = is_anonymous  # Anonimiškumo flag'as
        self.books_df = self.load_books()
        self.show_books()

    def load_books(self):
        try:
            df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            required_columns = {'knygos_pavadinimas', 'autorius', 'metai', 'ISBN', 'zanras', 'pastabos', 'knygos_statusas'}
            if not required_columns.issubset(df.columns):
                messagebox.showerror("Klaida", "Stulpeliai nerasti")
                return pd.DataFrame()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų sąrašo nepavyko rasti")
            return pd.DataFrame()

    def show_books(self):
        self.clear_window()

        self.search_label = tk.Label(self.root, text="Ieškoti knygos:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_books)

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.vsb = tk.Scrollbar(self.frame, orient="vertical")
        self.vsb.pack(side="right", fill="y")

        self.hsb = tk.Scrollbar(self.frame, orient="horizontal")
        self.hsb.pack(side="bottom", fill="x")

        self.book_tree = ttk.Treeview(self.frame, columns=("Pavadinimas", "Autorius", "Metai", "Žanras", "ISBN", "Pastabos", "Knygos statusas"), show="headings", yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.book_tree.pack(fill=tk.BOTH, expand=True)

        self.vsb.config(command=self.book_tree.yview)
        self.hsb.config(command=self.book_tree.xview)

        self.book_tree.heading("Pavadinimas", text="Pavadinimas")
        self.book_tree.heading("Autorius", text="Autorius")
        self.book_tree.heading("Metai", text="Metai")
        self.book_tree.heading("ISBN", text="ISBN")
        self.book_tree.heading("Žanras", text="Žanras")
        self.book_tree.heading("Pastabos", text="Pastabos")
        self.book_tree.heading("Knygos statusas", text="Knygos statusas")

        self.book_tree.column("Pavadinimas", width=200)
        self.book_tree.column("Autorius", width=150)
        self.book_tree.column("Metai", width=100)
        self.book_tree.column("Žanras", width=150)
        self.book_tree.column("ISBN", width=150)
        self.book_tree.column("Pastabos", width=350)
        self.book_tree.column("Knygos statusas", width=100)

        self.book_tree.bind("<Double-1>", self.open_book_profile)

        self.populate_books()

    def populate_books(self):
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for index, row in self.books_df.iterrows():
            self.book_tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos'], row['knygos_statusas']))

    def open_book_profile(self, event):
        if not self.book_tree.selection():
            return
        selected_item = self.book_tree.selection()[0]
        selected_book = self.book_tree.item(selected_item, "values")

        # Išsaugoti pradinę informaciją
        self.selected_book_data = selected_book

        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(700, 100, text="Knygos profilis", font=("Arial", 30), fill="black")

        self.create_profile_field("Pavadinimas:", selected_book[0], 200)
        self.create_profile_field("Autorius:", selected_book[1], 250)
        self.create_profile_field("Metai:", selected_book[2], 300)
        self.create_profile_field("Žanras:", selected_book[3], 350)
        self.create_profile_field("ISBN:", selected_book[4], 400)
        self.create_profile_field("Pastabos:", selected_book[5], 450)
        self.create_profile_field("Knygos statusas:", selected_book[6], 500)

        # Tik ne anoniminiai vartotojai gali redaguoti knygą
        if not self.is_anonymous:
            self.add_button("Išsaugoti pakeitimus", 550, self.save_book_edits)
            self.add_button("Išduoti skaitytojui", 750, self.save_book_edits)
        self.add_button("Atgal į knygų sąrašą", 650, self.show_books)
        self.add_button("Rezervuoti knygą", 850, self.show_books)

    def create_profile_field(self, label_text, value, y_position):
        label = tk.Label(self.root, text=label_text, font=("Arial", 15))
        label.place(x=500, y=y_position)
        entry = tk.Entry(self.root, font=("Arial", 15), width=40)
        entry.place(x=700, y=y_position)
        entry.insert(0, value)
        setattr(self, f"{label_text.strip(':').lower()}_entry", entry)

    def add_button(self, text, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=20, height=2, bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)
        button.place(x=700, y=y_position)

    def save_book_edits(self):
        """Išsaugoti redaguotus knygos duomenis ir išsaugoti redagavimo istoriją."""
        new_data = {
            'Pavadinimas': self.pavadinimas_entry.get(),
            'Autorius': self.autorius_entry.get(),
            'Metai': self.metai_entry.get(),
            'Žanras': self.žanras_entry.get(),
            'ISBN': self.isbn_entry.get(),
            'Pastabos': self.pastabos_entry.get(),
            'Knygos statusas': self.knygos_statusas_entry.get()
        }

        # Rasti knygą ir atnaujinti duomenis CSV faile
        self.books_df.loc[self.books_df['ISBN'] == self.selected_book_data[4], new_data.keys()] = new_data.values()
        self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')

        # Išsaugoti redagavimo istoriją
        self.save_edit_history(self.selected_book_data, new_data)

        messagebox.showinfo("Sėkmė", "Knygos duomenys sėkmingai atnaujinti!")
        self.show_books()

    def save_edit_history(self, old_data, new_data):
        """Išsaugoti redagavimo istoriją CSV faile."""
        changes = []
        for key, new_value in new_data.items():
            old_value = self.selected_book_data[list(new_data.keys()).index(key)]
            if old_value != new_value:
                changes.append({
                    'Pakeista data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Laukas': key,
                    'Sena reikšmė': old_value,
                    'Nauja reikšmė': new_value,
                    'ISBN': self.selected_book_data[4]
                })

        if changes:
            try:
                history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\edit_history.csv")
            except FileNotFoundError:
                history_df = pd.DataFrame(columns=['Pakeista data', 'Laukas', 'Sena reikšmė', 'Nauja reikšmė', 'ISBN'])

            history_df = pd.concat([history_df, pd.DataFrame(changes)], ignore_index=True)
            history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\edit_history.csv", index=False, encoding='utf-8')

    def remove_book(self):
        """Pašalinti knygą pagal ISBN ir perkelti į ištrintų knygų sąrašą."""
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(700, 100, text="Pašalinti knygą", font=("Arial", 30), fill="black")
        self.canvas.create_text(700, 200, text="Įveskite ISBN numerį", font=("Arial", 20), fill="black")
        
        isbn_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=isbn_entry)

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
        
        self.add_button("Ištrinti knygą", 400, delete_book)
        self.add_button("Atgal", 500, self.show_books)

    def filter_books(self, event=None):
        search_term = self.search_entry.get().lower()

        filtered_books = self.books_df[
            (self.books_df['knygos_pavadinimas'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['autorius'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['metai'].astype(str).str.contains(search_term, case=False, na=False)) |
            (self.books_df['zanras'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['ISBN'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['pastabos'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['knygos_statusas'].str.contains(search_term, case=False, na=False))
        ]

        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for index, row in filtered_books.iterrows():
            self.book_tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos'], row['knygos_statusas']))

    def add_book(self):
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

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

        self.canvas.create_text(700, 800, text="Knygos statusas", font=("Arial", 20), fill="black")
        status_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 850, window=status_entry)

        def submit_book():
            author = author_entry.get()
            title = title_entry.get()
            year = year_entry.get()
            isbn = isbn_entry.get()
            genre = genre_entry.get()
            about = about_entry.get()
            status = status_entry.get()

            new_book = {
                'autorius': author,
                'knygos_pavadinimas': title,
                'metai': year,
                'ISBN': isbn,
                'zanras': genre,
                'pastabos': about,
                'knygos_statusas': status
            }

            try:
                books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
                books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
                books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')
                messagebox.showinfo("Sėkmė", f"Knyga '{title}' sėkmingai pridėta!")
            except FileNotFoundError:
                messagebox.showerror("Klaida", "Knygų duomenų failas nerastas.")

        self.add_button("Patvirtinti pridėjimą", 900, submit_book)
        self.add_button("Atgal", 950, self.show_books)

    def search_for_book(self):
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(700, 100, text="Paieškos langas", font=("Arial", 30), fill="black")
        self.canvas.create_text(700, 200, text="Įveskite knygos pavadinimą, autorių, metus arba ISBN", font=("Arial", 20), fill="black")
        search_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=search_entry)

        def search():
            search_query = search_entry.get()
            search_results = self.books_df[
                (self.books_df['knygos_pavadinimas'].str.contains(search_query, case=False, na=False)) |
                (self.books_df['autorius'].str.contains(search_query, case=False, na=False)) |
                (self.books_df['metai'].astype(str).str.contains(search_query, case=False, na=False)) |
                (self.books_df['ISBN'].str.contains(search_query, case=False, na=False))
            ]
            if not search_results.empty:
                for index, row in search_results.iterrows():
                    book_info = f"Knygos pavadinimas: {row['knygos_pavadinimas']}, Rašytojas: {row['autorius']}, ISBN: {row['ISBN']}, Metai: {row['metai']}, Žanras: {row['zanras']}, KNygos statusas: {row['knygos_statusas']}"
                    book_label = tk.Label(self.root, text=book_info)
                    book_label.pack(pady=5)
            else:
                tk.Label(self.root, text="Knygų nerasta.").pack(pady=5)

        self.add_button("Ieškoti", 400, search)
        self.add_button("Atgal", 500, self.show_books)

    def remove_book(self):
        """Pašalinti knygą pagal ISBN ir perkelti į ištrintų knygų sąrašą."""
        self.clear_window()
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(700, 100, text="Pašalinti knygą", font=("Arial", 30), fill="black")
        self.canvas.create_text(700, 200, text="Įveskite ISBN numerį", font=("Arial", 20), fill="black")
        isbn_entry = tk.Entry(self.root)
        self.canvas.create_window(700, 250, window=isbn_entry)

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

        self.add_button("Ištrinti knygą", 400, delete_book)
        self.add_button("Atgal", 500, self.show_books)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Būtina paleisti tkinter pagrindinį langą
if __name__ == "__main__":
    root = tk.Tk()
    app = Books(root, is_anonymous=True)  # Pvz., jei norime paleisti kaip anonimą
    root.mainloop()

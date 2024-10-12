import tkinter as tk
from tkinter import messagebox
import pandas as pd

class Books:
    def __init__(self, root):
        self.root = root
        self.books_df = self.load_books()

    def load_books(self):
        """Knygų sąrašas iš duomenų bazės"""
        try:
            return pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        except FileNotFoundError:
            messagebox.showerror("Error", "Knygų sąrašo nepavyko rasti")
            return pd.DataFrame()

    def find_book(self, search_query):
        """Surasti knygą pagal pavadinimą, autorių arba ISBN."""
        results = self.books_df[
            (self.books_df['knygos_pavadinimas'].str.contains(search_query, case=False, na=False)) |
            (self.books_df['autorius'].str.contains(search_query, case=False, na=False)) |
            (self.books_df['ISBN'].astype(str).str.contains(search_query, case=False, na=False))
        ]
        return results

    def find_reservation(self, reservation_query):
        """Rasti rezervaciją"""
        # Placeholder for reservation search
        pass

    def show_books(self):
        """PArodyti visą knygų sąrašą"""
        books_per_page = 50
        current_page = 0
        total_pages = len(self.books_df) // books_per_page + (1 if len(self.books_df) % books_per_page > 0 else 0)

        def update_books_list(page):
            nonlocal current_page
            current_page = page
            start_idx = current_page * books_per_page
            end_idx = start_idx + books_per_page

            for widget in book_list_frame.winfo_children():
                widget.destroy()

            for index, row in self.books_df.iloc[start_idx:end_idx].iterrows():
                book_info = f" {row['autorius']},  {row['knygos_pavadinimas']},  {row['metai']}, ISBN: {row['ISBN']}"
                tk.Label(book_list_frame, text=book_info).pack()

        # Create book list frame
        book_list_frame = tk.Frame(self.root)
        book_list_frame.pack(pady=20)

        # Pagination buttons
        def next_page():
            nonlocal current_page
            if current_page < total_pages - 1:
                update_books_list(current_page + 1)

        def previous_page():
            nonlocal current_page
            if current_page > 0:
                update_books_list(current_page - 1)

        tk.Button(self.root, text="Ankstesnis", command=previous_page).pack(side="left", padx=10)
        tk.Button(self.root, text="Kitas", command=next_page).pack(side="right", padx=10)

        update_books_list(0)

    def show_history(self, reader_id):
        """PArodyti knygos skaitymo istoriją"""
        pass

    def show_book_profile(self, book_row):
        """Detalus knygos profilis"""
        self.clear_window()

        tk.Label(self.root, text=f"Book: {book_row['knygos_pavadinimas']}", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.root, text=f"Author: {book_row['autorius']}").pack(pady=5)
        tk.Label(self.root, text=f"Year: {book_row['metai']}").pack(pady=5)
        tk.Label(self.root, text=f"ISBN: {book_row['ISBN']}").pack(pady=5)
        tk.Label(self.root, text=f"Genre: {book_row['zanras']}").pack(pady=5)
        tk.Label(self.root, text=f"Description: {book_row['pastabos']}").pack(pady=10)

        tk.Button(self.root, text="Back", command=lambda: self.show_books()).pack(pady=10)

def create_widgets(self):
        # Paieškos laukas
        self.search_label = tk.Label(self.root, text="Ieškoti knygos:")
        self.search_label.pack(pady=5)
        
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_books)  # Knygų filtravimas
        
        # Frame su slankikliais
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Vertikalus slankiklis
        self.vsb = tk.Scrollbar(self.frame, orient="vertical")
        self.vsb.pack(side="right", fill="y")
        
        # Horizontalus slankiklis
        self.hsb = tk.Scrollbar(self.frame, orient="horizontal")
        self.hsb.pack(side="bottom", fill="x")

        # Knygų sąrašas naudojant Treeview
        self.book_tree = ttk.Treeview(self.frame, columns=("Pavadinimas", "Autorius", "Metai", "Žanras"), show="headings", yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.book_tree.pack(fill=tk.BOTH, expand=True)

        self.vsb.config(command=self.book_tree.yview)
        self.hsb.config(command=self.book_tree.xview)

        # Knygų sąrašo stulpeliai
        self.book_tree.heading("Pavadinimas", text="Pavadinimas")
        self.book_tree.heading("Autorius", text="Autorius")
        self.book_tree.heading("Metai", text="Metai")
        self.book_tree.heading("Žanras", text="Žanras")

        self.book_tree.column("Pavadinimas", width=200)
        self.book_tree.column("Autorius", width=150)
        self.book_tree.column("Metai", width=100)
        self.book_tree.column("Žanras", width=150)

        # Knygos profilio peržiūra
        self.book_tree.bind("<Double-1>", self.open_book_profile)

        # Knygų sąrašo užpildymas
        self.populate_books()

    def load_books_from_csv(self, file_path):
        books = []
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    books.append({
                        "pavadinimas": row['pavadinimas'],
                        "autorius": row['autorius'],
                        "metai": int(row['metai']),
                        "zanras": row['zanras']
                    })
        except FileNotFoundError:
            messagebox.showerror("Klaida", f"Nepavyko rasti failo: {file_path}")
        return books

    def populate_books(self):
        # Išvalyti sąrašą
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        # Įrašyti knygas
        for book in self.books:
            self.book_tree.insert("", "end", values=(book["pavadinimas"], book["autorius"], book["metai"], book["zanras"]))

    def filter_books(self, event=None):
        search_term = self.search_entry.get().lower()

        filtered_books = [book for book in self.books if
                          search_term in book["pavadinimas"].lower() or
                          search_term in book["autorius"].lower() or
                          search_term in str(book["metai"]).lower() or
                          search_term in book["zanras"].lower()]
        
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for book in filtered_books:
            self.book_tree.insert("", "end", values=(book["pavadinimas"], book["autorius"], book["metai"], book["zanras"]))

    def open_book_profile(self, event):
        selected_item = self.book_tree.selection()[0]
        selected_book = self.book_tree.item(selected_item, "values")
        
        # Čia pateikiame išsamią knygos informaciją
        messagebox.showinfo("Knygos profilis", f"Pavadinimas: {selected_book[0]}\nAutorius: {selected_book[1]}\nMetai: {selected_book[2]}\nŽanras: {selected_book[3]}")



    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime

class Books:
    def __init__(self, root, is_anonymous=False):
        self.root = root
        self.is_anonymous = is_anonymous  # Anonimiškumo flag'as
        self.books_df = self.load_books()
        self.readers_df = self.load_readers()

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

    def load_readers(self):
        try:
            df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            required_columns = {'vardas', 'pavarde', 'email', 'telefonas', 'skaitytojo_kortele'}
            if not required_columns.issubset(df.columns):
                messagebox.showerror("Klaida", "Skaitytojų stulpeliai nerasti")
                return pd.DataFrame()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Skaitytojų sąrašo nepavyko rasti")
            return pd.DataFrame()

    def show_books(self):
        # Sukurti naują langą
        new_window = tk.Toplevel(self.root)
        new_window.title("Knygų sąrašas")

        # Kiti komponentai kuriami naujame lange
        search_label = tk.Label(new_window, text="Ieškoti knygos:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_books(search_entry, new_window))

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        book_tree = ttk.Treeview(frame, columns=("Pavadinimas", "Autorius", "Metai", "Žanras", "ISBN", "Pastabos", "Knygos statusas"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        book_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=book_tree.yview)
        hsb.config(command=book_tree.xview)

        book_tree.heading("Pavadinimas", text="Pavadinimas")
        book_tree.heading("Autorius", text="Autorius")
        book_tree.heading("Metai", text="Metai")
        book_tree.heading("ISBN", text="ISBN")
        book_tree.heading("Žanras", text="Žanras")
        book_tree.heading("Pastabos", text="Pastabos")
        book_tree.heading("Knygos_statusas", text="Knygos statusas")

        book_tree.column("Pavadinimas", width=200)
        book_tree.column("Autorius", width=150)
        book_tree.column("Metai", width=100)
        book_tree.column("Žanras", width=150)
        book_tree.column("ISBN", width=150)
        book_tree.column("Pastabos", width=350)
        book_tree.column("Knygos_statusas", width=100)

        book_tree.bind("<Double-1>", self.open_book_profile)

        self.populate_books(book_tree)

    def populate_books(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        for index, row in self.books_df.iterrows():
            tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos'], row['knygos_statusas']))

    def filter_books(self, search_entry, window):
        search_term = search_entry.get().lower()
        filtered_books = self.books_df[
            (self.books_df['knygos_pavadinimas'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['autorius'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['metai'].astype(str).str.contains(search_term, case=False, na=False)) |
            (self.books_df['zanras'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['ISBN'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['pastabos'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['knygos_statusas'].str.contains(search_term, case=False, na=False))
        ]

        tree = window.winfo_children()[1].winfo_children()[2]  # Gauti Treeview iš naujo lango
        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_books.iterrows():
            tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos'], row['knygos_statusas']))

    def open_book_profile(self, event):
        selected_item = event.widget.selection()[0]
        selected_book = event.widget.item(selected_item, "values")

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Knygos profilis: {selected_book[0]}")

        self.create_profile_field(new_window, "Pavadinimas:", selected_book[0], 200)
        self.create_profile_field(new_window, "Autorius:", selected_book[1], 250)
        self.create_profile_field(new_window, "Metai:", selected_book[2], 300)
        self.create_profile_field(new_window, "Žanras:", selected_book[3], 350)
        self.create_profile_field(new_window, "ISBN:", selected_book[4], 400)
        self.create_profile_field(new_window, "Pastabos:", selected_book[5], 450)
        self.create_profile_field(new_window, "Knygos statusas:", selected_book[6], 500)

        # Tik ne anonimiški vartotojai gali redaguoti knygą
        if not self.is_anonymous:
            self.add_button(new_window, "Išsaugoti pakeitimus", 550, self.save_book_edits)
        self.add_button(new_window, "Uždaryti", 650, new_window.destroy)

    def create_profile_field(self, window, label_text, value, y_position):
        label = tk.Label(window, text=label_text, font=("Arial", 15))
        label.place(x=100, y=y_position)
        entry = tk.Entry(window, font=("Arial", 15), width=40)
        entry.place(x=250, y=y_position)
        entry.insert(0, value)
        setattr(self, f"{label_text.strip(':').lower()}_entry", entry)

    def add_button(self, window, text, y_position, command):
        button = tk.Button(window, text=text, font=("Arial", 15), width=20, height=2, bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)
        button.place(x=250, y=y_position)

    def save_book_edits(self):
        # Implementuokite funkcionalumą išsaugoti knygos redagavimus, jei reikia
        pass

    def add_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pridėti naują knygą")

        self.create_profile_field(new_window, "Pavadinimas:", "", 100)
        self.create_profile_field(new_window, "Autorius:", "", 150)
        self.create_profile_field(new_window, "Metai:", "", 200)
        self.create_profile_field(new_window, "Zanras:", "", 250)
        self.create_profile_field(new_window, "ISBN:", "", 300)
        self.create_profile_field(new_window, "Pastabos:", "", 350)
        self.create_profile_field(new_window, "Knygos_statusas:", "", 400)

        self.add_button(new_window, "Pridėti knygą", 500, lambda: self.submit_book(new_window))

    def submit_book(self, window):
        new_book = {
            'autorius': self.autorius_entry.get(),
            'knygos_pavadinimas': self.pavadinimas_entry.get(),
            'metai': self.metai_entry.get(),
            'ISBN': self.isbn_entry.get(),
            'zanras': self.zanras_entry.get(),
            'pastabos': self.pastabos_entry.get(),
            'knygos_statusas': self.knygos_statusas_entry.get()
        }

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
            books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')
            messagebox.showinfo("Knyga pridėta sėkmingai", f"Knyga {new_book['knygos_pavadinimas']} sėkmingai pridėta!")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų failas nerastas.")
        window.destroy()

    def remove_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pašalinti knygą")

        # Įveskite ISBN laukelį su tinkama y_position
        self.create_profile_field(new_window, "Įveskite ISBN:", "", 100)
        
        # Pridedame mygtuką "Pašalinti knygą"
        self.add_button(new_window, "Rasti knygą", 200, lambda: self.show_book_before_delete(new_window))

    def show_book_before_delete(self, window):
        isbn = self.isbn_entry.get()

        if not isbn.isnumeric():
            messagebox.showerror("Klaida", "ISBN numerį sudaro tik skaičiai.")
            return

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų bazė nerasta")
            return

        # Surandame knygą pagal ISBN
        book_to_delete = books_df[books_df["ISBN"] == isbn]

        if book_to_delete.empty:
            messagebox.showwarning("Įspėjimas", f"Knyga su ISBN {isbn} nerasta.")
        else:
            # Sukuriamas naujas langas, kuriame parodoma knygos informacija
            book_data = book_to_delete.iloc[0]
            confirm_window = tk.Toplevel(window)
            confirm_window.title(f"Ištrinti knygą: {book_data['knygos_pavadinimas']}?")

            # Rodome knygos informaciją
            tk.Label(confirm_window, text=f"Pavadinimas: {book_data['knygos_pavadinimas']}", font=("Arial", 12)).pack(pady=10)
            tk.Label(confirm_window, text=f"Autorius: {book_data['autorius']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"Metai: {book_data['metai']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"Žanras: {book_data['zanras']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"ISBN: {book_data['ISBN']}", font=("Arial", 12)).pack(pady=5)

            # Patvirtinimo ir atšaukimo mygtukai
            tk.Button(confirm_window, text="Patvirtinti trynimą", command=lambda: self.confirm_delete(book_data, books_df, confirm_window)).pack(pady=10)
            tk.Button(confirm_window, text="Atšaukti", command=confirm_window.destroy).pack(pady=10)

    def confirm_delete(self, book_data, books_df, confirm_window):
        # Šaliname knygą iš duomenų bazės
        books_df_filtered = books_df[books_df["ISBN"] != book_data['ISBN']]

        # Saugojame atnaujintą sąrašą
        books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding="UTF-8")

        # Perkeliam knygą į ištrintų knygų sąrašą
        try:
            deleted_books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\deleted_books_db.csv")
        except FileNotFoundError:
            deleted_books_df = pd.DataFrame(columns=books_df.columns)

        deleted_books_df = pd.concat([deleted_books_df, pd.DataFrame([book_data])], ignore_index=True)
        deleted_books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\deleted_books_db.csv", index=False, encoding="UTF-8")

        messagebox.showinfo("Sėkmė", f"Knyga {book_data['knygos_pavadinimas']} su ISBN {book_data['ISBN']} sėkmingai ištrinta.")
        
        # Uždaryti patvirtinimo langą
        confirm_window.destroy()

    def search_for_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Paieška")

        self.create_profile_field(new_window, "Įveskite paieškos tekstą:", "", 100)
        self.add_button(new_window, "Ieškoti", 200, lambda: self.filter_books(self.isbn_entry, new_window))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Būtina paleisti tkinter pagrindinį langą
if __name__ == "__main__":
    root = tk.Tk()
    app = Books(root, is_anonymous=True)  # Pvz., jei norime paleisti kaip anonimą
    root.mainloop()

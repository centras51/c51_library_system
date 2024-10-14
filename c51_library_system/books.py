import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

class Books:
    def __init__(self, root):
        self.root = root
        self.books_df = self.load_books()
        self.show_books()

    def load_books(self):
        try:
            df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            required_columns = {'knygos_pavadinimas', 'autorius', 'metai', 'ISBN', 'zanras', 'pastabos'}
            if not required_columns.issubset(df.columns):
                messagebox.showerror("Klaida", "Stulpeliai nerasti")
                return pd.DataFrame()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų sąrašo nepavyko rasti")
            return pd.DataFrame()

    def show_books(self):
        # Paieškos laukas
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

        self.book_tree = ttk.Treeview(self.frame, columns=("Pavadinimas", "Autorius", "Metai", "Žanras", "ISBN", "Pastabos"), show="headings", yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.book_tree.pack(fill=tk.BOTH, expand=True)

        self.vsb.config(command=self.book_tree.yview)
        self.hsb.config(command=self.book_tree.xview)

        # Knygų sąrašo stulpeliai
        self.book_tree.heading("Pavadinimas", text="Pavadinimas")
        self.book_tree.heading("Autorius", text="Autorius")
        self.book_tree.heading("Metai", text="Metai")
        self.book_tree.heading("ISBN", text="ISBN")
        self.book_tree.heading("Žanras", text="Žanras")
        self.book_tree.heading("Pastabos", text="Pastabos")

        self.book_tree.column("Pavadinimas", width=200)
        self.book_tree.column("Autorius", width=150)
        self.book_tree.column("Metai", width=100)
        self.book_tree.column("Žanras", width=150)
        self.book_tree.column("ISBN", width=150)
        self.book_tree.column("Pastabos", width=350)

        # Knygos profilio peržiūra
        self.book_tree.bind("<Double-1>", self.open_book_profile)

        # Knygų sąrašo užpildymas
        self.populate_books()

    def populate_books(self):
        # Išvalyti sąrašą
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        # Įrašyti knygas
        for index, row in self.books_df.iterrows():
            self.book_tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos']))

    def filter_books(self, event=None):
        search_term = self.search_entry.get().lower()

        filtered_books = self.books_df[
            (self.books_df['knygos_pavadinimas'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['autorius'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['metai'].astype(str).str.contains(search_term, case=False, na=False)) |
            (self.books_df['zanras'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['ISBN'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['pastabos'].str.contains(search_term, case=False, na=False))
        ]

        # Išvalyti ir užpildyti filtruotas knygas
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for index, row in filtered_books.iterrows():
            self.book_tree.insert("", "end", values=(row['knygos_pavadinimas'], row['autorius'], row['metai'], row['zanras'], row['ISBN'], row['pastabos']))

    def open_book_profile(self, event):
        if not self.book_tree.selection():
            return
        selected_item = self.book_tree.selection()[0]
        selected_book = self.book_tree.item(selected_item, "values")
        
        # Išvalyti langą, kad parodytume knygos profilį
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(700, 100, text="Knygos profilis", font=("Arial", 30), fill="black")

        # Knygos profilio informacijos laukeliai
        self.create_profile_field("Pavadinimas:", selected_book[0], 200)
        self.create_profile_field("Autorius:", selected_book[1], 250)
        self.create_profile_field("Metai:", selected_book[2], 300)
        self.create_profile_field("Žanras:", selected_book[3], 350)
        self.create_profile_field("ISBN:", selected_book[4], 400)
        self.create_profile_field("Pastabos:", selected_book[5], 450)

        # Mygtukas grįžti į knygų sąrašą
        self.add_button("Atgal į knygų sąrašą", 600, self.show_books)

    def create_profile_field(self, label_text, value, y_position):
        """Sukurti profilio lauką su pavadinimu ir reikšme"""
        label = tk.Label(self.root, text=label_text, font=("Arial", 15))
        label.place(x=500, y=y_position)
        entry = tk.Entry(self.root, font=("Arial", 15), width=40)
        entry.place(x=700, y=y_position)
        entry.insert(0, value)
        entry.config(state='readonly')

    def add_button(self, text, y_position, command):
        """Sukurti mygtuką su efektais"""
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=20, height=2,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)
        button.place(x=700, y=y_position)

    def clear_window(self):
        """Išvalyti langą prieš peržiūrint naują turinį"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Books(root)
    root.mainloop()

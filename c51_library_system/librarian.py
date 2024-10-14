import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
from books import Books
from readerregistration import ReaderRegistration


class Librarian:
    def __init__(self, root, librarian_info):
        self.root = root
        self.librarian_info = librarian_info
        self.books_instance = Books(self.root)
        self.readerregistration_instance = ReaderRegistration(self.root)
        self.button_width = 30  
        self.button_height = 3  

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.add_librarian_info()

        self.show_menu()

    def add_librarian_info(self):
        """Prideda bibliotekininko informaciją apačioje."""
        librarian_info_text = f"Bibliotekininkas: {self.librarian_info[0]} {self.librarian_info[1]}, Tel: {self.librarian_info[2]}, El. paštas: {self.librarian_info[3]}"
        librarian_label = tk.Label(self.root, text=librarian_info_text, font=("Arial", 12), bg="lightgray", fg="black")
        
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
        self.add_button("Išduoti knygą", 250, 500, self.lend_book)  
        self.add_button("Pašalinti knygą", 250, 650, self.books_instance.remove_book)  

        self.add_button("Skaitytojų sąrašas", 750, 200, self.reader_list)  
        self.add_button("Surasti skaitytoją", 750, 350, self.search_reader)  
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
        # Sukuriame naują langą skaitytojų sąrašui
        new_window = tk.Toplevel(self.root)
        new_window.title("Skaitytojų sąrašas")

        # Paieškos laukelis
        search_label = tk.Label(new_window, text="Ieškoti skaitytojo:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_readers(search_entry))

        # Sukuriame rėmelį lentelės rodymui
        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        # Lentelė skaitytojams rodyti
        self.reader_tree = ttk.Treeview(frame, columns=("Vardas", "Pavardė", "El. paštas", "Telefonas", "Skaitytojo kortelė", "Username"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.reader_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=self.reader_tree.yview)
        hsb.config(command=self.reader_tree.xview)

        # Sukuriame lentelės antraštes
        self.reader_tree.heading("Vardas", text="Vardas")
        self.reader_tree.heading("Pavardė", text="Pavardė")
        self.reader_tree.heading("El. paštas", text="El. paštas")
        self.reader_tree.heading("Telefonas", text="Telefonas")
        self.reader_tree.heading("Skaitytojo kortelė", text="Skaitytojo kortelė")
        self.reader_tree.heading("Username", text="Username")

        self.reader_tree.column("Vardas", width=150)
        self.reader_tree.column("Pavardė", width=150)
        self.reader_tree.column("El. paštas", width=200)
        self.reader_tree.column("Telefonas", width=150)
        self.reader_tree.column("Skaitytojo kortelė", width=150)
        self.reader_tree.column("Username", width=150)

        # Užpildome lentelę skaitytojais
        self.populate_readers(self.reader_tree)

    def populate_readers(self, tree):
        # Įkrauname skaitytojų duomenų failą
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

        # Konvertuojame reikalingus stulpelius į tekstą
        readers_df['telefonas'] = readers_df['telefonas'].astype(str)
        readers_df['skaitytojo_kortele'] = readers_df['skaitytojo_kortele'].astype(str)
        readers_df['username'] = readers_df['username'].astype(str)

        for item in tree.get_children():
            tree.delete(item)

        for index, row in readers_df.iterrows():
            tree.insert("", "end", values=(
                row['vardas'], 
                row['pavarde'], 
                row['email'], 
                row['telefonas'], 
                row['skaitytojo_kortele'], 
                row['username']
            ))


    def search_reader(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Ieškoti skaitytojo")

        tk.Label(new_window, text="Įveskite skaitytojo kortelės nr, vardą arba pavardę:").pack(pady=10)
        self.search_entry = tk.Entry(new_window)
        self.search_entry.pack(pady=5)

        tk.Button(new_window, text="Ieškoti", command=lambda: self.filter_readers(self.search_entry)).pack(pady=10)

    def filter_readers(self, search_entry):
        search_term = search_entry.get().lower()
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

        # Konvertuojame visus reikalingus stulpelius į tekstą, įskaitant telefoną ir kortelę
        readers_df['vardas'] = readers_df['vardas'].astype(str)
        readers_df['pavarde'] = readers_df['pavarde'].astype(str)
        readers_df['email'] = readers_df['email'].astype(str)
        readers_df['telefonas'] = readers_df['telefonas'].astype(str)
        readers_df['skaitytojo_kortele'] = readers_df['skaitytojo_kortele'].astype(str)

        # Filtruojame skaitytojus pagal paieškos terminą
        filtered_readers = readers_df[
            (readers_df['vardas'].str.contains(search_term, case=False, na=False)) |
            (readers_df['pavarde'].str.contains(search_term, case=False, na=False)) |
            (readers_df['email'].str.contains(search_term, case=False, na=False)) |
            (readers_df['telefonas'].str.contains(search_term, case=False, na=False)) |
            (readers_df['skaitytojo_kortele'].str.contains(search_term, case=False, na=False))
        ]

        # Atnaujiname TreeView su filtruotais duomenimis
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)

        for index, row in filtered_readers.iterrows():
            self.reader_tree.insert("", "end", values=(
                row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['skaitytojo_kortele']
            ))

    def remove_reader(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pašalinti skaitytoją")

        # Laukas įvesti skaitytojo kortelės numerį, vardą arba pavardę
        tk.Label(new_window, text="Įveskite kortelės numerį, vardą arba pavardę:").pack(pady=10)
        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)

        def search_reader():
            search_term = search_entry.get().strip().lower()
            if not search_term:
                messagebox.showerror("Klaida", "Įveskite kortelės numerį, vardą arba pavardę")
                return
            
            readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

            # Ieškoti skaitytojo pagal kortelės numerį, vardą arba pavardę
            filtered_readers = readers_df[
                (readers_df['skaitytojo_kortele'].str.contains(search_term, case=False, na=False)) |
                (readers_df['vardas'].str.contains(search_term, case=False, na=False)) |
                (readers_df['skaitytojo_kortele'].str.contains(search_term, case=False, na=False)) |
                (readers_df['pavarde'].str.contains(search_term, case=False, na=False))
            ]

            if filtered_readers.empty:
                messagebox.showwarning("Įspėjimas", f"Skaitytojas su paieškos terminu '{search_term}' nerastas")
            else:
                if len(filtered_readers) > 1:
                    self.display_multiple_readers(new_window, filtered_readers)
                else:
                    reader_data = filtered_readers.iloc[0]
                    self.display_reader_data(new_window, reader_data, readers_df)

        tk.Button(new_window, text="Ieškoti", command=search_reader).pack(pady=10)

    def display_reader_data(self, parent_window, reader_data, readers_df):
        """Funkcija rodanti skaitytojo duomenis prieš ištrynimą ir reikalaujanti slaptažodžio patvirtinimo."""
        reader_info = f"Vardas: {reader_data['vardas']}\nPavardė: {reader_data['pavarde']}\nEl. paštas: {reader_data['email']}\nTelefonas: {reader_data['telefonas']}\nSkaitytojo kortelė: {reader_data['skaitytojo_kortele']}\nUsername: {reader_data['username']}"
        tk.Label(parent_window, text=reader_info, justify="left").pack(pady=10)

        tk.Label(parent_window, text="Įveskite savo slaptažodį, kad patvirtintumėte trynimą:").pack(pady=10)
        password_entry = tk.Entry(parent_window, show="*")
        password_entry.pack(pady=5)

        def confirm_delete():
            entered_password = password_entry.get()
            correct_password = self.librarian_info[-1]

            if entered_password == correct_password:
                readers_df_filtered = readers_df[readers_df["skaitytojo_kortele"] != reader_data['skaitytojo_kortele']]
                readers_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding="utf-8")
                messagebox.showinfo("Sėkmė", "Skaitytojas sėkmingai ištrintas!")
                parent_window.destroy()
            else:
                messagebox.showerror("Klaida", "Neteisingas slaptažodis")

        tk.Button(parent_window, text="Patvirtinti trynimą", command=confirm_delete).pack(pady=10)

    def display_multiple_readers(self, parent_window, filtered_readers):
        """Funkcija rodanti kelis rastus skaitytojus pasirinkimui."""
        tk.Label(parent_window, text="Pasirinkite skaitytoją:").pack(pady=10)

        for index, reader in filtered_readers.iterrows():
            reader_info = f"{reader['vardas']} {reader['pavarde']}, Kortelė: {reader['skaitytojo_kortele']}"
            tk.Button(parent_window, text=reader_info, command=lambda r=reader: self.display_reader_data(parent_window, r, filtered_readers)).pack(pady=5)

    def show_librarians(self):
        # Sukuriame naują langą bibliotekininkų sąrašui
        new_window = tk.Toplevel(self.root)
        new_window.title("Bibliotekininkų sąrašas")

        # Paieškos laukelis
        search_label = tk.Label(new_window, text="Ieškoti bibliotekininko:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_librarians(search_entry, new_window))

        # Sukuriame rėmelį lentelės rodymui
        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        # Lentelė bibliotekininkams rodyti
        librarian_tree = ttk.Treeview(frame, columns=("Vardas", "Pavardė", "El. paštas", "Telefonas", "Username"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        librarian_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=librarian_tree.yview)
        hsb.config(command=librarian_tree.xview)

        # Sukuriame lentelės antraštes
        librarian_tree.heading("Vardas", text="Vardas")
        librarian_tree.heading("Pavardė", text="Pavardė")
        librarian_tree.heading("El. paštas", text="El. paštas")
        librarian_tree.heading("Telefonas", text="Telefonas")
        librarian_tree.heading("Username", text="Username")

        librarian_tree.column("Vardas", width=150)
        librarian_tree.column("Pavardė", width=150)
        librarian_tree.column("El. paštas", width=200)
        librarian_tree.column("Telefonas", width=150)
        librarian_tree.column("Username", width=150)

        # Užpildome lentelę bibliotekininkais
        self.populate_librarians(librarian_tree)

    def populate_librarians(self, tree):
        # Įkrauname bibliotekininkų duomenų failą
        librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
        
        for item in tree.get_children():
            tree.delete(item)

        for index, row in librarians_df.iterrows():
            tree.insert("", "end", values=(row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['username']))

    def filter_librarians(self, search_entry, window):
        search_term = search_entry.get().lower()
        librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")

        # Konvertuojame visus reikalingus stulpelius į tekstą
        librarians_df['vardas'] = librarians_df['vardas'].astype(str)
        librarians_df['pavarde'] = librarians_df['pavarde'].astype(str)
        librarians_df['email'] = librarians_df['email'].astype(str)
        librarians_df['telefonas'] = librarians_df['telefonas'].astype(str)
        librarians_df['username'] = librarians_df['username'].astype(str)

        # Filtruojame bibliotekininkus pagal paieškos terminą
        filtered_librarians = librarians_df[
            (librarians_df['vardas'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['pavarde'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['email'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['telefonas'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['username'].str.contains(search_term, case=False, na=False))
        ]

        tree = window.winfo_children()[1].winfo_children()[2]  # Gauti Treeview iš naujo lango
        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_librarians.iterrows():
            tree.insert("", "end", values=(row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['username']))
            
            
    
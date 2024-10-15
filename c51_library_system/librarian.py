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

        self.show_menu()  # Pirmiausia rodomas meniu

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

        self.canvas.create_text(250, 50, text=f"Bibliotekininkas: {self.librarian_info[0]} {self.librarian_info[1]}, Tel: {self.librarian_info[2]}, El. paštas: {self.librarian_info[3]}", font=("Arial", 15, "bold"), fill="green", anchor="nw")

        self.add_button("Peržiūrėti knygas", 250, 200, self.books_instance.show_books)  
        self.add_button("Pridėti knygą", 250, 350, self.books_instance.add_book)  
        self.add_button("Knygų statistika", 250, 500, self.books_instance.show_statistics)  

        self.add_button("Skaitytojų sąrašas", 750, 200, self.reader_list)  
        self.add_button("Pridėti skaitytoją", 750, 350, self.readerregistration_instance.register)  
        self.add_button("Pašalinti knygą", 750, 500, self.books_instance.remove_book)  

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
        
        # Ignoruojame slaptažodžio stulpelį
        for item in tree.get_children():
            tree.delete(item)

        # Pridėti tik reikiamus stulpelius į TreeView
        for index, row in readers_df.iterrows():
            tree.insert("", "end", values=(
                row['vardas'], 
                row['pavarde'], 
                row['email'], 
                row['telefonas'], 
                row['skaitytojo_kortele'], 
                row['username']
            ))

        tree.bind("<Double-1>", lambda event: self.open_reader_profile(event, tree))

    def open_reader_profile(self, event, tree):
        # Paimkite dabartinį pasirinktą elementą
        item_id = tree.focus()  
        selected_item = tree.item(item_id)['values']

        if len(selected_item) < 6:
            messagebox.showerror("Klaida", "Nepavyko įkelti visų skaitytojo duomenų. Trūksta duomenų.")
            return

        # Sukuriame struktūrą su skaitytojo duomenimis (be slaptažodžio)
        reader_data = {
            "vardas": selected_item[0],
            "pavarde": selected_item[1],
            "email": selected_item[2],
            "telefonas": selected_item[3],
            "skaitytojo_kortele": selected_item[4],
            "username": selected_item[5]
        }

        self.show_reader_profile(reader_data)

    def get_books_list(self):
        # Funkcija, kuri grąžina knygų sąrašą
        books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        return books_df['knygos_pavadinimas'].tolist()

    def show_reader_profile(self, reader_data):
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"Skaitytojo profilis: {reader_data['vardas']} {reader_data['pavarde']}")

        # Redaguojamos įvesties laukeliai
        tk.Label(profile_window, text="Vardas:").pack(pady=5)
        vardas_entry = tk.Entry(profile_window)
        vardas_entry.insert(0, reader_data['vardas'])
        vardas_entry.pack(pady=5)

        tk.Label(profile_window, text="Pavardė:").pack(pady=5)
        pavarde_entry = tk.Entry(profile_window)
        pavarde_entry.insert(0, reader_data['pavarde'])
        pavarde_entry.pack(pady=5)

        tk.Label(profile_window, text="El. paštas:").pack(pady=5)
        email_entry = tk.Entry(profile_window)
        email_entry.insert(0, reader_data['email'])
        email_entry.pack(pady=5)

        tk.Label(profile_window, text="Telefonas:").pack(pady=5)
        telefonas_entry = tk.Entry(profile_window)
        telefonas_entry.insert(0, reader_data['telefonas'])
        telefonas_entry.pack(pady=5)

        # Knygų priskyrimas (dropdown)
        tk.Label(profile_window, text="Priskirti knygą:").pack(pady=5)
        book_list = self.get_books_list()  # Gauti knygų sąrašą
        book_combobox = ttk.Combobox(profile_window, values=book_list)
        book_combobox.pack(pady=5)

        tk.Button(profile_window, text="Priskirti knygą", command=lambda: self.assign_book_to_reader(reader_data['skaitytojo_kortele'], book_combobox.get())).pack(pady=10)

        # Skaitymo istorija
        tk.Label(profile_window, text="Skaitymo istorija:").pack(pady=5)
        self.show_reading_history(profile_window, reader_data['skaitytojo_kortele'])

        # Išsaugoti pakeitimus
        tk.Button(profile_window, text="Išsaugoti pakeitimus", command=lambda: self.save_reader_changes(
            reader_data['skaitytojo_kortele'], vardas_entry.get(), pavarde_entry.get(), email_entry.get(), telefonas_entry.get(), profile_window)).pack(pady=10)

        # Mygtukas skaitytojo trynimui
        tk.Button(profile_window, text="Ištrinti skaitytoją", command=lambda: self.delete_reader(reader_data['skaitytojo_kortele'], profile_window)).pack(pady=10)

    def show_reading_history(self, parent, reader_card_number):
        # Skaitymo istorijos rodymas
        reading_history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")
        reader_history = reading_history_df[reading_history_df['skaitytojo_kortele'] == reader_card_number]

        for index, row in reader_history.iterrows():
            tk.Label(parent, text=f"Knyga: {row['knygos_pavadinimas']}, Knygos paėmimo data: {row['knygos_paemimo_data']}, Knygos grąžinimo data: {row['knygos_grazinimo_data']}").pack(pady=2)

    def assign_book_to_reader(self, reader_card_number, book_name):
        # Priskirti knygą skaitytojui
        if book_name:
            # Įkrauname esamą skaitytojų, knygų ir skaitymo istorijos duomenų bazę
            readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")

            # Paverčiame skaitytojo kortelės numerį į tekstą ir pašaliname bet kokius tarpelius
            reader_card_number = str(reader_card_number).strip()

            # Ieškome skaitytojo pagal kortelės numerį
            reader_info = readers_df[readers_df['skaitytojo_kortele'].astype(str).str.strip() == reader_card_number]
            
            if reader_info.empty:
                messagebox.showerror("Klaida", f"Nerasta skaitytojo su kortelės numeriu: {reader_card_number}")
                return

            reader_info = reader_info.iloc[0]  # Paimame pirmą rastą įrašą

            # Patikriname, kiek knygų šis skaitytojas turi šiuo metu
            active_loans = history_df[(history_df['skaitytojo_kortele'] == reader_card_number) &
                                    (pd.to_datetime(history_df['knygos_grazinimo_data']) > pd.Timestamp.now())]

            if len(active_loans) >= 5:
                messagebox.showerror("DĖMESIO", "Jūs negalite paimti daugiau nei 5 knygas vienu metu.")
                return

            # Patikriname, ar yra vėluojamų knygų
            overdue_loans = history_df[(history_df['skaitytojo_kortele'] == reader_card_number) &
                                    (pd.to_datetime(history_df['knygos_grazinimo_data']) < pd.Timestamp.now())]

            if not overdue_loans.empty:
                messagebox.showerror("DĖMESIO", "Jūs negalite paimti naujų knygų, kol turite vėluojamų knygų.")
                return

            # Ieškome knygos pagal pavadinimą
            book_info = books_df[books_df['knygos_pavadinimas'] == book_name]

            if book_info.empty:
                messagebox.showerror("Klaida", f"Nerasta knyga su pavadinimu: {book_name}")
                return

            book_info = book_info.iloc[0]  # Paimame pirmą rastą įrašą

            # Patikriname, ar knyga jau yra užimta
            last_loan_entry = history_df[history_df['knygos_pavadinimas'] == book_name].sort_values('knygos_grazinimo_data', ascending=False).head(1)

            if not last_loan_entry.empty and pd.to_datetime(last_loan_entry['knygos_grazinimo_data'].values[0]) > pd.Timestamp.now():
                messagebox.showerror("Klaida", f"Knyga '{book_name}' jau yra užimta iki {last_loan_entry['knygos_grazinimo_data'].values[0]}.")
                return

            # Sukuriame naują įrašą skaitymo istorijoje
            grazinimo_data = pd.Timestamp.now().date() + pd.Timedelta(days=14)  # Priskiriame 14 dienų terminą
            new_entry = pd.DataFrame({
                "vardas": [reader_info['vardas']],
                "pavarde": [reader_info['pavarde']],
                "skaitytojo_kortele": [reader_card_number],
                "autorius": [book_info['autorius']],
                "knygos_pavadinimas": [book_name],
                "ISBN": [book_info['ISBN']],
                "knygos_paemimo_data": [pd.Timestamp.now().date()],
                "knygos_grazinimo_data": [grazinimo_data],
                                        })

            # Pridedame naują įrašą į skaitymo istoriją
            history_df = pd.concat([history_df, new_entry], ignore_index=True)

            # Atnaujiname knygos statusą į "užimta iki" su konkrečia grąžinimo data iš skaitymo istorijos
            books_df.loc[books_df['knygos_pavadinimas'] == book_name, 'statusas'] = f"užimta iki {grazinimo_data}"

            # Išsaugome atnaujintą istoriją ir knygų duomenis CSV failuose
            history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv", index=False)
            books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False)

            # Pranešimas apie sėkmingą priskyrimą
            messagebox.showinfo("Sėkmė", f"Knyga '{book_name}' sėkmingai priskirta skaitytojui {reader_info['vardas']} {reader_info['pavarde']}. Knyga užimta iki {grazinimo_data}.")
        else:
            messagebox.showerror("Klaida", "Pasirinkite knygą priskyrimui.")


    def save_reader_changes(self, reader_card_number, vardas, pavarde, email, telefonas, window):
        # Išsaugoti pakeitimus skaitytojo duomenyse
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        readers_df.loc[readers_df['skaitytojo_kortele'] == reader_card_number, ['vardas', 'pavarde', 'email', 'telefonas']] = [vardas, pavarde, email, telefonas]
        readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False)
        messagebox.showinfo("Sėkmė", "Skaitytojo informacija sėkmingai atnaujinta.")
        window.destroy()

    def delete_reader(self, reader_card_number, window):
        # Įkrauname skaitytojų duomenų failą
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

        # Paverčiame kortelės numerį į tekstą ir pašaliname bet kokius tarpelius
        readers_df['skaitytojo_kortele'] = readers_df['skaitytojo_kortele'].astype(str).str.strip()
        reader_card_number = str(reader_card_number).strip()

        # Patikriname, ar skaitytojas egzistuoja
        reader_info = readers_df[readers_df['skaitytojo_kortele'] == reader_card_number]

        if reader_info.empty:
            messagebox.showerror("Klaida", "Skaitytojas nerastas.")
            return

        # Paimame skaitymo istoriją
        reading_history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")
        reader_history = reading_history_df[reading_history_df['skaitytojo_kortele'] == reader_card_number]

        if reader_history.empty:
            messagebox.showinfo("Informacija", "Šis skaitytojas neturi jokių skaitymo įrašų.")

        # Perkeliame skaitytoją į removed_readers_db.csv
        removed_reader_data = pd.merge(reader_info, reader_history, on="skaitytojo_kortele", how="left")
        try:
            removed_readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_readers_db.csv")
        except FileNotFoundError:
            removed_readers_df = pd.DataFrame(columns=['vardas', 'pavarde', 'email', 'telefonas', 'skaitytojo_kortele', 
                                                    'autorius', 'knygos_pavadinimas', 'ISBN', 
                                                    'knygos_paemimo_data', 'knygos_grazinimo_data'])
        removed_readers_df = pd.concat([removed_readers_df, removed_reader_data], ignore_index=True)
        removed_readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_readers_db.csv", index=False, encoding="utf-8")

        # Pašaliname skaitytoją iš readers_db.csv
        readers_df = readers_df[readers_df['skaitytojo_kortele'] != reader_card_number]
        readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding="utf-8")

        messagebox.showinfo("Pašalinimas pavyko", f"Skaitytojas {reader_info['vardas'].values[0]} {reader_info['pavarde'].values[0]} sėkmingai pašalintas iš skaitytojų sąrašo")
        window.destroy()



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
            (readers_df['username'].str.contains(search_term, case=False, na=False)) |
            (readers_df['skaitytojo_kortele'].str.contains(search_term, case=False, na=False))
        ]

        # Atnaujiname TreeView su filtruotais duomenimis
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)

        for index, row in filtered_readers.iterrows():
            self.reader_tree.insert("", "end", values=(
                row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['skaitytojo_kortele'], row['username']
            ))

    
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
            
             
    
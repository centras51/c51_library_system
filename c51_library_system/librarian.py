import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
from books import Books
from readerregistration import ReaderRegistration
import datetime


class Librarian:
    def __init__(self, root, librarian_info):
        self.root = root
        self.librarian_info = librarian_info
        self.books_instance = Books(self.root)
        self.readerregistration_instance = ReaderRegistration(self.root, is_librarian=True)
        self.button_width = 30  
        self.button_height = 3  

        self.original_image = Image.open("D:\\CodeAcademy\\c51_library_system\\background\\library.png")
        self.background_image = self.original_image.resize((1400, 800), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.show_menu()  

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=1400, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(250, 50, text=f"Bibliotekininkas: {self.librarian_info[0]} {self.librarian_info[1]}, Tel: {self.librarian_info[2]}, El. paštas: {self.librarian_info[3]}", font=("Arial", 15, "bold"), fill="yellow", anchor="nw")

        self.add_button("Peržiūrėti knygas", 250, 200, self.books_instance.show_books)  
        self.add_button("Pridėti knygą", 250, 350, self.books_instance.add_book)  
        self.add_button("Išduotos knygos", 250, 500, self.lend_books)  
        self.add_button("Knygų statistika", 250, 650, self.books_instance.show_statistics)  

        self.add_button("Skaitytojų sąrašas", 700, 200, self.reader_list)  
        self.add_button("Pridėti skaitytoją", 700, 350, self.readerregistration_instance.register)  
        self.add_button("Pašalinti knygą", 700, 500, self.books_instance.remove_book)  
        self.add_button("Nurašytos knygos", 700, 650, self.books_instance.show_removed_books)  

        self.add_button("Peržiūrėti darbuotojus", 1150, 200, self.show_librarians)  
        self.add_button("Ištrinti skaitytojai", 1150, 350, self.show_removed_readers)  
        self.add_button("Atgal į prisijungimo langą", 1150, 500, self.go_back_to_login)  
        self.add_button("Išeiti iš sistemos", 1150, 650, self.root.quit)  

    def add_button(self, text, x_position, y_position, command):
        button = tk.Button(self.root, text=text, font=("Arial", 15), width=self.button_width, height=self.button_height,
                           bg="lightblue", fg="black", activebackground="darkblue", activeforeground="white", command=command)

        self.canvas.create_window(x_position, y_position, window=button)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def go_back_to_login(self):
        from librarian_login import LibrarianLogin
        librarian_login = LibrarianLogin(self.root)
        librarian_login.librarian_login_screen(back_function=self.go_back_to_login)

    def reader_list(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Skaitytojų sąrašas")

        search_label = tk.Label(new_window, text="Ieškoti skaitytojo:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_readers(search_entry))

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        self.reader_tree = ttk.Treeview(frame, columns=("Vardas", "Pavardė", "El. paštas", "Telefonas", "Skaitytojo kortelė", "Username"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.reader_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=self.reader_tree.yview)
        hsb.config(command=self.reader_tree.xview)

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

        self.populate_readers(self.reader_tree)

    def populate_readers(self, tree):
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        
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

        tree.bind("<Double-1>", lambda event: self.open_reader_profile(event, tree))

    def open_reader_profile(self, event, tree):
        item_id = tree.focus()  
        selected_item = tree.item(item_id)['values']

        if len(selected_item) < 6:
            messagebox.showerror("Klaida", "Nepavyko įkelti visų skaitytojo duomenų. Trūksta duomenų.")
            return

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
        books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        return books_df['knygos_pavadinimas'].tolist()

    def lend_books(self):
        books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        reading_history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")

        reading_history_df['knygos_grazinimo_data'] = pd.to_datetime(reading_history_df['knygos_grazinimo_data'], errors='coerce')

        merged_df = pd.merge(reading_history_df, readers_df[['skaitytojo_kortele', 'vardas', 'pavarde']], on='skaitytojo_kortele', how='left')

        final_df = pd.merge(merged_df, books_df[['knygos_pavadinimas', 'autorius']], on='knygos_pavadinimas', how='left')

        filtered_books_df = final_df[(final_df['faktine_grazinimo_data'].isna()) & (final_df['knygos_pavadinimas'].isin(books_df[books_df['statusas'] != 'laisva']['knygos_pavadinimas']))]

        new_window = tk.Toplevel(self.root)
        new_window.title("Išduotų į namus knygų sąrašas")

        tree = ttk.Treeview(new_window, columns=("Vardas", "Pavardė", "Skaitytojo Kortelė", "Autorius", "Knygos Pavadinimas", "Paėmimo Data", "Grąžinimo Data"), show="headings")

        tree.heading("Vardas", text="Vardas")
        tree.heading("Pavardė", text="Pavardė")
        tree.heading("Skaitytojo Kortelė", text="Skaitytojo Kortelė")
        tree.heading("Autorius", text="Autorius")
        tree.heading("Knygos Pavadinimas", text="Knygos Pavadinimas")
        tree.heading("Paėmimo Data", text="Paėmimo Data")
        tree.heading("Grąžinimo Data", text="Grąžinimo Data")

        tree.column("Vardas", width=100)
        tree.column("Pavardė", width=100)
        tree.column("Skaitytojo Kortelė", width=120)
        tree.column("Autorius", width=150)
        tree.column("Knygos Pavadinimas", width=200)
        tree.column("Paėmimo Data", width=120)
        tree.column("Grąžinimo Data", width=120)

        for index, row in filtered_books_df.iterrows():
            tree.insert("", tk.END, values=(
                row["vardas"], 
                row["pavarde"], 
                row["skaitytojo_kortele"], 
                row["autorius"], 
                row["knygos_pavadinimas"], 
                row["knygos_paemimo_data"], 
                row["knygos_grazinimo_data"]
            ))

        tree.pack(fill=tk.BOTH, expand=True)
        new_window.mainloop()






    def open_book_profile(self, book_title):
        self.books_instance.open_book_profile(None)

    def update_return_date(self, book_title):
        history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv",
                                usecols=['skaitytojo_kortele', 'knygos_pavadinimas', 'knygos_paemimo_data', 'knygos_grazinimo_data', 'faktine_grazinimo_data'],
                                encoding='utf-8', delimiter=',')

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        history_df.loc[(history_df['knygos_pavadinimas'] == book_title) & (history_df['faktine_grazinimo_data'].isnull()), 'faktine_grazinimo_data'] = current_date

        history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv", index=False, encoding='utf-8')

        messagebox.showinfo("Atnaujinimas", f"Knyga '{book_title}' sėkmingai pažymėta kaip grąžinta.")


    
    def show_reader_profile(self, reader_data):
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"Skaitytojo profilis: {reader_data['vardas']} {reader_data['pavarde']}")

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

        tk.Label(profile_window, text="Priskirti knygą:").pack(pady=5)
        book_list = self.get_books_list()  
        book_combobox = ttk.Combobox(profile_window, values=book_list)
        book_combobox.pack(pady=5)

        tk.Button(profile_window, text="Priskirti knygą", command=lambda: self.assign_book_to_reader(reader_data['skaitytojo_kortele'], book_combobox.get())).pack(pady=10)

        tk.Label(profile_window, text="Skaitymo istorija:").pack(pady=5)
        self.show_reading_history(profile_window, reader_data['skaitytojo_kortele'])

        tk.Button(profile_window, text="Išsaugoti pakeitimus", command=lambda: self.save_reader_changes(
            reader_data['skaitytojo_kortele'], vardas_entry.get(), pavarde_entry.get(), email_entry.get(), telefonas_entry.get(), profile_window)).pack(pady=10)

        tk.Button(profile_window, text="Ištrinti skaitytoją", command=lambda: self.delete_reader(reader_data['skaitytojo_kortele'], profile_window)).pack(pady=10)

    def show_reading_history(self, parent, reader_card_number):
        reading_history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")
        
        reader_history = reading_history_df[reading_history_df['skaitytojo_kortele'] == reader_card_number]

        if reader_history.empty:
            tk.Label(parent, text="Šis skaitytojas neturi skaitymo istorijos.").pack(pady=2)
            return

        for index, row in reader_history.iterrows():
            tk.Label(
                parent, 
                text=f"Knyga: {row['knygos_pavadinimas']}, Paėmimo data: {row['knygos_paemimo_data']}, Grąžinimo data: {row['knygos_grazinimo_data']}, Faktinė grąžinimo data: {row.get('faktine_grazinimo_data', 'Nėra')}"
            ).pack(pady=2)
            
    def assign_book_to_reader(self, reader_card_number, book_name):
        if book_name:
            readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")

            reader_card_number = str(reader_card_number).strip()

            reader_info = readers_df[readers_df['skaitytojo_kortele'].astype(str).str.strip() == reader_card_number]
            
            if reader_info.empty:
                messagebox.showerror("Klaida", f"Nerasta skaitytojo su kortelės numeriu: {reader_card_number}")
                return

            reader_info = reader_info.iloc[0]  

            active_loans = history_df[(history_df['skaitytojo_kortele'] == reader_card_number) &
                          (history_df['faktine_grazinimo_data'].isna())]

            if len(active_loans) >= 5:
                messagebox.showerror("DĖMESIO", "Jūs negalite paimti daugiau nei 5 knygas vienu metu.")
                return

            overdue_loans = history_df[(history_df['skaitytojo_kortele'] == reader_card_number) &
                                    (pd.to_datetime(history_df['knygos_grazinimo_data']) < pd.Timestamp.now())]

            if not overdue_loans.empty:
                messagebox.showerror("DĖMESIO", "Jūs negalite paimti naujų knygų, kol turite vėluojamų knygų.")
                return

            book_info = books_df[books_df['knygos_pavadinimas'] == book_name]

            if book_info.empty:
                messagebox.showerror("Klaida", f"Nerasta knyga su pavadinimu: {book_name}")
                return

            book_info = book_info.iloc[0]  

            last_loan_entry = history_df[history_df['knygos_pavadinimas'] == book_name].sort_values('knygos_grazinimo_data', ascending=False).head(1)

            history_df['knygos_grazinimo_data'] = pd.to_datetime(history_df['knygos_grazinimo_data'], errors='coerce')

            if not last_loan_entry.empty and last_loan_entry['knygos_grazinimo_data'].values[0] > pd.Timestamp.now():
                messagebox.showerror("Klaida", f"Knyga '{book_name}' jau yra užimta iki {last_loan_entry['knygos_grazinimo_data'].values[0]}.")
                return


            grazinimo_data = pd.Timestamp.now().date() + pd.Timedelta(days=14)  
            new_entry = pd.DataFrame({
                "vardas": [reader_info['vardas']],
                "pavarde": [reader_info['pavarde']],
                "skaitytojo_kortele": [reader_card_number],
                "autorius": [book_info['autorius']],
                "knygos_pavadinimas": [book_name],
                "ISBN": [book_info['ISBN']],
                "knygos_paemimo_data": [pd.Timestamp.now().date()],
                "knygos_grazinimo_data": [grazinimo_data],
                "faktine_grazinimo_data": [None],
                                        })

            history_df = pd.concat([history_df, new_entry], ignore_index=True)

            books_df.loc[books_df['knygos_pavadinimas'] == book_name, 'statusas'] = f"užimta iki {grazinimo_data}"

            history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv", index=False)
            books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False)

            messagebox.showinfo("Sėkmė", f"Knyga '{book_name}' sėkmingai priskirta skaitytojui {reader_info['vardas']} {reader_info['pavarde']}. Knyga užimta iki {grazinimo_data}.")
        else:
            messagebox.showerror("Klaida", "Pasirinkite knygą priskyrimui.")


    def save_reader_changes(self, reader_card_number, vardas, pavarde, email, telefonas, window):
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        readers_df.loc[readers_df['skaitytojo_kortele'] == reader_card_number, ['vardas', 'pavarde', 'email', 'telefonas']] = [vardas, pavarde, email, telefonas]
        readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False)
        messagebox.showinfo("Sėkmė", "Skaitytojo informacija sėkmingai atnaujinta.")
        window.destroy()

    def delete_reader(self, reader_card_number, window):
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

        readers_df['skaitytojo_kortele'] = readers_df['skaitytojo_kortele'].astype(str).str.strip()
        reader_card_number = str(reader_card_number).strip()

        reader_info = readers_df[readers_df['skaitytojo_kortele'] == reader_card_number]

        if reader_info.empty:
            messagebox.showerror("Klaida", "Skaitytojas nerastas.")
            return

        reading_history_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv")
        reader_history = reading_history_df[reading_history_df['skaitytojo_kortele'] == reader_card_number]

        if reader_history.empty:
            messagebox.showinfo("Informacija", "Šis skaitytojas neturi jokių skaitymo įrašų.")

        removed_reader_data = pd.merge(reader_info, reader_history, on="skaitytojo_kortele", how="left")
        try:
            removed_readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_readers_db.csv")
        except FileNotFoundError:
            removed_readers_df = pd.DataFrame(columns=['vardas', 'pavarde', 'email', 'telefonas', 'skaitytojo_kortele', 
                                                    'autorius', 'knygos_pavadinimas', 'ISBN', 
                                                    'knygos_paemimo_data', 'knygos_grazinimo_data', 'faktine_grazinimo_data'])
        removed_readers_df = pd.concat([removed_readers_df, removed_reader_data], ignore_index=True)
        removed_readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_readers_db.csv", index=False, encoding="utf-8")

        readers_df = readers_df[readers_df['skaitytojo_kortele'] != reader_card_number]
        readers_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding="utf-8")

        messagebox.showinfo("Pašalinimas pavyko", f"Skaitytojas {reader_info['vardas'].values[0]} {reader_info['pavarde'].values[0]} sėkmingai pašalintas iš skaitytojų sąrašo")
        window.destroy()



    def filter_readers(self, search_entry):
        search_term = search_entry.get().lower()
        readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")

        readers_df['vardas'] = readers_df['vardas'].astype(str)
        readers_df['pavarde'] = readers_df['pavarde'].astype(str)
        readers_df['email'] = readers_df['email'].astype(str)
        readers_df['telefonas'] = readers_df['telefonas'].astype(str)
        readers_df['skaitytojo_kortele'] = readers_df['skaitytojo_kortele'].astype(str)

        filtered_readers = readers_df[
            (readers_df['vardas'].str.contains(search_term, case=False, na=False)) |
            (readers_df['pavarde'].str.contains(search_term, case=False, na=False)) |
            (readers_df['email'].str.contains(search_term, case=False, na=False)) |
            (readers_df['telefonas'].str.contains(search_term, case=False, na=False)) |
            (readers_df['username'].str.contains(search_term, case=False, na=False)) |
            (readers_df['skaitytojo_kortele'].str.contains(search_term, case=False, na=False))
        ]

        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)

        for index, row in filtered_readers.iterrows():
            self.reader_tree.insert("", "end", values=(
                row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['skaitytojo_kortele'], row['username']
            ))

    
    def show_librarians(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Bibliotekininkų sąrašas")

        search_label = tk.Label(new_window, text="Ieškoti bibliotekininko:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_librarians(search_entry, new_window))

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        librarian_tree = ttk.Treeview(frame, columns=("Vardas", "Pavardė", "El. paštas", "Telefonas", "Username"), show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        librarian_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=librarian_tree.yview)
        hsb.config(command=librarian_tree.xview)

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

        self.populate_librarians(librarian_tree)

    def populate_librarians(self, tree):
        librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
        
        for item in tree.get_children():
            tree.delete(item)

        for index, row in librarians_df.iterrows():
            tree.insert("", "end", values=(row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['username']))

    def filter_librarians(self, search_entry, window):
        search_term = search_entry.get().lower()
        librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")

        librarians_df['vardas'] = librarians_df['vardas'].astype(str)
        librarians_df['pavarde'] = librarians_df['pavarde'].astype(str)
        librarians_df['email'] = librarians_df['email'].astype(str)
        librarians_df['telefonas'] = librarians_df['telefonas'].astype(str)
        librarians_df['username'] = librarians_df['username'].astype(str)

        filtered_librarians = librarians_df[
            (librarians_df['vardas'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['pavarde'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['email'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['telefonas'].str.contains(search_term, case=False, na=False)) |
            (librarians_df['username'].str.contains(search_term, case=False, na=False))
        ]

        tree = window.winfo_children()[1].winfo_children()[2]  
        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_librarians.iterrows():
            tree.insert("", "end", values=(row['vardas'], row['pavarde'], row['email'], row['telefonas'], row['username']))
            
    def show_removed_readers(self):
        messagebox.showwarning("Apribota paslauga", "Šiuo metu neįmanoma pažiūrėti pašalintų skaitytojų")
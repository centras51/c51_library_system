import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime
import re


class Books:
    def __init__(self, root, is_anonymous=False, is_reader=False):
        self.root = root
        self.is_anonymous = is_anonymous
        self.is_reader = is_reader
        self.books_df = self.load_books()
        self.readers_df = self.load_readers()
        self.reading_history_df = self.load_reading_history()
        self.selected_book = None

    def load_books(self):
        try:
            df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            required_columns = {'knygos_pavadinimas', 'autorius', 'metai', 'ISBN', 'zanras', 'pastabos', 'statusas'}
            if not required_columns.issubset(df.columns):
                messagebox.showerror("Klaida", "Trūksta būtinų stulpelių knygų duomenų bazėje.")
                return pd.DataFrame()
            df['knygos_pavadinimas'] = df['knygos_pavadinimas'].str.strip().str.title()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų bazės failas nerastas.")
            return pd.DataFrame()

    def load_readers(self):
        try:
            df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            required_columns = {'vardas', 'pavarde', 'email', 'telefonas', 'skaitytojo_kortele'}
            if not required_columns.issubset(df.columns):
                messagebox.showerror("Klaida", "Trūksta būtinų stulpelių skaitytojų duomenų bazėje.")
                return pd.DataFrame()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Skaitytojų duomenų bazės failas nerastas.")
            return pd.DataFrame()

    def load_reading_history(self):
        try:
            df = pd.read_csv(
                "D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv",
                usecols=['skaitytojo_kortele', 'knygos_pavadinimas', 'knygos_paemimo_data', 'knygos_grazinimo_data',
                         'faktine_grazinimo_data'],
                encoding='utf-8',
                delimiter=','
            )
            df['knygos_pavadinimas'] = df['knygos_pavadinimas'].str.strip().str.title()
            return df
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Skaitymo istorijos failas nerastas.")
            return pd.DataFrame()

    def get_current_reader(self, knygos_pavadinimas):
        knygos_pavadinimas = knygos_pavadinimas.strip().title()
        self.reading_history_df['knygos_paemimo_data'] = pd.to_datetime(
            self.reading_history_df['knygos_paemimo_data'], errors='coerce')
        self.reading_history_df['knygos_grazinimo_data'] = pd.to_datetime(
            self.reading_history_df['knygos_grazinimo_data'], errors='coerce')

        today = pd.Timestamp(datetime.now().date())

        current_reading = self.reading_history_df[
            (self.reading_history_df['knygos_pavadinimas'] == knygos_pavadinimas) &
            (self.reading_history_df['knygos_paemimo_data'] <= today) &
            (self.reading_history_df['knygos_grazinimo_data'] >= today)
            ]

        if not current_reading.empty:
            current_reading = current_reading.sort_values('knygos_paemimo_data', ascending=False).iloc[0]
            skaitytojo_kortele = current_reading['skaitytojo_kortele']
            reader = self.readers_df[self.readers_df['skaitytojo_kortele'] == skaitytojo_kortele]
            if not reader.empty:
                return reader.iloc[0]
        return None

    def show_books(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Knygų sąrašas")

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

        columns = ("knygos_pavadinimas", "autorius", "metai", "ISBN", "zanras", "pastabos", "statusas")
        book_tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=vsb.set,
                                 xscrollcommand=hsb.set)
        book_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=book_tree.yview)
        hsb.config(command=book_tree.xview)

        book_tree.heading("knygos_pavadinimas", text="Pavadinimas")
        book_tree.heading("autorius", text="Autorius")
        book_tree.heading("metai", text="Metai")
        book_tree.heading("ISBN", text="ISBN")
        book_tree.heading("zanras", text="Zanras")
        book_tree.heading("pastabos", text="Pastabos")
        book_tree.heading("statusas", text="statusas")

        book_tree.column("knygos_pavadinimas", width=200)
        book_tree.column("autorius", width=150)
        book_tree.column("metai", width=100)
        book_tree.column("ISBN", width=150)
        book_tree.column("zanras", width=150)
        book_tree.column("pastabos", width=350)
        book_tree.column("statusas", width=100)

        book_tree.bind("<Double-1>", self.open_book_profile)

        self.populate_books(book_tree)

    def populate_books(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        for index, row in self.books_df.iterrows():
            tree.insert("", "end", values=(
                row['knygos_pavadinimas'],
                row['autorius'],
                row['metai'],
                row['ISBN'],
                row['zanras'],
                row['pastabos'],
                row['statusas']
            ))

    def filter_books(self, search_entry, window):
        search_term = search_entry.get().title()
        filtered_books = self.books_df[
            (self.books_df['knygos_pavadinimas'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['autorius'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['metai'].astype(str).str.contains(search_term, case=False, na=False)) |
            (self.books_df['zanras'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['ISBN'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['pastabos'].str.contains(search_term, case=False, na=False)) |
            (self.books_df['statusas'].str.contains(search_term, case=False, na=False))
            ]

        tree = window.children['!frame'].children['!treeview']

        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_books.iterrows():
            tree.insert("", "end", values=(
                row['knygos_pavadinimas'],
                row['autorius'],
                row['metai'],
                row['ISBN'],
                row['zanras'],
                row['pastabos'],
                row['statusas']
            ))

    def open_book_profile(self, event):
        if event is not None:
            selected_item = event.widget.selection()[0]
            selected_book = event.widget.item(selected_item, "values")
            self.selected_book = selected_book
        else:
            selected_book = self.selected_book

        new_window = tk.Toplevel(self.root)
        new_window.title(f"Knygos profilis: {selected_book[0]}")

        is_readonly = self.is_reader or self.is_anonymous

        self.create_profile_field(new_window, "Pavadinimas:", selected_book[0], 100, is_readonly=is_readonly)
        self.create_profile_field(new_window, "Autorius:", selected_book[1], 150, is_readonly=is_readonly)
        self.create_profile_field(new_window, "Metai:", selected_book[2], 200, is_readonly=is_readonly)
        self.create_profile_field(new_window, "ISBN:", selected_book[3], 250, is_readonly=is_readonly)
        self.create_profile_field(new_window, "Zanras:", selected_book[4], 300, is_readonly=is_readonly)
        self.create_profile_field(new_window, "Pastabos:", selected_book[5], 350, is_readonly=is_readonly)

        knygos_statusas = selected_book[6]
        tk.Label(new_window, text=f"Statusas: {knygos_statusas}", font=("Arial", 15)).place(x=100, y=400)

        if "Rezervuota" in knygos_statusas:
            rezervavo = knygos_statusas.split(" ")[1]
            tk.Label(new_window, text=f"Rezervavo skaitytojas: {rezervavo}", font=("Arial", 15)).place(x=700, y=400)

        current_reader = self.get_current_reader(selected_book[0])
        if current_reader is not None:
            reader_info = f"{current_reader['vardas']} {current_reader['pavarde']}"
            if not self.is_reader:
                tk.Label(new_window, text=f"Skaito dabar: {reader_info}", font=("Arial", 15)).place(x=700, y=400)

        if not self.is_anonymous:
            if self.is_reader:
                self.add_button(new_window, "Rezervuoti knygą", 550, lambda: self.reserve_book(selected_book[0]))
            else:
                self.add_button(new_window, "Priskirti knygą skaitytojui", 430,
                                lambda: self.assign_book_to_reader_ui(selected_book[0], new_window))
                self.add_button(new_window, "Rezervuoti knygą", 510, lambda: self.reserve_book(selected_book[0]))
                self.add_button(new_window, "Išsaugoti pakeitimus", 590, self.save_book_edits)

                if not "laisva" in knygos_statusas.lower():
                    self.add_button(new_window, "Pažymėti kaip grąžintą", 670,
                                    lambda: self.return_book(selected_book[0], new_window))

                self.add_button(new_window, "Ištrinti knygą", 740,
                                lambda: self.confirm_delete_from_profile(selected_book[0], selected_book[3],
                                                                         new_window))

    def reserve_book(self, knygos_pavadinimas):
        if hasattr(self, 'reader_card_number') and self.reader_card_number:
            reader_card_number = self.reader_card_number
        else:
            reader_card_number = tk.simpledialog.askstring("Skaitytojo kortelė",
                                                           "Įveskite savo skaitytojo kortelės numerį:")

            if not reader_card_number:
                messagebox.showerror("Klaida", "Skaitytojo kortelės numeris neįvestas.")
                return

            self.reader_card_number = reader_card_number

        today = datetime.now()
        reservation_end = today + pd.Timedelta(hours=4)

        if self.get_current_reader(knygos_pavadinimas) is not None:
            messagebox.showerror("Klaida", "Ši knyga jau rezervuota arba užimta.")
            return

        reservation_status = f"Rezervuota {reader_card_number} iki {reservation_end.strftime('%Y-%m-%d %H:%M')}"
        self.books_df.loc[
            self.books_df['knygos_pavadinimas'] == knygos_pavadinimas.strip().title(), 'statusas'] = reservation_status
        self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')

        messagebox.showinfo("Sėkmė",
                            f"Knyga '{knygos_pavadinimas}' rezervuota iki {reservation_end.strftime('%Y-%m-%d %H:%M')}.")

        self.open_book_profile(None)

    def check_late_books(self, reader_card_number):
        self.reading_history_df['knygos_grazinimo_data'] = pd.to_datetime(
            self.reading_history_df['knygos_grazinimo_data'], errors='coerce')

        today = pd.Timestamp(datetime.now().date())

        late_books = self.reading_history_df[
            (self.reading_history_df['skaitytojo_kortele'] == reader_card_number) &
            (self.reading_history_df['knygos_grazinimo_data'] < today) &
            (self.reading_history_df['faktine_grazinimo_data'].isna())
            ]

        return not late_books.empty

    def get_reader_history(self, reader_card_number):
        history = self.reading_history_df[self.reading_history_df['skaitytojo_kortele'] == reader_card_number]

        books_read = history['knygos_pavadinimas'].tolist()

        reserved_books = self.books_df[
            self.books_df['statusas'].str.contains(f"Rezervuota {reader_card_number}", na=False)
        ]['knygos_pavadinimas'].tolist()

        return books_read + reserved_books

    def create_profile_field(self, window, label_text, value, y_position, is_readonly=False):
        label = tk.Label(window, text=label_text, font=("Arial", 15))
        label.place(x=100, y=y_position)
        entry = tk.Entry(window, font=("Arial", 15), width=40)
        entry.place(x=250, y=y_position)
        entry.insert(0, value)

        if is_readonly:
            entry.config(state='readonly')

        attribute_name = re.sub(r'\W+', '', label_text).title() + '_entry'
        setattr(self, attribute_name, entry)

    def add_button(self, window, text, y_position, command):
        button = tk.Button(window, text=text, font=("Arial", 15), width=20, height=2,
                           bg="lightblue", fg="black", activebackground="darkblue",
                           activeforeground="white", command=command)
        button.place(x=250, y=y_position)

        button.bind("<Enter>", lambda e: button.config(bg="darkblue", fg="white"))
        button.bind("<Leave>", lambda e: button.config(bg="lightblue", fg="black"))

    def save_book_edits(self):
        knygos_pavadinimas = self.Pavadinimas_entry.get()
        autorius = self.Autorius_entry.get()
        metai = self.Metai_entry.get()
        zanras = self.Zanras_entry.get()
        isbn = self.Isbn_entry.get()
        pastabos = self.Pastabos_entry.get()
        statusas = self.Statusas_entry.get()

        self.books_df.loc[
            self.books_df['ISBN'] == isbn, ['knygos_pavadinimas', 'autorius', 'metai', 'zanras', 'pastabos',
                                            'statusas']] = [
            knygos_pavadinimas.strip().title(), autorius, metai, zanras, pastabos, statusas
        ]

        self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')

        messagebox.showinfo("Sėkmė", f"Knygos '{knygos_pavadinimas}' duomenys buvo sėkmingai atnaujinti.")

    def assign_book_to_reader_ui(self, knygos_pavadinimas, window):
        assign_window = tk.Toplevel(self.root)
        assign_window.title(f"Priskirti knygą: {knygos_pavadinimas}")

        tk.Label(assign_window, text="Pasirinkite skaitytoją:", font=("Arial", 15)).place(x=100, y=50)

        reader_names = self.readers_df['vardas'] + ' ' + self.readers_df['pavarde']
        selected_reader = tk.StringVar(assign_window)
        selected_reader.set(reader_names.iloc[0])

        reader_menu = tk.OptionMenu(assign_window, selected_reader, *reader_names)
        reader_menu.place(x=250, y=50)

        self.add_button(assign_window, "Priskirti knygą", 150, lambda: self.assign_book_to_reader(
            knygos_pavadinimas,
            self.readers_df[self.readers_df['vardas'] + ' ' + self.readers_df['pavarde'] == selected_reader.get()][
                'skaitytojo_kortele'].values[0],
            window
        ))

    def assign_book_to_reader(self, knygos_pavadinimas, skaitytojo_kortele, window):
        if self.get_current_reader(knygos_pavadinimas) is not None:
            messagebox.showerror("Klaida", "Ši knyga jau priskirta kitam skaitytojui.")
            return

        planuojama_grazinimo_data = datetime.now() + pd.Timedelta(days=14)

        new_entry = {
            'skaitytojo_kortele': skaitytojo_kortele,
            'knygos_pavadinimas': knygos_pavadinimas.strip().title(),
            'knygos_paemimo_data': datetime.now().strftime('%Y-%m-%d'),
            'knygos_grazinimo_data': planuojama_grazinimo_data.strftime('%Y-%m-%d'),
            'faktine_grazinimo_data': None
        }

        self.reading_history_df = pd.concat([self.reading_history_df, pd.DataFrame([new_entry])], ignore_index=True)
        self.reading_history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv", index=False,
                                       encoding='utf-8')

        statusas_naujas = f"Užimta iki {planuojama_grazinimo_data.strftime('%Y-%m-%d')}"
        self.books_df.loc[
            self.books_df['knygos_pavadinimas'] == knygos_pavadinimas.strip().title(), 'statusas'] = statusas_naujas
        self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')

        messagebox.showinfo("Sėkmė",
                            f"Knyga '{knygos_pavadinimas}' priskirta skaitytojui iki {planuojama_grazinimo_data.strftime('%Y-%m-%d')}.")

        window.destroy()
        self.open_book_profile(None)

        window.destroy()
        self.open_book_profile(None)

    def return_book(self, knygos_pavadinimas, window):
        self.reading_history_df['knygos_grazinimo_data'] = pd.to_datetime(
            self.reading_history_df['knygos_grazinimo_data'], errors='coerce')
        self.reading_history_df['faktine_grazinimo_data'] = pd.to_datetime(
            self.reading_history_df['faktine_grazinimo_data'], errors='coerce')

        lend_check = (self.reading_history_df[
                          'knygos_pavadinimas'].str.strip().str.title() == knygos_pavadinimas.strip().title()) & \
                     (self.reading_history_df['faktine_grazinimo_data'].isna())

        if not self.reading_history_df.loc[lend_check].empty:
            index = self.reading_history_df.loc[lend_check].index[-1]
            if 'faktine_grazinimo_data' not in self.reading_history_df.columns:
                self.reading_history_df['faktine_grazinimo_data'] = pd.NaT
            self.reading_history_df.at[index, 'faktine_grazinimo_data'] = datetime.now().strftime('%Y-%m-%d')
            self.reading_history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv",
                                           index=False, encoding='utf-8')
            self.books_df.loc[self.books_df[
                                  'knygos_pavadinimas'].str.strip().str.title() == knygos_pavadinimas.strip().title(), 'statusas'] = 'laisva'
            self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False,
                                 encoding='utf-8')
            messagebox.showinfo("Sėkmė", f"Knyga '{knygos_pavadinimas}' sėkmingai grąžinta.")
            window.destroy()
            self.open_book_profile(None)
        else:
            messagebox.showerror("Klaida", "Knyga nėra paskolinta arba jau pažymėta kaip grąžinta.")

    def add_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pridėti naują knygą")

        self.create_profile_field(new_window, "knygos_pavadinimas:", "", 100)
        self.create_profile_field(new_window, "autorius:", "", 150)
        self.create_profile_field(new_window, "metai:", "", 200)
        self.create_profile_field(new_window, "zanras:", "", 250)
        self.create_profile_field(new_window, "ISBN:", "", 300)
        self.create_profile_field(new_window, "pastabos:", "", 350)
        self.create_profile_field(new_window, "statusas:", "", 400)

        self.add_button(new_window, "Pridėti knygą", 450, lambda: self.submit_book(new_window))

    def submit_book(self, window):
        new_book = {
            'knygos_pavadinimas': self.knygos_entry.get().strip().title(),
            'autorius': self.autorius_entry.get(),
            'metai': self.metai_entry.get(),
            'zanras': self.zanras_entry.get(),
            'ISBN': self.isbn_entry.get(),
            'pastabos': self.pastabos_entry.get(),
            'statusas': self.statusas_entry.get()
        }

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
            books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')
            messagebox.showinfo("Knyga pridėta sėkmingai",
                                f"Knyga '{new_book['knygos_pavadinimas']}' sėkmingai pridėta!")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų failas nerastas.")
        window.destroy()

    def show_statistics(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Skaitymo statistika")

        date_format = '%Y-%m-%d'
        self.reading_history_df['knygos_paemimo_data'] = pd.to_datetime(
            self.reading_history_df['knygos_paemimo_data'], format=date_format, errors='coerce'
        )
        self.reading_history_df['faktine_grazinimo_data'] = pd.to_datetime(
            self.reading_history_df['faktine_grazinimo_data'], format=date_format, errors='coerce'
        )

        valid_readings = self.reading_history_df.dropna(subset=['knygos_paemimo_data', 'faktine_grazinimo_data'])

        reading_times = (valid_readings['faktine_grazinimo_data'] - valid_readings['knygos_paemimo_data']).dt.days

        if not reading_times.empty:
            fastest_book_index = reading_times.idxmin()
            fastest_books = valid_readings.loc[fastest_book_index, 'knygos_pavadinimas']
        else:
            fastest_books = "Nėra duomenų"

        popular_books = self.reading_history_df['knygos_pavadinimas'].value_counts().head(10)
        popular_genres = self.books_df['zanras'].value_counts().head(5)

        tk.Label(new_window, text="Populiariausios knygos:", font=("Arial", 15)).pack(pady=10)
        for book, count in popular_books.items():
            tk.Label(new_window, text=f"{book} - {count} kartų", font=("Arial", 12)).pack(pady=5)

        tk.Label(new_window, text="Populiariausi žanrai:", font=("Arial", 15)).pack(pady=10)
        for genre, count in popular_genres.items():
            tk.Label(new_window, text=f"{genre} - {count} kartų", font=("Arial", 12)).pack(pady=5)

        tk.Label(new_window, text="Greičiausiai perskaityta knyga:", font=("Arial", 15)).pack(pady=10)
        tk.Label(new_window, text=f"{fastest_books}", font=("Arial", 12)).pack(pady=5)

    def remove_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pašalinti knygą")

        self.create_profile_field(new_window, "Įveskite ISBN:", "", 100)

        self.add_button(new_window, "Rasti knygą", 150, lambda: self.show_book_before_delete(new_window))

    def show_book_before_delete(self, window):
        isbn = self.isbn_entry.get()

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygų duomenų bazė nerasta")
            return

        book_to_delete = books_df[books_df["ISBN"] == isbn]

        if book_to_delete.empty:
            messagebox.showwarning("Įspėjimas", f"Knyga su ISBN {isbn} nerasta.")
        else:
            book_data = book_to_delete.iloc[0]
            confirm_window = tk.Toplevel(window)
            confirm_window.title(f"Ištrinti knygą: {book_data['knygos_pavadinimas']}?")

            tk.Label(confirm_window, text=f"Pavadinimas: {book_data['knygos_pavadinimas']}", font=("Arial", 12)).pack(
                pady=10)
            tk.Label(confirm_window, text=f"Autorius: {book_data['autorius']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"Metai: {book_data['metai']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"Žanras: {book_data['zanras']}", font=("Arial", 12)).pack(pady=5)
            tk.Label(confirm_window, text=f"ISBN: {book_data['ISBN']}", font=("Arial", 12)).pack(pady=5)

            tk.Label(confirm_window, text="Ištrynimo priežastis:", font=("Arial", 12)).pack(pady=5)
            deletion_reason_entry = tk.Entry(confirm_window, width=50)
            deletion_reason_entry.pack(pady=5)

            tk.Button(confirm_window, text="Patvirtinti trynimą", command=lambda: self.confirm_delete(
                book_data, books_df, confirm_window, deletion_reason_entry.get())).pack(pady=10)
            tk.Button(confirm_window, text="Atšaukti", command=confirm_window.destroy).pack(pady=10)

    def confirm_delete(self, book_data, books_df, confirm_window, deletion_reason):
        books_df_filtered = books_df[books_df["ISBN"] != book_data['ISBN']]

        books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False,
                                 encoding="UTF-8")

        book_data = book_data.copy()
        book_data['istrynimo_data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        book_data['istrynimo_priezastis'] = deletion_reason

        try:
            deleted_books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_books_db.csv")
        except FileNotFoundError:
            columns = ['autorius', 'knygos_pavadinimas', 'metai', 'ISBN', 'zanras', 'pastabos', 'istrynimo_data',
                       'istrynimo_priezastis']
            deleted_books_df = pd.DataFrame(columns=columns)

        deleted_books_df = pd.concat([deleted_books_df, pd.DataFrame([book_data])], ignore_index=True)
        deleted_books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_books_db.csv", index=False,
                                encoding="UTF-8")

        messagebox.showinfo("Ištrynimas sėkmingas",
                            f"Knyga '{book_data['knygos_pavadinimas']}' su ISBN {book_data['ISBN']} sėkmingai ištrinta.")

        confirm_window.destroy()

    def show_removed_books(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Nurašytos knygos")

        try:
            removed_books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_books_db.csv")
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Nėra nurašytų knygų duomenų.")
            return

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        columns = ['autorius', 'knygos_pavadinimas', 'metai', 'ISBN', 'zanras', 'pastabos', 'istrynimo_data',
                   'istrynimo_priezastis']
        book_tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=vsb.set,
                                 xscrollcommand=hsb.set)
        book_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=book_tree.yview)
        hsb.config(command=book_tree.xview)

        for col in columns:
            book_tree.heading(col, text=col.capitalize())

        book_tree.column("autorius", width=150)
        book_tree.column("knygos_pavadinimas", width=200)
        book_tree.column("metai", width=100)
        book_tree.column("ISBN", width=150)
        book_tree.column("zanras", width=150)
        book_tree.column("pastabos", width=200)
        book_tree.column("istrynimo_data", width=150)
        book_tree.column("istrynimo_priezastis", width=200)

        for index, row in removed_books_df.iterrows():
            book_tree.insert("", "end", values=(
                row['autorius'],
                row['knygos_pavadinimas'],
                row['metai'],
                row['ISBN'],
                row['zanras'],
                row['pastabos'],
                row['istrynimo_data'],
                row['istrynimo_priezastis']
            ))

    def confirm_delete_from_profile(self, knygos_pavadinimas, isbn, window):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title(f"Ištrinti knygą: {knygos_pavadinimas}?")

        tk.Label(confirm_window, text=f"Ar tikrai norite ištrinti knygą '{knygos_pavadinimas}'?",
                 font=("Arial", 12)).pack(pady=10)
        tk.Label(confirm_window, text="Ištrynimo priežastis:", font=("Arial", 12)).pack(pady=5)
        deletion_reason_entry = tk.Entry(confirm_window, width=50)
        deletion_reason_entry.pack(pady=5)

        tk.Button(confirm_window, text="Patvirtinti trynimą", command=lambda: self.confirm_delete_from_profile_action(
            knygos_pavadinimas, isbn, deletion_reason_entry.get(), window, confirm_window)).pack(pady=10)
        tk.Button(confirm_window, text="Atšaukti", command=confirm_window.destroy).pack(pady=10)

    def confirm_delete_from_profile_action(self, knygos_pavadinimas, isbn, deletion_reason, window, confirm_window):
        if not deletion_reason.strip():
            messagebox.showerror("Klaida", "Įveskite ištrynimo priežastį.")
            return

        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            book_data = books_df.loc[books_df['ISBN'] == isbn].iloc[0]
            books_df_filtered = books_df[books_df['ISBN'] != isbn]

            books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False,
                                     encoding="UTF-8")

            book_data['istrynimo_data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            book_data['istrynimo_priezastis'] = deletion_reason
            try:
                removed_books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_books_db.csv")
            except FileNotFoundError:
                removed_books_df = pd.DataFrame(
                    columns=['autorius', 'knygos_pavadinimas', 'metai', 'ISBN', 'zanras', 'pastabos', 'istrynimo_data',
                             'istrynimo_priezastis'])
            removed_books_df = pd.concat([removed_books_df, pd.DataFrame([book_data])], ignore_index=True)
            removed_books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\removed_books_db.csv", index=False,
                                    encoding="UTF-8")

            messagebox.showinfo("Sėkmė", f"Knyga '{knygos_pavadinimas}' su ISBN {isbn} sėkmingai ištrinta.")
            confirm_window.destroy()
            window.destroy()
        except FileNotFoundError:
            messagebox.showerror("Klaida", "Knygos duomenų bazė nerasta.")

    def show_return_books(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Grąžinimo laukiančios knygos")

        search_label = tk.Label(new_window, text="Ieškoti knygos:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", lambda event: self.filter_return_books(search_entry, new_window))

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        columns = (
        "knygos_pavadinimas", "autorius", "skaitytojas", "paemimo_data", "grazinimo_data", "faktine_grazinimo_data")
        return_tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=vsb.set,
                                   xscrollcommand=hsb.set)
        return_tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=return_tree.yview)
        hsb.config(command=return_tree.xview)

        return_tree.heading("knygos_pavadinimas", text="Knygos Pavadinimas")
        return_tree.heading("autorius", text="Autorius")
        return_tree.heading("skaitytojas", text="Skaitytojas")
        return_tree.heading("paemimo_data", text="Paimimo Data")
        return_tree.heading("grazinimo_data", text="Grąžinimo Data")

        return_tree.column("knygos_pavadinimas", width=200)
        return_tree.column("autorius", width=150)
        return_tree.column("skaitytojas", width=150)
        return_tree.column("paemimo_data", width=100)
        return_tree.column("grazinimo_data", width=100)

        return_tree.bind("<Double-1>", self.mark_book_returned)

        self.populate_return_books(return_tree)

    def populate_return_books(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        today = pd.Timestamp(datetime.now().date())
        filtered_history = self.reading_history_df[self.reading_history_df['knygos_grazinimo_data'] >= today]

        for index, row in filtered_history.iterrows():
            reader_info = self.readers_df[self.readers_df['skaitytojo_kortele'] == row['skaitytojo_kortele']].iloc[0]
            tree.insert("", "end", values=(
                row['knygos_pavadinimas'],
                self.books_df[self.books_df['knygos_pavadinimas'] == row['knygos_pavadinimas']]['autorius'].values[0],
                f"{reader_info['vardas']} {reader_info['pavarde']}",
                row['knygos_paemimo_data'],
                row['knygos_grazinimo_data'],
                row['faktine_grazinimo_data']
            ))

    def filter_return_books(self, search_entry, window):
        search_term = search_entry.get().title()
        filtered_history = self.reading_history_df[
            (self.reading_history_df['knygos_pavadinimas'].str.contains(search_term, case=False, na=False)) |
            (self.reading_history_df['knygos_grazinimo_data'].astype(str).str.contains(search_term, case=False,
                                                                                       na=False)),
            (self.reading_history_df['faktine_grazinimo_data'].astype(str).str.contains(search_term, case=False,
                                                                                        na=False))
        ]

        tree = window.children['!frame'].children['!treeview']
        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_history.iterrows():
            reader_info = self.readers_df[self.readers_df['skaitytojo_kortele'] == row['skaitytojo_kortele']].iloc[0]
            tree.insert("", "end", values=(
                row['knygos_pavadinimas'],
                self.books_df[self.books_df['knygos_pavadinimas'] == row['knygos_pavadinimas']]['autorius'].values[0],
                f"{reader_info['vardas']} {reader_info['pavarde']}",
                row['knygos_paemimo_data'],
                row['knygos_grazinimo_data'],
                row['faktine_grazinimo_data']
            ))

    def mark_book_returned(self, event):
        selected_item = event.widget.selection()[0]
        selected_book = event.widget.item(selected_item, "values")
        knygos_pavadinimas = selected_book[0]
        skaitytojas = selected_book[2]

        reader_card_number = self.readers_df[
            (self.readers_df['vardas'] + ' ' + self.readers_df['pavarde'] == skaitytojas)
        ]['skaitytojo_kortele'].values[0]

        confirm = messagebox.askyesno("Grąžinti Knygą",
                                      f"Ar tikrai norite pažymėti knygą '{knygos_pavadinimas}' kaip grąžintą?")
        if not confirm:
            return

        today = datetime.now().strftime('%Y-%m-%d')
        mask = (self.reading_history_df['knygos_pavadinimas'] == knygos_pavadinimas) & \
               (self.reading_history_df['skaitytojo_kortele'] == reader_card_number)

        self.reading_history_df.loc[mask, 'faktine_grazinimo_data'] = today
        self.reading_history_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\reading_history.csv", index=False,
                                       encoding='utf-8')

        self.books_df.loc[self.books_df['knygos_pavadinimas'] == knygos_pavadinimas, 'statusas'] = 'laisva'
        self.books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')

        messagebox.showinfo("Sėkmė", f"Knyga '{knygos_pavadinimas}' sėkmingai pažymėta kaip grąžinta.")

        self.populate_return_books()

    def search_for_book(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Paieška")

        self.create_profile_field(new_window, "Įveskite paieškos tekstą:", "", 100)
        self.add_button(new_window, "Ieškoti", 150,
                        lambda: self.filter_books(self.iveskitepaieskosteksta_entry, new_window))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Books(root, is_anonymous=False, is_reader=False)
    root.mainloop()

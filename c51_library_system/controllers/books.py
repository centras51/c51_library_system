import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Label, Entry, Button
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import threading


class Books:
    def __init__(self, root, is_anonymous=False, is_reader=False, reader_id=None):
        self.root = root
        self.is_anonymous = is_anonymous
        self.is_reader = is_reader
        self.reader_id = reader_id
        self.selected_book = None
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        return sqlite3.connect("D:\\CodeAcademy\\c51_library_system\\data_bases\\library_db.db")

    def get_reader_history(self, skaitytojo_kortele):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                query = """SELECT 
                        reading_history.knygos_isdavimo_data AS 'Paėmimo data',
                        reading_history.knygos_id as 'Knygos ID',
                        authors.vardas_pavarde AS 'Autoriaus vardas',
                        authors.pavarde AS 'Autoriaus pavardė',
                        books.knygos_pavadinimas AS 'Knygos pavadinimas',
                        books.ISBN
                    FROM
                        reading_history
                    JOIN
                        books ON books.knygos_id = reading_history.knygos_id
                    JOIN
                        authors ON authors.author_id = books.author_id
                    JOIN
                        readers ON readers.skaitytojo_id = reading_history.skaitytojo_id
                    WHERE
                        readers.skaitytojo_kortele = ? and books.statusas <> 'laisva';
                """
                cursor.execute(query, (skaitytojo_kortele,))
                history = cursor.fetchall()
            return history if history else []  
        except Exception as e:
            messagebox.showerror("Klaida", f"Klaida gaunant skaitymo istoriją: {e}")
            return []
        
    def submit_book(self, window):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO books 
                                (knygos_pavadinimas, autorius, metai, zanras, ISBN, pastabos, statusas)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                    self.knygos_entry.get().strip().title(),
                    self.autorius_entry.get(),
                    self.metai_entry.get(),
                    self.zanras_entry.get(),
                    self.isbn_entry.get(),
                    self.pastabos_entry.get(),
                    self.statusas_entry.get()
                ))
            messagebox.showinfo("Knyga pridėta sėkmingai", f"Knyga '{self.knygos_entry.get()}' pridėta!")
        except Exception as e:
            messagebox.showerror("Klaida", f"Pridedant knygą įvyko klaida: {e}")
        finally:
            window.destroy()

    def open_book_profile(self, event):
        selected_item = event.widget.selection()[0]
        selected_book = event.widget.item(selected_item, "values")
        
        profile_window = Toplevel(self.root)
        profile_window.title(f"Knygos profilis: {selected_book[3]}")  

        is_readonly = self.is_reader or self.is_anonymous  

        fields = [
            ("Knygos ID", selected_book[0], False),  
            ("Autoriaus vardas", selected_book[1], not self.is_reader and not self.is_anonymous),
            ("Autoriaus pavardė", selected_book[2], not self.is_reader and not self.is_anonymous),
            ("Knygos pavadinimas", selected_book[3], not self.is_reader and not self.is_anonymous),
            ("Metai", selected_book[4], not self.is_reader and not self.is_anonymous),
            ("Žanras", selected_book[5], not self.is_reader and not self.is_anonymous),
            ("ISBN", selected_book[6], not self.is_reader and not self.is_anonymous),
            ("Knygos aprašymas", selected_book[7], not self.is_reader and not self.is_anonymous),
            ("Statusas", selected_book[8], False)  
        ]

        entries = {}

        for i, (label_text, value, editable) in enumerate(fields):
            Label(profile_window, text=label_text + ":", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(profile_window, font=("Arial", 12), width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, value)
            if not editable:
                entry.config(state="readonly")
            entries[label_text] = entry  

        if not self.is_anonymous:  
            if self.is_reader:
                Button(profile_window, text="Rezervuoti knygą", font=("Arial", 12), command=lambda: self.reserve_book(selected_book[0])).grid(row=len(fields), column=1, pady=10)
            else:
                Button(profile_window, text="Priskirti knygą skaitytojui", font=("Arial", 12), command=lambda: self.assign_book_to_reader_ui(selected_book[0], profile_window)).grid(row=len(fields), column=0, pady=10)
                Button(profile_window, text="Rezervuoti knygą", font=("Arial", 12), command=lambda: self.reserve_book(selected_book[0])).grid(row=len(fields)+1, column=0, pady=10)
                Button(profile_window, text="Išsaugoti pakeitimus", font=("Arial", 12), command=lambda: self.save_book_edits(entries)).grid(row=len(fields)+2, column=0, pady=10)
                
                if "užimta" in selected_book[8].lower():
                    Button(profile_window, text="Pažymėti kaip grąžintą", font=("Arial", 12), command=lambda: self.return_book(selected_book[0], profile_window)).grid(row=len(fields)+3, column=0, pady=10)

                Button(profile_window, text="Ištrinti knygą", font=("Arial", 12), command=lambda: self.confirm_delete(selected_book[0], "Ištrynimo priežastis", profile_window)).grid(row=len(fields)+4, column=0, pady=10)

    def create_profile_field(self, window, label_text, value, y_position, is_readonly=False):
        tk.Label(window, text=label_text, font=("Arial", 12)).place(x=50, y=y_position)
        entry = tk.Entry(window, font=("Arial", 12), width=40)
        entry.place(x=200, y=y_position)
        entry.insert(0, value)
        if is_readonly:
            entry.config(state="readonly")
        return entry

    def add_button(self, window, text, y_position, command):
        button = tk.Button(window, text=text, command=command, font=("Arial", 12), width=20)
        button.place(x=200, y=y_position)
        return button

    def reserve_book(self, knygos_id):
        try:
            if not self.reader_id:
                messagebox.showerror("Klaida", "Skaitytojo ID nėra nustatytas. Rezervacija negalima.")
                return

            reservation_end = datetime.now() + timedelta(hours=4)

            with sqlite3.connect("D:\\CodeAcademy\\c51_library_system\\data_bases\\library_db.db", timeout=10) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO reading_history 
                    (skaitytojo_id, knygos_id, knygos_isdavimo_data, data_grazinimui, pradelstos_dienos, bauda) 
                    VALUES (?, ?, ?, ?, 0, 0)
                """, (self.reader_id, knygos_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), reservation_end.strftime('%Y-%m-%d %H:%M:%S')))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Klaida", "Nepavyko įrašyti rezervacijos į skaitymo istoriją.")
                    return

                cursor.execute("""
                    UPDATE books SET statusas = ? WHERE knygos_id = ?
                """, (f"Rezervuota iki {reservation_end.strftime('%Y-%m-%d %H:%M')}", knygos_id))

            messagebox.showinfo("Rezervacija sėkminga", "Knyga sėkmingai rezervuota.")
            
            threading.Timer(4 * 3600, self.schedule_clear_reservation, args=[knygos_id]).start()
            
        except sqlite3.Error as e:
            messagebox.showerror("Klaida", f"Rezervuojant knygą įvyko klaida: {e}")

    def schedule_clear_reservation(self, knygos_id):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT statusas FROM books WHERE knygos_id = ?", (knygos_id,))
                statusas = cursor.fetchone()
                if statusas and "Rezervuota" in statusas[0]:
                    cursor.execute("UPDATE books SET statusas = 'laisva' WHERE knygos_id = ?", (knygos_id,))
                    conn.commit()
                    print(f"Knygos {knygos_id} rezervacija baigėsi, statusas grąžintas į 'laisva'.")
        except Exception as e:
            print(f"Klaida keičiant rezervacijos statusą: {e}")


    def save_book_edits(self, entries):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE books
                                SET knygos_pavadinimas = ?, autorius = ?, metai = ?, zanras = ?, pastabos = ?, ISBN = ?
                                WHERE knygos_id = ?""", (
                    entries["Knygos pavadinimas"].get().strip().title(),
                    entries["Autoriaus vardas"].get(),
                    entries["Metai"].get(),
                    entries["Žanras"].get(),
                    entries["Knygos aprašymas"].get(),
                    entries["ISBN"].get(),
                    entries["Knygos ID"].get()
                ))
            messagebox.showinfo("Duomenys atnaujinti", "Knygos duomenys buvo atnaujinti.")
        except Exception as e:
            messagebox.showerror("Klaida", f"Atnaujinant knygą įvyko klaida: {e}")

    def assign_book_to_reader(self, knygos_id, skaitytojo_id, window):
        try:
            planuojama_grazinimo_data = datetime.now() + timedelta(days=14)
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO reading_history 
                                (skaitytojo_id, knygos_id, knygos_isdavimo_data, data_grazinimui)
                                VALUES (?, ?, ?, ?)""", (
                    skaitytojo_id,
                    knygos_id,
                    datetime.now().strftime('%Y-%m-%d'),
                    planuojama_grazinimo_data.strftime('%Y-%m-%d')
                ))
                cursor.execute("""UPDATE books
                                SET statusas = ?
                                WHERE knygos_id = ?""", (
                    f"Užimta iki {planuojama_grazinimo_data.strftime('%Y-%m-%d')}",
                    knygos_id
                ))
            messagebox.showinfo("Sėkmė", "Knyga priskirta skaitytojui.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Klaida", f"Priskiriant knygą įvyko klaida: {e}")

    def return_book(self, knygos_id, iraso_id, window):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE reading_history
                                SET faktine_grazinimo_data = ?
                                WHERE iraso_id = ? AND knygos_id = ?""", (today, iraso_id, knygos_id))
                cursor.execute("""UPDATE books
                                SET statusas = 'laisva'
                                WHERE knygos_id = ?""", (knygos_id,))
                self.update_return_data(iraso_id, today)
            messagebox.showinfo("Sėkmė", "Knyga pažymėta kaip grąžinta.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Klaida", f"Grąžinant knygą įvyko klaida: {e}")

    def confirm_delete(self, knygos_id, deletion_reason):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO removed_books (knygos_id, istrynimo_priezastis)
                                VALUES (?, ?)""", (knygos_id, deletion_reason))
                cursor.execute("DELETE FROM books WHERE knygos_id = ?", (knygos_id,))
            messagebox.showinfo("Sėkmė", "Knyga sėkmingai ištrinta.")
        except Exception as e:
            messagebox.showerror("Klaida", f"Ištrinant knygą įvyko klaida: {e}")

    def show_removed_books(self):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT books.knygos_pavadinimas, books.autorius, books.metai, books.ISBN, 
                                  books.zanras, books.pastabos, removed_books.istrynimo_data, removed_books.istrynimo_priezastis
                                  FROM removed_books
                                  JOIN books ON removed_books.knygos_id = books.knygos_id""")
                removed_books = cursor.fetchall()
            new_window = tk.Toplevel(self.root)
            new_window.title("Nurašytos knygos")

            frame = tk.Frame(new_window)
            frame.pack(fill=tk.BOTH, expand=True)

            vsb = tk.Scrollbar(frame, orient="vertical")
            vsb.pack(side="right", fill="y")

            hsb = tk.Scrollbar(frame, orient="horizontal")
            hsb.pack(side="bottom", fill="x")

            columns = ['knygos_pavadinimas', 'autorius', 'metai', 'ISBN', 'zanras', 'pastabos', 'istrynimo_data', 'istrynimo_priezastis']
            book_tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            book_tree.pack(fill=tk.BOTH, expand=True)

            vsb.config(command=book_tree.yview)
            hsb.config(command=book_tree.xview)

            for col in columns:
                book_tree.heading(col, text=col.capitalize())

            for row in removed_books:
                book_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Klaida", f"Nurašytų knygų įkėlimo klaida: {e}")

    def update_return_data(self, iraso_id, faktine_grazinimo_data=None):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT data_grazinimui FROM reading_history WHERE iraso_id = ?", (iraso_id,))
                record = cursor.fetchone()
                if not record:
                    messagebox.showerror("Klaida", "Įrašo su pateiktu ID nėra.")
                    return

                data_grazinimui = datetime.strptime(record[0], "%Y-%m-%d")
                grazinimo_data = datetime.strptime(faktine_grazinimo_data, "%Y-%m-%d") if faktine_grazinimo_data else datetime.now()
                
                pradelstos_dienos = np.busday_count(data_grazinimui.date(), grazinimo_data.date())
                bauda = round(pradelstos_dienos * 0.03, 2) if pradelstos_dienos > 0 else 0

                cursor.execute("""UPDATE reading_history
                                SET faktine_grazinimo_data = ?, pradelstos_dienos = ?, bauda = ?
                                WHERE iraso_id = ?""", 
                               (grazinimo_data.strftime("%Y-%m-%d"), pradelstos_dienos, bauda, iraso_id))
            messagebox.showinfo("Grąžinimas pavyko", f"Grąžinimas sėkmingai atnaujintas. Pradelstos dienos: {pradelstos_dienos}, Bauda: {bauda} EUR")
        except Exception as e:
            messagebox.showerror("Klaida", f"Įvyko klaida atnaujinant grąžinimo informaciją: {e}")

    def check_late_books(self, reader_id):
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("""SELECT COUNT(*)
                                FROM reading_history
                                WHERE skaitytojo_id = ? AND faktine_grazinimo_data IS NULL AND data_grazinimui < ?""",
                               (reader_id, today))
                late_books_count = cursor.fetchone()[0]
            if late_books_count > 0:
                messagebox.showwarning(
                    "Vėluojančios knygos",
                    f"Turite {late_books_count} vėluojančių knygų. Prašome jas grąžinti kuo greičiau."
                )
        except Exception as e:
            messagebox.showerror("Klaida", f"Įvyko klaida tikrinant vėluojančias knygas: {e}")

    def show_books(self):
        new_window = Toplevel(self.root)
        new_window.title("Knygų sąrašas")

        search_label = tk.Label(new_window, text="Ieškoti knygos:")
        search_label.pack(pady=5)
        search_entry = tk.Entry(new_window)
        search_entry.pack(pady=5)

        frame = tk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Knygos ID", "Autoriaus vardas", "Autoriaus pavardė", "Knygos pavadinimas", 
                "Metai", "Žanras", "ISBN", "Knygos aprašymas", "Statusas")
        book_tree = ttk.Treeview(frame, columns=columns, show="headings")
        book_tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            book_tree.heading(col, text=col)

        book_tree.bind("<Double-1>", lambda event: self.open_book_profile(event))

        search_entry.bind("<KeyRelease>", lambda event: self.filter_books(search_entry, book_tree))

        self.populate_books(book_tree)

    def populate_books(self, tree):
        books = self.load_books()
        for item in tree.get_children():
            tree.delete(item)
        for row in books:
            tree.insert("", "end", values=row)

    def filter_books(self, search_entry, tree):
        search_term = search_entry.get().lower()
        books = self.load_books()
        for item in tree.get_children():
            tree.delete(item)
        for row in books:
            if any(search_term in str(value).lower() for value in row):
                tree.insert("", "end", values=row)

    def load_books(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT 
                                books.knygos_id,
                                authors.vardas_pavarde as 'Autoriaus vardas',
                                authors.pavarde as 'Autoriaus pavardė',
                                books.knygos_pavadinimas as 'Knygos pavadinimas',
                                books.metai as 'Metai',
                                books.zanras as 'Žanras',
                                books.ISBN,
                                books.pastabos as 'Knygos aprašymas',
                                books.statusas as 'Statusas'
                              FROM books
                              JOIN authors ON books.author_id = authors.author_id""")
            return cursor.fetchall()


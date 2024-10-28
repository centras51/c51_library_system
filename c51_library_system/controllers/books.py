import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta
import numpy as np


class Books:
    def __init__(self, root, is_anonymous=False, is_reader=False):
        self.root = root
        self.is_anonymous = is_anonymous
        self.is_reader = is_reader
        self.selected_book = None
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        return sqlite3.connect("D:\\CodeAcademy\\c51_library_system\\data_bases\\library_db.db")

    def submit_book(self, window):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO books (knygos_pavadinimas, autorius, metai, zanras, ISBN, pastabos, statusas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.knygos_entry.get().strip().title(),
                self.autorius_entry.get(),
                self.metai_entry.get(),
                self.zanras_entry.get(),
                self.isbn_entry.get(),
                self.pastabos_entry.get(),
                self.statusas_entry.get()
            ))
            self.connection.commit()
            messagebox.showinfo("Knyga pridėta sėkmingai", f"Knyga '{self.knygos_entry.get()}' pridėta!")
        except Exception as e:
            messagebox.showerror("Klaida", f"Pridedant knygą įvyko klaida: {e}")
        finally:
            window.destroy()

    def save_book_edits(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE books
                SET knygos_pavadinimas = ?, autorius = ?, metai = ?, zanras = ?, pastabos = ?, statusas = ?
                WHERE ISBN = ?
            """, (
                self.Pavadinimas_entry.get().strip().title(),
                self.Autorius_entry.get(),
                self.Metai_entry.get(),
                self.Zanras_entry.get(),
                self.Pastabos_entry.get(),
                self.Statusas_entry.get(),
                self.Isbn_entry.get()
            ))
            self.connection.commit()
            messagebox.showinfo("Sėkmė", "Knygos duomenys buvo atnaujinti.")
        except Exception as e:
            messagebox.showerror("Klaida", f"Atnaujinant knygą įvyko klaida: {e}")

    def assign_book_to_reader(self, knygos_pavadinimas, skaitytojo_kortele, window):
        try:
            cursor = self.connection.cursor()
            planuojama_grazinimo_data = datetime.now() + timedelta(days=14)
            cursor.execute("""
                INSERT INTO reading_history (skaitytojo_kortele, knygos_id, knygos_paemimo_data, data_grazinimui)
                VALUES (?, (SELECT knygos_id FROM books WHERE knygos_pavadinimas = ?), ?, ?)
            """, (
                skaitytojo_kortele,
                knygos_pavadinimas.strip().title(),
                datetime.now().strftime('%Y-%m-%d'),
                planuojama_grazinimo_data.strftime('%Y-%m-%d')
            ))
            cursor.execute("""
                UPDATE books
                SET statusas = ?
                WHERE knygos_pavadinimas = ?
            """, (
                f"Užimta iki {planuojama_grazinimo_data.strftime('%Y-%m-%d')}",
                knygos_pavadinimas.strip().title()
            ))
            self.connection.commit()
            messagebox.showinfo("Sėkmė", f"Knyga '{knygos_pavadinimas}' priskirta skaitytojui.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Klaida", f"Priskiriant knygą įvyko klaida: {e}")

    def return_book(self, knygos_id, window):
        # Pažymi knygą kaip grąžintą pagal knygos ID
        try:
            cursor = self.connection.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                UPDATE reading_history
                SET faktine_grazinimo_data = ?
                WHERE knygos_id = ? AND faktine_grazinimo_data IS NULL
            """, (today, knygos_id))
            cursor.execute("""
                UPDATE books
                SET statusas = 'laisva'
                WHERE knygos_id = ?
            """, (knygos_id,))
            self.connection.commit()
            messagebox.showinfo("Sėkmė", "Knyga pažymėta kaip grąžinta.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Klaida", f"Grąžinant knygą įvyko klaida: {e}")

    def confirm_delete(self, knygos_id, deletion_reason):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO removed_books (knygos_id, istrynimo_priezastis)
                SELECT knygos_id, ?
                FROM books
                WHERE knygos_id = ?
            """, (deletion_reason, knygos_id))
            cursor.execute("DELETE FROM books WHERE knygos_id = ?", (knygos_id,))
            self.connection.commit()
            messagebox.showinfo("Sėkmė", "Knyga sėkmingai ištrinta.")
        except Exception as e:
            messagebox.showerror("Klaida", f"Ištrinant knygą įvyko klaida: {e}")

    def show_removed_books(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT books.knygos_pavadinimas, books.autorius, books.metai, books.ISBN, books.zanras, books.pastabos, 
                       removed_books.istrynimo_data, removed_books.istrynimo_priezastis
                FROM removed_books
                JOIN books ON removed_books.knygos_id = books.knygos_id
            """)
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
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT data_grazinimui
                FROM reading_history
                WHERE iraso_id = ?
            """, (iraso_id,))
            
            record = cursor.fetchone()
            if not record:
                messagebox.showerror("Klaida", "Įrašo su pateiktu ID nėra.")
                return

            data_grazinimui = datetime.strptime(record[0], "%Y-%m-%d")
            
            grazinimo_data = datetime.strptime(faktine_grazinimo_data, "%Y-%m-%d") if faktine_grazinimo_data else datetime.now()
            
            pradelstos_dienos = np.busday_count(data_grazinimui.date(), grazinimo_data.date())
            bauda = round(pradelstos_dienos * 0.03, 2) if pradelstos_dienos > 0 else 0

            cursor.execute("""
                UPDATE reading_history
                SET faktine_grazinimo_data = ?, pradelstos_dienos = ?, bauda = ?
                WHERE iraso_id = ?
            """, (grazinimo_data.strftime("%Y-%m-%d"), pradelstos_dienos, bauda, iraso_id))
            
            self.connection.commit()
            messagebox.showinfo("Sėkmė", f"Grąžinimas sėkmingai atnaujintas. Pradelstos dienos: {pradelstos_dienos}, Bauda: {bauda} EUR")
        except Exception as e:
            messagebox.showerror("Klaida", f"Įvyko klaida atnaujinant grąžinimo informaciją: {e}")
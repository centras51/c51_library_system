import streamlit as st

class Books():
    def __init__(self) -> None:
        pass
    
    def find_book(self):
        pass
    
    def find_reservation(self):
        pass
    
    def show_books(self):
        pass
    
    def show_history(self):
        pass
    
    def show_book_profile(self, book_row):
        st.subheader(f"Knyga: {book_row['knygos_pavadinimas']}")
        st.write(f"Autorius: {book_row['autorius']}")
        st.write(f"Išleidimo metai: {book_row['metai']}")
        st.write(f"ISBN: {book_row['ISBN']}")
        st.write(f"Žanras: {book_row['zanras']}")
        st.write(f"Aprašymas: {book_row['pastabos']}")
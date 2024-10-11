import pandas as pd
import streamlit as st

class Reader:
    def __init__(self) -> None:
        pass
    
    def username_password_verification(self, username, password):
        usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv")
        user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
        if not user_info.empty:
            return user_info['password'].values[0] == password
        return False
    
    def make_reservation(self):
        pass
    
    def find_book(self):
        pass
    
    def show_books(self):
        try:
            books_df = pd.read_csv("CSVs/books_db.csv")
            return books_df
        except FileNotFoundError:
            st.error("Knygų sąrašas nerastas.")
            
    def show_reader_history(self):
        pass
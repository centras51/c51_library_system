import pandas as pd
import datetime as dt
import streamlit as st
import getpass
import re
import random


st.set_page_config(layout="wide")

class Librarian:
    def __init__(self) -> None:
        pass

    def username_password_verification(self, username, password):
        usr_psw_df = pd.read_csv("CSVs\\librarians_db.csv")
        user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
        if not user_info.empty:
            return user_info['password'].values[0] == password
        return False
        
    def find_reader(self):
        pass
    
    def find_book(self):
        pass
    
    def remove_book(self):
        pass
    
    def add_book(self):
        pass
    

class Reader:
    def __init__(self) -> None:
        pass
    
    def username_password_verification(self, username, password):
        usr_psw_df = pd.read_csv("CSVs\\passwords_db.csv")
        user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
        if not user_info.empty:
            return user_info['password'].values[0] == password
        return False
    
    def make_reservation(self):
        pass
    
    def find_book(self):
        pass
    
    def show_reader_history(self):
        pass

class ReaderRegistration:
    def __init__(self) -> None:
        pass
    
    def is_valid_email(self, reader_email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        return re.match(email_regex, reader_email) is not None
    
    def is_valid_phone(self, reader_phone):
        number_length = len(reader_phone)
        first_digit = reader_phone[0]
        return reader_phone.isnumeric() and number_length == 8 and first_digit == "6"
    
    def reader_card_number_generator(self):
        self.reader_card_number = random.randint(10000000, 99999999)
        reader_df = pd.read_csv("CSVs\\readers_db.csv")
        existing_reader_card_numbers = reader_df['skaitytojo_kortele'].to_list()
        while True:
            if self.reader_card_number not in existing_reader_card_numbers:
                return self.reader_card_number
    
    def save_reader_datas(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number):
        new_reader_line = {'vardas': reader_name, 'pavarde': reader_last_name, 'email': reader_email, 'telefonas': reader_phone, 'skaitytojo_kortele': reader_card_number}
        reader_df = pd.read_csv("CSVs\\readers_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("CSVs\\readers_db.csv", index=False, encoding='utf-8')
        
    def save_reader_password(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number, username, password):
        new_reader_line = {'vardas': reader_name, 'pavarde': reader_last_name, 'email': reader_email, 'telefonas': reader_phone, 'skaitytojo_kortele': reader_card_number, 'username': username, 'password': password}
        reader_df = pd.read_csv("CSVs\\passwords_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("CSVs\\passwords_db.csv", index=False, encoding='utf-8')


class BorrowBook():
    def __init__(self) -> None:
        pass
    
    def take_book(self):
        pass
    
    def return_book(self):
        pass
    
    def set_term(self):
        pass
    
    def books_with_delay(self):
        pass
    
    def fines_for_delay(self):
        pass
    

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

reader_registration = ReaderRegistration()
librarian = Librarian()
reader = Reader()

st.title("C51 BIBLIOTEKOS SISTEMA")

col1, col2, col3, col4 = st.columns([0.5, 0.5, 0.5, 0.5])

with col1:
    if st.button("Prisijungimas bibliotekininkui"):
        st.write("Prisijungimas bibliotekininkui")

with col2:
    if st.button("Prisijungimas bibliotekos lankytojui"):
        st.write("Prisijungimas bibliotekos lankytojui")

with col3:
    if st.button("Dirbti neprisijungus (apribotos funkcijos)"):
        st.write("Dirbti neprisijungus (apribotos funkcijos)")
        
with col4:
    if st.button("Naujo skaitytojo registracija"):
        st.write("Naujo skaitytojo registracija")
        
        
    print("-" * 50)
    print("C51 BIBLIOTEKOS SISTEMA")
    print("-" * 50)
    print("2. Prisijungimas bibliotekos lankytojui.")
    print("3. Dirbti neprisijungus (apribotos funkcijos).")
    print("4. Naujo skaitytojo registracija.")
    print("5. Išeiti iš programos.")
    print("-" * 50)
    try:
        choose_1_level = int(input("Įveskite savo pasirinkimą (1 - 5):\n"))
        if choose_1_level == 1:
            print("-" * 50)
            print("C51 BIBLIOTEKOS SISTEMA")
            print("-" * 50)
            print("Norėdami prisijungti prie darbuotojo aplinkos, įveskite savo duomenis")
            print("-" * 50)
            librarian_login_user_name = input("Įveskite naudotojo vardą:\n ")
            librarian_login_password = input("Įveskite slaptažodį:\n ")
            if not librarian.username_password_verification(librarian_login_user_name, librarian_login_password):
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                print("Neteisingas slaptažodis arba vartotojo vardas!")
            else:
                print(f"Sveiki prisijungę, {librarian_login_user_name}!")
        elif choose_1_level == 2:
            print("-" * 50)
            print("C51 BIBLIOTEKOS SISTEMA")
            print("-" * 50)
            print("Norėdami prisijungti prie lankytojo aplinkos, įveskite savo duomenis")
            print("-" * 50)
            reader_login_user_name = input("Įveskite naudotojo vardą:\n ")
            reader_login_password = input("Įveskite slaptažodį:\n ")
            if not reader.username_password_verification(reader_login_user_name, reader_login_password):
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                print("Neteisingas slaptažodis arba vartotojo vardas!")
            else:
                print(f"Sveiki prisijungę, {reader_login_user_name}!")
            while True:    
                print("1. Peržiūrėti leidinių sąrašą;")
                print("2. Ieškoti leidinių.")
                print("3. Grįžti į pagrindinį langą.")
                print("4. Išeiti iš programos.")
                choose_1_3_level = input("Pasirinkite 1-4:\n")
        elif choose_1_level == 3:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                print("Darbas su apribotomis funkcijomis. Be registracijos galite:")
                print("1. Peržiūrėti leidinių sąrašą;")
                print("2. Ieškoti leidinių.")
                print("3. Grįžti į pagrindinį langą.")
                print("4. Išeiti iš programos.")
                anonymous_choose = int(input("Pasirinkite 1-4:\n"))
        elif choose_1_level == 4:
            while True:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("NAUJO SKAITYTOJO REGISTRACIJA")
                print("-" * 50)
                reader_name = input("Įveskite savo vardą:\n").strip().title()
                if not reader_name.isalpha():
                    print(f"Vardą turi sudaryti tik raidės. Jūsų įvestas vardas {reader_name} yra netinkamas.")
                    continue
                reader_last_name = input("Įveskite savo pavardę:\n").strip().title()
                if not reader_last_name.isalpha():
                    print(f"Pavardę turi sudaryti tik raidės. Jūsų įvesta pavardė {reader_last_name} yra netinkama.")
                    continue
                reader_email = input("Įveskite savo el. pašto adresą:\n")
                if not reader_registration.is_valid_email(reader_email):
                    print(f"Jūsų įvestas el. pašto adresas {reader_email} neatitinka reikalavimų.")
                    continue
                while True:
                    username = input("Įveskite naują vartotojo vardą:\n")
                    password = input("Įveskite naują slaptažodį:\n")
                    password2 = input("Pakartokite slaptažodį:\n")
                    if password != password2:
                        print("Slaptažodžiai nesutampa! Pakartokite iš naujo")
                        continue
                    else:
                        break
                while True:
                    reader_phone = input("Įveskite savo telefono numerį: +370")
                    if not reader_registration.is_valid_phone(reader_phone):
                        print(f"Klaida! Patikrinkite telefono numerį. Jūsų įvestas numeris:\n{reader_phone}")
                    else:
                        reader_phone = "+370" + reader_phone
                        break
                print(f"Registracija sėkminga. Jūsų duomenys:\n {reader_name} {reader_last_name},\n Telefono numeris: {reader_phone}\n Email: {reader_email}")
                print(f"Jūsų skaitytojo kortelės numeris: {reader_registration.reader_card_number_generator()}")
                reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, reader_phone, reader_registration.reader_card_number_generator())
                reader_registration.save_reader_password(reader_name, reader_last_name, reader_email, reader_phone, reader_registration.reader_card_number, username, password)
                break
            
        elif choose_1_level == 5:
            print("Išeinama iš programos!")
    except ZeroDivisionError:
        print("Reikšmė turi būti 1-5")
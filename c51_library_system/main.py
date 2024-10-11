import pandas as pd
import datetime as dt
import streamlit as st
import getpass
import re
from readeregistration import ReaderRegistration
from librarian import Librarian
from reader import Reader


st.set_page_config(layout="wide")







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

menu = ["Prisijungimas bibliotekininkui", "Prisijungimas lankytojui", "Dirbti neprisijungus (apribotos funkcijos)", "Naujo skaitytojo registracija", "Išeiti"]
choice = st.sidebar.selectbox("Pasirinkite", menu)

col1, col2 = st.columns(2)
with col1:
    st.title("C51 BIBLIOTEKOS SISTEMA")

with col2:
    if st.button("Išeiti iš sistemos"):
        st.write("Išeiti")

if choice == "Prisijungimas bibliotekininkui":
    st.subheader("Bibliotekininko prisijungimas")
    librarian_username = st.text_input("Naudotojo vardas", key="librarian_username")
    librarian_password = st.text_input("Slaptažodis", type='password', key="librarian_password")
    if st.button("Prisijungti"):
        if librarian.username_password_verification(librarian_username, librarian_password):
            st.success(f"Sveiki prisijungę, {librarian_username}!")
        else:
            st.error("Neteisingas naudotojo vardas arba slaptažodis!")

if choice == "Prisijungimas lankytojui":
    st.subheader("Bibliotekos lankytojo prisijungimas")
    reader_username = st.text_input("Naudotojo vardas", key="reader_username")
    reader_password = st.text_input("Slaptažodis", type='password', key="reader_password")
    if st.button("Prisijungti", key="reader_login_button"):
        if reader.username_password_verification(reader_username, reader_password):
            st.success(f"Sveiki prisijungę, {reader_username}!")
        else:
            st.error("Neteisingas naudotojo vardas arba slaptažodis!")

if choice == "Dirbti neprisijungus (apribotos funkcijos)":
    pass

if choice == "Naujo skaitytojo registracija":
    st.subheader("Naujo skaitytojo registracija")
    reader_name = st.text_input("Vardas", key="new_reader_name")
    reader_last_name = st.text_input("Pavardė", key="new_reader_lastname")
    reader_email = st.text_input("El. paštas", key="new_reader_email")
    reader_phone = st.text_input("Telefono numeris", help="Įveskite numerį be +370", key="new_reader_phone")
    
    if st.button("Registruotis", key="register_button"):
        if not reader_name.isalpha() or not reader_last_name.isalpha():
            st.error("Vardą ir pavardę turi sudaryti tik raidės!")
        elif not reader_registration.is_valid_email(reader_email):
            st.error("Neteisingas el. pašto formatas!")
        elif not reader_registration.is_valid_phone(reader_phone):
            st.error("Neteisingas telefono numeris! Numeris turi būti 8 skaitmenų, prasidedantis 6.")
        else:
            reader_card_number = reader_registration.reader_card_number_generator()
            reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, "+370" + reader_phone, reader_card_number)
            st.success(f"Sėkmingai užregistruotas {reader_name} {reader_last_name}. Kortelės numeris: {reader_card_number}")
            
            
# while True:
#     print("-" * 50)
#     print("C51 BIBLIOTEKOS SISTEMA")
#     print("-" * 50)
#     print("1. Prisijungimas bibliotekininkui.")
#     print("2. Prisijungimas bibliotekos lankytojui.")
#     print("3. Dirbti neprisijungus (apribotos funkcijos).")
#     print("4. Naujo skaitytojo registracija.")
#     print("5. Išeiti iš programos.")
#     print("-" * 50)
#     try:
#         choose_1_level = int(input("Įveskite savo pasirinkimą (1 - 5):\n"))
#         if choose_1_level == 1:
#             print("-" * 50)
#             print("C51 BIBLIOTEKOS SISTEMA")
#             print("-" * 50)
#             print("Norėdami prisijungti prie darbuotojo aplinkos, įveskite savo duomenis")
#             print("-" * 50)
#             librarian_login_user_name = input("Įveskite naudotojo vardą:\n ")
#             if librarian_login_user_name in passwords:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("-" * 50)
#                 librarian_login_password = input("Įveskite slaptažodį:\n ")
#                 if librarian_login_password in passwords:
#                     print("-" * 50)
#                     print("C51 BIBLIOTEKOS SISTEMA")
#                     print("-" * 50)
#                     print(f"Sveiki prisijungę {librarian_login_user_name}!")
#                 else:
#                     print("Neteisingas slaptažodis!")
#                     continue
#             else:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("-" * 50)
#                 print(f'"{librarian_login_user_name}" vartotojo nėra!')
#                 continue
#         elif choose_1_level == 2:
#             print("-" * 50)
#             print("C51 BIBLIOTEKOS SISTEMA")
#             print("-" * 50)
#             print("Norėdami prisijungti prie lankytojo aplinkos, įveskite savo duomenis")
#             print("-" * 50)
#             reader_login_user_name = input("Įveskite naudotojo vardą:\n ")
#             if reader_login_user_name in passwords:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("-" * 50)
#                 reader_login_password = input("Įveskite slaptažodį:\n ")
#                 if reader_login_password in passwords:
#                     print("-" * 50)
#                     print("C51 BIBLIOTEKOS SISTEMA")
#                     print("-" * 50)
#                     print(f"Sveiki prisijungę {reader_login_user_name}!")
#                 else:
#                     print("Neteisingas slaptažodis!")
#                     continue
#             else:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("-" * 50)
#                 print(f'"{reader_login_user_name}" vartotojo nėra!')
#                 continue
#         elif choose_1_level == 3:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("-" * 50)
#                 print("Darbas su apribotomis funkcijomis. Be registracijos galite:")
#                 print("1. Peržiūrėti leidinių sąrašą;")
#                 print("2. Ieškoti leidinių.")
#                 print("3. Grįžti į pagrindinį langą.")
#                 print("4. Išeiti iš programos.")
#                 anonymous_choose = int(input("Pasirinkite 1-4:\n"))
#         elif choose_1_level == 4:
#             while True:
#                 print("-" * 50)
#                 print("C51 BIBLIOTEKOS SISTEMA")
#                 print("NAUJO SKAITYTOJO REGISTRACIJA")
#                 print("-" * 50)
#                 reader_name = input("Įveskite savo vardą:\n").strip().title()
#                 if not reader_name.isalpha():
#                     print(f"Vardą turi sudaryti tik raidės. Jūsų įvestas vardas {reader_name} yra netinkamas.")
#                     continue
#                 reader_last_name = input("Įveskite savo pavardę:\n").strip().title()
#                 if not reader_last_name.isalpha():
#                     print(f"Pavardę turi sudaryti tik raidės. Jūsų įvesta pavardė {reader_last_name} yra netinkama.")
#                     continue
#                 reader_email = input("Įveskite savo el. pašto adresą:\n")
#                 if not reader_registration.is_valid_email(reader_email):
#                     print(f"Jūsų įvestas el. pašto adresas {reader_email} neatitinka reikalavimų.")
#                     continue
#                 while True:
#                     reader_phone = input("Įveskite savo telefono numerį: +370")
#                     if not reader_registration.is_valid_phone(reader_phone):
#                         print(f"Klaida! Patikrinkite telefono numerį. Jūsų įvestas numeris:\n{reader_phone}")
#                     else:
#                         reader_phone = "+370" + reader_phone
#                         break
#                 print(f"Registracija sėkminga. Jūsų duomenys:\n {reader_name} {reader_last_name},\n Telefono numeris: {reader_phone}\n Email: {reader_email}")
#                 print(f"Jūsų skaitytojo kortelės numeris: {reader_registration.reader_card_number_generator()}")
#                 reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, reader_phone, reader_registration.reader_card_number_generator())
#                 break
            
#         elif choose_1_level == 5:
#             print("Išeinama iš programos!")
#             break
#     except ValueError:
#         print("Reikšmė turi būti 1-5")
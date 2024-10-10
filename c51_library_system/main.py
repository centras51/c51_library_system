import pandas as pd
import datetime as dt
import streamlit as st
import getpass
import re
import random


class Librarian:
    def __init__(self) -> None:
        pass

    def username_password_verification(self):
        pass

class Reader:
    def __init__(self) -> None:
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

reader_registration = ReaderRegistration()

while True:
    print("-" * 50)
    print("C51 BIBLIOTEKOS SISTEMA")
    print("-" * 50)
    print("1. Prisijungimas bibliotekininkui.")
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
            if librarian_login_user_name in passwords:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                librarian_login_password = input("Įveskite slaptažodį:\n ")
                if librarian_login_password in passwords:
                    print("-" * 50)
                    print("C51 BIBLIOTEKOS SISTEMA")
                    print("-" * 50)
                    print(f"Sveiki prisijungę {librarian_login_user_name}!")
                else:
                    print("Neteisingas slaptažodis!")
                    continue
            else:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                print(f'"{librarian_login_user_name}" vartotojo nėra!')
                continue
        elif choose_1_level == 2:
            print("-" * 50)
            print("C51 BIBLIOTEKOS SISTEMA")
            print("-" * 50)
            print("Norėdami prisijungti prie lankytojo aplinkos, įveskite savo duomenis")
            print("-" * 50)
            reader_login_user_name = input("Įveskite naudotojo vardą:\n ")
            if reader_login_user_name in passwords:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                reader_login_password = input("Įveskite slaptažodį:\n ")
                if reader_login_password in passwords:
                    print("-" * 50)
                    print("C51 BIBLIOTEKOS SISTEMA")
                    print("-" * 50)
                    print(f"Sveiki prisijungę {reader_login_user_name}!")
                else:
                    print("Neteisingas slaptažodis!")
                    continue
            else:
                print("-" * 50)
                print("C51 BIBLIOTEKOS SISTEMA")
                print("-" * 50)
                print(f'"{reader_login_user_name}" vartotojo nėra!')
                continue
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
                    reader_phone = input("Įveskite savo telefono numerį: +370")
                    if not reader_registration.is_valid_phone(reader_phone):
                        print(f"Klaida! Patikrinkite telefono numerį. Jūsų įvestas numeris:\n{reader_phone}")
                    else:
                        reader_phone = "+370" + reader_phone
                        break
                print(f"Registracija sėkminga. Jūsų duomenys:\n {reader_name} {reader_last_name},\n Telefono numeris: {reader_phone}\n Email: {reader_email}")
                print(f"Jūsų skaitytojo kortelės numeris: {reader_registration.reader_card_number_generator()}")
                reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, reader_phone, reader_registration.reader_card_number_generator())
                break
            
        elif choose_1_level == 5:
            print("Išeinama iš programos!")
            break
    except ValueError:
        print("Reikšmė turi būti 1-5")
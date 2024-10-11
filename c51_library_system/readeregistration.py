import random
import pandas as pd
import re

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
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        existing_reader_card_numbers = reader_df['skaitytojo_kortele'].to_list()
        while True:
            if self.reader_card_number not in existing_reader_card_numbers:
                return self.reader_card_number
    
    def save_reader_datas(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number):
        new_reader_line = {'vardas': reader_name, 'pavarde': reader_last_name, 'email': reader_email, 'telefonas': reader_phone, 'skaitytojo_kortele': reader_card_number}
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv", index=False, encoding='utf-8')
        
    def save_reader_password(self, reader_name, reader_last_name, reader_email, reader_phone, reader_card_number, new_username, new_password):
        new_reader_line = {'vardas': reader_name, 'pavarde': reader_last_name, 'email': reader_email, 'telefonas': reader_phone, 'skaitytojo_kortele': reader_card_number, 'username': new_username, 'password': new_password}
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv")
        reader_df = pd.concat([reader_df, pd.DataFrame([new_reader_line])], ignore_index=True)
        reader_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\passwords_db.csv", index=False, encoding='utf-8')
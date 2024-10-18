import pandas as pd
import random
import string


class Generator:
    def reader_card_number_generator(self):
        reader_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
        existing_reader_card_numbers = reader_df['skaitytojo_kortele'].to_list()
        while True:
            reader_card_number = random.randint(10000000, 99999999)
            if reader_card_number not in existing_reader_card_numbers:
                return reader_card_number
            
    def generate_username_password(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return username, password
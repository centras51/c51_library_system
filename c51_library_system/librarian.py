import pandas as pd

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
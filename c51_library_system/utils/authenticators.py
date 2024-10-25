import sqlite3


class Authenticator:
    def __init__(self, db_path="D:\\CodeAcademy\\c51_library_system\\data_bases\\library_db.db"):
        self.db_path = db_path
    
    def username_password_verification(self, reader_username, reader_password):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            
            cursor.execute("SELECT password_ FROM readers WHERE username = ?", (reader_username,))
            result = cursor.fetchone()

            if result and result[0] == reader_password:
                return True  
            else:
                return False  
        except sqlite3.Error as e:
            print(f"Duomenų bazės klaida: {e}")
            return False
        finally:
            if connection:
                connection.close()

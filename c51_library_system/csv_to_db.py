import pandas as pd
import sqlite3

csv_file_path = "D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv"

connection = sqlite3.connect("librarians_db.db")
cur = connection.cursor()

df = pd.read_csv(csv_file_path)

cur.execute("""CREATE TABLE IF NOT EXISTS librarians (
        bibliotekininko_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vardas TEXT,
        pavarde TEXT,
        email TEXT,
        telefonas TEXT,
        username TEXT,
        password_ TEXT
    )
""")

df.to_sql('librarians', connection, if_exists='append', index=False)

connection.commit()
connection.close()

print("CSV duomenys sėkmingai perkelti į duomenų bazę.")

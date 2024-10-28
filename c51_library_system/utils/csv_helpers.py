import pandas as pd
import os


CSV_PATH_READERS = "D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv"

class CsvProcessor:
    def read_readers_csv():
        if os.path.exists(CSV_PATH_READERS):
            return pd.read_csv(CSV_PATH_READERS)
        else:
            raise FileNotFoundError(f"CSV failas nerastas: {CSV_PATH_READERS}")
        
    def write_reader_csv(dataframe):
        dataframe.to_csv(CSV_PATH_READERS, index=False, encoding='utf-8')
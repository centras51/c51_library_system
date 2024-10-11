import pandas as pd
import streamlit as st
from readeregistration import ReaderRegistration
 

class Librarian:
    def __init__(self) -> None:
        pass

    def username_password_verification(self, username, password):
        usr_psw_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
        user_info = usr_psw_df.loc[usr_psw_df['username'] == username]
        if not user_info.empty:
            return user_info['password'].values[0] == password
        return False
    
    def show_books(self):
        try:
            books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
            books_per_page = 50
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 0
            total_pages = (len(books_df) // books_per_page) + (1 if len(books_df) % books_per_page > 0 else 0)

            start_idx = st.session_state.current_page * books_per_page
            end_idx = start_idx + books_per_page
            current_books = books_df.iloc[start_idx:end_idx]
            
            st.dataframe(current_books, use_container_width=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("Atgal", disabled=st.session_state.current_page == 0):
                    st.session_state.current_page -= 1
                    
            with col2:
                st.write(f"Puslapis {st.session_state.current_page + 1} iš {total_pages}")
                
            with col3:
                if st.button("Kitas", disabled=st.session_state.current_page >= total_pages - 1):
                    st.session_state.current_page += 1
                    
        except FileNotFoundError:
            st.error("Knygų sąrašas nerastas.")

    def show_readers(self):
        try:
            readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
            return readers_df
        except FileNotFoundError:
            st.error("Skaitytojų sąrašas nerastas.")

    def find_reader(self):
        if 'search_query' not in st.session_state:
            st.session_state.search_query = ''
        search_query = st.text_input("Įveskite skaitytojo vardą, pavardę, skaitytojo kortelės numerį, email'ą arba telefoną", 
                                    value=st.session_state.search_query)

        if st.button("Rasti skaitytoją", key="search_readers"):
            st.session_state.search_query = search_query
            
            try:
                readers_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\readers_db.csv")
                search_results = readers_df[
                    readers_df['vardas'].str.contains(search_query, case=False, na=False) | 
                    readers_df['pavardė'].str.contains(search_query, case=False, na=False) |
                    readers_df['skaitytojo_kortelės_numeris'].astype(str).str.contains(search_query, case=False, na=False) |
                    readers_df['telefonas'].astype(str).str.contains(search_query, case=False, na=False) |
                    readers_df['email'].str.contains(search_query, case=False, na=False)
                ]
                if not search_results.empty:
                    st.write("Rasti skaitytojai:")
                    st.dataframe(search_results, use_container_width=True)
                else:
                    st.info("Pagal jūsų užklausą skaitytojas nerastas.")
                    
            except FileNotFoundError:
                st.error("Skaitytojų sąrašas nerastas.")

    def add_reader(self):
        ReaderRegistration()

    def find_book(self):
        books_df = self.show_books()
        if books_df is not None:
            st.write(books_df)
        search_query = st.text_input("Įveskite knygos pavadinimą")
        if st.button("Ieškoti", key="search_books"):
            search_results = books_df[books_df['knygos_pavadinimas'].str.contains(search_query, case=False, na=False)]
        if not search_results.empty:
            st.write(search_results)
        else:
            st.info("Pagal jūsų užklausą knygų nerasta.")
            
    def find_author(self):
        books_df = self.show_books()
        if books_df is not None:
            st.write(books_df)
        search_query = st.text_input("Įveskite autorių")
        if st.button("Ieškoti", key="search_author"):
            search_results = books_df[books_df['autorius'].str.contains(search_query, case=False, na=False)]
        if not search_results.empty:
            st.write(search_results)
        else:
            st.info("Pagal jūsų užklausą rašytojo nerasta.")


    def remove_book(self, value_del=None, criterion="ISBN"):
        books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        if books_df is not None:
            st.write(books_df)
            value_del = st.text_input("Įveskite ISBN numerį", value=value_del)
            if st.button("Ištrinti knygą", key="delete_book"):
                if not value_del.isnumeric():
                    st.error("ISBN numerį sudaro tik skaičiai")
                else:
                    books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
                    books_df_filtered = books_df[books_df[criterion] != value_del]

                    if len(books_df_filtered) == len(books_df):
                        st.warning(f"Knyga su ISBN {value_del} nerasta.")
                    else:
                        books_df_filtered.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding="UTF-8")
                        st.success(f"Knyga su ISBN {value_del} sėkmingai ištrinta.")
                        print(f"Knyga ISBN {value_del} buvo ištrinta.")
        else:
            st.info("Nėra knygos duomenų.")
            
    def add_book(self, book_author, book_title, book_release_date, book_isbn, book_genre, book_about):
        st.subheader("Pridėti naują knygą")
        book_author = st.text_input("Knygos autorius", key="autorius")
        book_title = st.text_input("Knygos pavadinimas", key="knygos_pavadinimas")
        book_release_date = st.text_input("Knygos išleidimo metai", key="metai")
        book_isbn = st.text_input("Knygos ISBN", key="ISBN")
        book_genre = st.text_input("Knygos žanras", key="zanras")
        book_about = st.text_area("Pastabos apie knygą", key="pastabos")
        if st.button("Patvirtinti pridėjimą"):
            st.success(f"Knyga '{book_title}' sėkmingai pridėta!")
        new_book = {'autorius': book_author, 'knygos_pavadinimas': book_title, 'metai': book_release_date, 'ISBN': book_isbn, 'zanras': book_genre, 'pastabos': book_about}
        books_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv")
        books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
        books_df.to_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\books_db.csv", index=False, encoding='utf-8')
        
    def show_librarians(self):
        try:
            librarians_df = pd.read_csv("D:\\CodeAcademy\\c51_library_system\\CSVs\\librarians_db.csv")
            selected_columns = librarians_df[['vardas', 'pavarde', 'email', 'telefonas']]
            st.dataframe(selected_columns, use_container_width=True)
        except FileNotFoundError:
            st.error("Darbuotojų sąrašas nerastas.")
        
        

        

import pandas as pd
import datetime as dt
import streamlit as st
import getpass
import re
from readeregistration import ReaderRegistration
from librarian import Librarian
from reader import Reader

st.set_page_config(layout="wide")

# Inicializuojame sesijos būseną
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def navigate(page):
    st.session_state.page = page

# Inicializuojame objektus
reader_registration = ReaderRegistration()
librarian = Librarian()
reader = Reader()

# Prisijungimo puslapis
if st.session_state.page == 'login':
    st.title("C51 BIBLIOTEKOS SISTEMA")
    
    # Meniu rodymas tik prisijungimo puslapyje
    st.subheader("Pasirinkite veiksmą:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Prisijungimas bibliotekininkui"):
            st.session_state.page = 'librarian_login'
    with col2:
        if st.button("Prisijungimas lankytojui"):
            st.session_state.page = 'reader_login'
    with col3:
        if st.button("Dirbti neprisijungus (apribotos funkcijos)"):
            navigate('anonymous_environment')
    
    if st.button("Naujo skaitytojo registracija"):
        navigate('reader_registration')
    if st.button("Išeiti"):
        st.write("Išeinama iš programos...")
        st.stop()

# Bibliotekininko prisijungimas
elif st.session_state.page == 'librarian_login':
    st.subheader("Bibliotekininko prisijungimas")
    librarian_username = st.text_input("Naudotojo vardas")
    librarian_password = st.text_input("Slaptažodis", type='password')
    if st.button("Prisijungti"):
        if librarian.username_password_verification(librarian_username, librarian_password):
            st.success(f"Sveiki prisijungę, {librarian_username}!")
            st.session_state['librarian_username'] = librarian_username  # Išsaugome vartotojo vardą
            navigate('librarian_environment')
        else:
            st.error("Neteisingas naudotojo vardas arba slaptažodis!")
    if st.button("Grįžti"):
        navigate('login')

# Skaitytojo prisijungimas
elif st.session_state.page == 'reader_login':
    st.subheader("Bibliotekos lankytojo prisijungimas")
    reader_username = st.text_input("Naudotojo vardas", key="reader_username")
    reader_password = st.text_input("Slaptažodis", type='password', key="reader_password")
    if st.button("Prisijungti", key="reader_login_button"):
        if reader.username_password_verification(reader_username, reader_password):
            st.success(f"Sveiki prisijungę, {reader_username}!")
            st.session_state['reader_username'] = reader_username  # Išsaugome vartotojo vardą
            navigate('reader_environment')
        else:
            st.error("Neteisingas naudotojo vardas arba slaptažodis!")
    if st.button("Grįžti"):
        navigate('login')

# Bibliotekininko aplinka
elif st.session_state.page == 'librarian_environment':
    st.title("Bibliotekos valdymas")
    st.write(f"Bibliotekininko vardas: {st.session_state.get('librarian_username')}")

    st.subheader("Knygų bazė")
    if st.button("Rodyti knygas"):
        books_df = librarian.show_books()
        st.dataframe(books_df, use_container_width=True)
        
    if st.button("Knygų paieška"):
        librarian.find_book()
        
    if st.button("Autoriaus paieška"):
        librarian.find_author()

    if st.button("Pridėti knygą"):
        librarian.add_book()

    if st.button("Nurašyti knygas"):
        librarian.remove_book()

    st.subheader("Skaitytojų bazė")
    if st.button("Atidaryti skaitytojų bazę"):
        readers_df = librarian.show_readers()
        if readers_df is not None:
            st.write(readers_df)
        else:
            st.info("Nėra skaitytojų duomenų.")

    if st.button("Paieška skaitytojų bazėje"):
       librarian.find_reader()

    if st.button("Pridėti naują skaitytoją"):
        st.subheader("Naujo skaitytojo registracija")
        reader_name = st.text_input("Vardas", key="name").title()
        reader_last_name = st.text_input("Pavardė", key="lastname").title()
        reader_email = st.text_input("El. paštas", key="email").lower()
        reader_phone = st.text_input("Telefono numeris +370", help="Įveskite numerį be +370", key="phone")

        if st.button("Registruoti", key="register_reader"):
            if not reader_name.isalpha() or not reader_last_name.isalpha():
                st.error("Vardą ir pavardę turi sudaryti tik raidės!")
            elif not reader_registration.is_valid_email(reader_email):
                st.error("Neteisingas el. pašto formatas!")
            elif not reader_registration.is_valid_phone(reader_phone):
                st.error("Neteisingas telefono numeris! Numeris turi būti 8 skaitmenų, prasidedantis 6.")
            else:
                reader_card_number = reader_registration.reader_card_number_generator()
                reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, "+370" + reader_phone, reader_card_number)
                st.success(f"Sėkmingai užregistruotas naujas skaitytojas: {reader_name} {reader_last_name}. Skaitytojo kortelės numeris: {reader_card_number}")

    st.subheader("Valdymo skiltis")
    if st.button("Bibliotekos darbuotojai"):
        librarian.show_librarians()
    
    if st.button("Atsijungti"):
        st.session_state.page = 'login'
        st.session_state.pop('librarian_username', None)
        st.experimental_rerun()

    if st.button("Išeiti iš programos"):
        st.write("Išeinama iš programos...")
        st.stop()

# Skaitytojo aplinka
elif st.session_state.page == 'reader_environment':
    st.title("Bibliotekos lankytojo aplinka")
    st.write(f"Sveiki, {st.session_state.get('reader_username')}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Peržiūrėti knygas"):
            books_df = reader.show_books()
            if books_df is not None:
                st.write(books_df)
            else:
                st.info("Nėra knygų duomenų.")

        if st.button("Ieškoti knygos"):
            search_query = st.text_input("Įveskite paieškos užklausą")
            if st.button("Ieškoti", key="search_books_reader"):
                search_results = reader.search_books(search_query)
                if not search_results.empty:
                    st.write(search_results)
                else:
                    st.info("Pagal jūsų užklausą knygų nerasta.")

    with col2:
        if st.button("Atsijungti"):
            st.session_state.page = 'login'
            st.session_state.pop('reader_username', None)
            st.experimental_rerun()

        if st.button("Išeiti iš programos"):
            st.write("Išeinama iš programos...")
            st.stop()

# Anoniminė aplinka
elif st.session_state.page == 'anonymous_environment':
    st.title("Peržiūra be registracijos")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Peržiūrėti knygas"):
            books_df = reader.show_books()
            if books_df is not None:
                st.write(books_df)
            else:
                st.info("Nėra knygų duomenų.")

        if st.button("Ieškoti knygos"):
            search_query = st.text_input("Įveskite paieškos užklausą")
            if st.button("Ieškoti", key="search_books_anonymous"):
                search_results = reader.search_books(search_query)
                if not search_results.empty:
                    st.write(search_results)
                else:
                    st.info("Pagal jūsų užklausą knygų nerasta.")

    with col2:
        if st.button("Grįžti į prisijungimo langą"):
            st.session_state.page = 'login'
            st.experimental_rerun()

        if st.button("Išeiti iš programos"):
            st.write("Išeinama iš programos...")
            st.stop()

# Naujo skaitytojo registracija
elif st.session_state.page == 'reader_registration':
    st.title("Naujo skaitytojo registracija")
    reader_name = st.text_input("Vardas", key="name").title()
    reader_last_name = st.text_input("Pavardė", key="lastname").title()
    reader_email = st.text_input("El. paštas", key="email").lower()
    reader_phone = st.text_input("Telefono numeris +370", help="Įveskite numerį be +370", key="phone")
    new_username = st.text_input("Jūsų prisijungimo vardas", help="Sugalvokite ir įveskite savo prisijungimo vardą", key="username")
    new_password = st.text_input("Jūsų slaptažodis", type="password", help="Įveskite slaptažodį", key="password")
    new_password2 = st.text_input("Pakartokite slaptažodį", type="password", help="Pakartokite slaptažodį", key="password1")

    if st.button("Registruotis", key="register_button"):
        if not reader_name.isalpha() or not reader_last_name.isalpha():
            st.error("Vardą ir pavardę turi sudaryti tik raidės!")
        elif not reader_registration.is_valid_email(reader_email):
            st.error("Neteisingas el. pašto formatas!")
        elif not reader_registration.is_valid_phone(reader_phone):
            st.error("Neteisingas telefono numeris! Numeris turi būti 8 skaitmenų, prasidedantis 6.")
        elif new_password != new_password2:
            st.error("Slaptažodžiai nesutampa.")
        else:
            reader_card_number = reader_registration.reader_card_number_generator()
            reader_registration.save_reader_datas(reader_name, reader_last_name, reader_email, "+370" + reader_phone, reader_card_number)
            reader_registration.save_reader_password(reader_name, reader_last_name, reader_email, "+370" + reader_phone, reader_card_number, new_username, new_password)
            st.success(f"Sėkmingai užregistruotas {reader_name} {reader_last_name}. Jūsų skaitytojo kortelės numeris: {reader_card_number}")
            st.info("Dabar galite prisijungti naudodami savo prisijungimo vardą ir slaptažodį.")
            st.session_state.page = 'login'
            st.experimental_rerun()
    if st.button("Grįžti"):
        navigate('login')


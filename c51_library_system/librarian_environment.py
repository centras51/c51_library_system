import streamlit as st
from librarian import Librarian
from c51_library_system.readerregistration import ReaderRegistration

def librarian_environment():
    st.title("Bibliotekos valdymas")
    librarian = Librarian()
    reader_registration = ReaderRegistration() 
    
    if 'librarian_username' in st.session_state:
        st.write(f"Bibliotekininko vardas: {st.session_state.get('librarian_username')}")

        with st.sidebar:
            if st.button("Atsijungti"):
                st.session_state.page = 'login'
                st.session_state.pop('librarian_username', None)
                st.experimental_rerun()
            if st.button("Išeiti iš programos"):
                st.write("Išeinama iš programos...")
                st.stop()

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
            reader_registration.add_reader()
    else:
        st.error("Prisijunkite, kad galėtumėte naudotis valdymo aplinka.")

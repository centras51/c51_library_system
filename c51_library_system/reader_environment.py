import streamlit as st
from reader import Reader

def reader_environment():
    st.title("Bibliotekos lankytojo aplinka")
    reader = Reader()
    
    if 'reader_username' in st.session_state:
        st.write(f"Sveiki, {st.session_state.get('reader_username')}")

        with st.sidebar:
            if st.button("Atsijungti"):
                st.session_state.page = 'login'
                st.session_state.pop('reader_username', None)
                st.experimental_rerun()
            if st.button("Išeiti iš programos"):
                st.write("Išeinama iš programos...")
                st.stop()

        if st.button("Peržiūrėti knygas"):
            books_df = reader.show_books()
            if books_df is not None:
                st.write(books_df)
            else:
                st.info("Nėra knygų duomenų.")

        if st.button("Ieškoti knygos"):
            search_query = st.text_input("Įveskite paieškos užklausą")
            if st.button("Ieškoti"):
                search_results = reader.search_books(search_query)
                if not search_results.empty:
                    st.write(search_results)
                else:
                    st.info("Pagal jūsų užklausą knygų nerasta.")
    else:
        st.error("Prisijunkite, kad galėtumėte naudotis lankytojo aplinka.")
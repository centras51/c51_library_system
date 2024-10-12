import streamlit as st
from reader import Reader

def anonymous_environment():
    st.title("Peržiūra be registracijos")
    reader = Reader()

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

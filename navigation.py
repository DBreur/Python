import streamlit as st

pg = st.navigation([
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/dashboard.py", title="Dashboard"),
    st.Page("pages/lyfta.py", title="Lyfta"),
    st.Page("pages/sambo.py", title="Sambo log")
])

pg.run()

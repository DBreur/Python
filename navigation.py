import streamlit as st

pg = st.navigation([
    # st.Page("main.py", title="Home"),
    st.Page("pages/dashboard.py", title="dashboard"),
    st.Page("pages/mettst.py", title="tst")
])

pg.run()

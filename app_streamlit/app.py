import streamlit as st

## Pages management
page_main = st.Page("pages/main.py", title="Calculateur")
page_methodo = st.Page("pages/methodo.py", title="Méthodologie")

pg = st.navigation([
  page_main,
  page_methodo,
])
pg.run()

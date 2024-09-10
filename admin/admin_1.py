import streamlit as st
from MyApp import mysheet

st.header("Admin 1")
st.write(f"Você está logado como {st.session_state['role']}.")

#rows = run_query("SELECT * from table1;")

conn, rows = mysheet()

placeholder = st.empty()
with placeholder.container(border=True):
   st.markdown("### Listagem de Usuários")
   st.table(rows)
import streamlit as st
from MyApp import mysheet, selectall, conn

st.header("Admin 1")
st.write(f"Você está logado como {st.session_state['role']}.")

lista_usuarios = selectall(conn, "usuarios")

placeholder = st.empty()
with placeholder.container(border=True):
   st.markdown("### Listagem de Usuários")
   st.table(lista_usuarios)
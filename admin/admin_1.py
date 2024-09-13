import streamlit as st
from utils import lista_usuarios

st.header("Admin 1")
st.write(f"Você está logado como {st.session_state['role']}.")

placeholder = st.empty()
with placeholder.container(border=True):
   st.markdown("### Listagem de Usuários")
   st.table(lista_usuarios)
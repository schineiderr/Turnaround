import streamlit as st
from MyApp import mysheet, conn

st.header("Acompanhe seu Desenvolvimento")
user = st.session_state["user"]
st.write("Você está logado como: ", user)


lista_desenvolvimentos = conn.query(f"SELECT * FROM forms WHERE email = '{user}'")
lista_id_forms = list(lista_desenvolvimentos["id"])
lista_tarefas = conn.query(f"SELECT * FROM tasks WHERE id_forms IN {lista_id_forms}")

st.write("Projetos")
st.write(lista_desenvolvimentos)

st.write("Tarefas")
st.write(lista_tarefas)
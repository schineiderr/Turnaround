import streamlit as st
from project.utils import get_forms, get_tasks

st.header("Acompanhe seu Desenvolvimento")
user = st.session_state["user"]
st.write("Você está logado como: ", user)

df_forms = get_forms()
#df_forms = lista_forms
df_tasks = get_tasks()
#df_tasks = lista_tasks

lista_desenvolvimentos = df_forms.query("email == @user")
lista_id_forms = list(lista_desenvolvimentos["id"])

lista_tarefas = df_tasks.query("id_forms in @lista_id_forms")

st.subheader("Projetos")
st.write(lista_desenvolvimentos)

st.subheader("Tarefas")
st.write(lista_tarefas)
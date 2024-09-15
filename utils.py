""" Util functions for app

"""
import streamlit as st
import time
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
@st.cache_resource
def mysheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn

conn = mysheet()

@st.cache_data
def get_contracts():
    lista_contratos = conn.query(f"SELECT * FROM contratos")
    return lista_contratos

@st.cache_data
def get_tasks():
    lista_tarefas = conn.query(f"SELECT * FROM tasks")
    return lista_tarefas

@st.cache_data
def get_forms():
    lista_projetos = conn.query(f"SELECT * FROM forms")
    return lista_projetos

@st.cache_data
def get_users():
    lista_usuarios = conn.query(f"SELECT * FROM usuarios")
    return lista_usuarios

@st.cache_data
def get_role(user, lista_usuarios):
    for row in lista_usuarios.itertuples():
        if row.user == user:
            role = row.permission
            break
        else:
            role = False
    return role

lista_usuarios = get_users()

def login():
    st.header("Login")
    user = st.text_input("E-mail:")
    role = get_role(user, lista_usuarios)
    col1, col2 = st.columns([1,8])
    if col1.button("Login"):
        if not role:
            st.error("Usuário não encontrado!")
        else:
            st.session_state["role"] = role
            st.session_state["user"] = user
            st.rerun()
    if col2.button("Cadastrar"):
        st.session_state["role"] = "Cadastrar"
        st.rerun()

def new_user():
    st.write("Faça seu cadastro: ")
    email = st.text_input("Email: ")
    col1, col2 = st.columns([1,6])
    submit_button = col1.button("Cadastrar")
    back_button = col2.button("Voltar")
    if submit_button:
        try:
            current_table = conn.query("SELECT * FROM usuarios")
            actual_update = pd.DataFrame({"user": [email], "permission": ['Solicitante']})
            aux = pd.concat([current_table, actual_update], ignore_index=True)
            df = conn.update(worksheet="usuarios",data=aux)
            st.success("Usuário cadastrado com sucesso!")
            st.session_state["role"] = "Solicitante"
            st.session_state["user"] = email
            st.cache_data.clear()
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error("Usuário Negado")
            st.write(e)
            time.sleep(3)
    if back_button:
        st.session_state["role"] = None
        st.rerun()

def generate_tasks(conn, id_form, solicitacao):
    current_table = get_tasks()
    id = max(current_table['id_task'])
    if solicitacao == "Novo Desenvolvimento":
        tasks = ["Reunião de Entendimento", "Elaboração de Proposta", "Desenvolvimento"]
    elif solicitacao == "Conheci a solução e quero em meu contrato":
        tasks = ["Avaliar Solicitação", "Implementar Desenvolvimento", "Validar"]
    elif solicitacao == "Melhorias ou Ajustes em Desenvolvimento Entregue":
        tasks = ["Avaliar Solicitação", "Realizar Melhorias ou Ajustes", "Validar"]
    actual_update = pd.DataFrame.from_dict({
        "id_forms": [id_form, id_form, id_form],
        "id_task": [id+1, id+2, id+3],
        "task": tasks,
        "start_date": ["", "", ""],
        "due_date": ["", "", ""],
        "end_date": ["", "", ""],
        "bucket": ["Backlog", "Backlog", "Backlog"],
        "description": ["", "", ""],
        "responsible": ["", "", ""]})
    aux = pd.concat([current_table, actual_update], ignore_index=False)
    new_table = conn.update(worksheet="tasks",data=aux)
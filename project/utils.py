""" Util functions for app

"""
import streamlit as st
import time
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import hashlib

def my_hash(pwd):
    pwd = pwd.encode('utf-8')
    hash_obj = hashlib.sha256(pwd)
    hex_hash = hash_obj.hexdigest()
    return hex_hash

#Create a connection object.
@st.cache_resource
def mysheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn 

conn = mysheet()

@st.cache_data
def get_contracts():
    #lista_contratos = conn.query(f"SELECT * FROM contratos")
    lista_contratos = conn.read(worksheet="contratos")
    return lista_contratos

@st.cache_data
def get_tasks():
    #lista_tarefas = conn.query(f"SELECT * FROM tasks")
    lista_tarefas = conn.read(worksheet="tasks")
    return lista_tarefas

@st.cache_data
def get_forms():
    #lista_projetos = conn.query(f"SELECT * FROM forms")
    lista_projetos = conn.read(worksheet="forms")
    return lista_projetos

@st.cache_data
def get_users():
    #lista_usuarios = conn.query(f"SELECT * FROM usuarios")
    lista_usuarios = conn.read(worksheet="usuarios")
    return lista_usuarios

@st.cache_data
def get_role(user, lista_usuarios):
    for row in lista_usuarios.itertuples():
        if row.user == user:
            role = row.permission
            user_pwd = row.password
            break
        else:
            role = False
            user_pwd = False
    return role, user_pwd

lista_usuarios = get_users()

def login():
    st.header("Login")
    user = st.text_input("E-mail:")
    pwd = st.text_input("Senha:", type="password")
    col1, col2 = st.columns([1,8])
    if col1.button("Login"):
        role, user_pwd = get_role(user, lista_usuarios)
        if not role:
            st.error("Usuário não encontrado!")
        else:
            hash_pwd = my_hash(pwd)
            if user_pwd == hash_pwd:
                st.session_state["role"] = role
                st.session_state["user"] = user
                st.rerun()
            else:
                 st.error("Senha incorreta!")
    if col2.button("Cadastrar"):
        st.session_state["role"] = "Cadastrar"
        st.rerun()

def new_user():
    st.write("Faça seu cadastro: ")
    email = st.text_input("Email: ")
    name = st.text_input("Nome: ")
    pwd = st.text_input("Senha: ", type="password")
    col1, col2 = st.columns([1,6])
    submit_button = col1.button("Cadastrar")
    back_button = col2.button("Voltar")
    if submit_button:
        try:
            current_table = get_users()
            actual_update = pd.DataFrame({"user": [email],
                                          "name": [name],
                                          "permission": ['Solicitante'],
                                          "contract": [""],
                                          "password": [my_hash(pwd)]})
            aux = pd.concat([current_table, actual_update], ignore_index=True)
            #lista_usuarios = pd.concat([lista_usuarios, actual_update], ignore_index=True)
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

def generate_tasks(id_form, solicitacao):
    current_table = get_tasks()
    #current_table = lista_tasks
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
    #lista_tasks = pd.concat([current_table, actual_update], ignore_index=False)
    new_table = conn.update(worksheet="tasks",data=aux)
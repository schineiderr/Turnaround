import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

#rows = [("samuel.bucher@timenow.com.br", "Admin"), ("rychard.malfer@timenow.com.br", "Solicitante")]

# Create a connection object.
def mysheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    rows = conn.read()
    return conn, rows

conn, rows = mysheet()
    
def get_role(user, rows):
    for row in rows.itertuples():
        if row.user == user:
            role = row.permission
            break
        else:
            role = False
    return role

# Start roles definition for pages flow

if "role" not in st.session_state:
    st.session_state["role"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None

ROLES = [None, "Cadastrar", "Solicitante", "Membro", "Admin"]

def login():
    st.header("Login")
    user = st.text_input("E-mail:")
    role = get_role(user, rows)
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

role = st.session_state["role"]

def logout():
    st.session_state["role"] = None
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

logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

request_1 = st.Page(
    "request/request_1.py",
    title="Iniciativas",
    icon=":material/help:",
    default=(role == "Solicitante"),
)
request_2 = st.Page(
    "request/request_2.py", title="Abertura de Tickets", icon=":material/bug_report:"
)
request_3 = st.Page(
    "request/request_3.py", title="Acompanhe seu Desenvolvimento", icon=":material/bug_report:"
)
request_4 = st.Page(
    "request/request_4.py", title="Receita Transformada", icon=":material/bug_report:"
)
request_5 = st.Page(
    "request/request_5.py", title="Pesquisa NPS", icon=":material/bug_report:"
)

respond_1 = st.Page(
    "respond/respond_1.py",
    title="Membro 1",
    icon=":material/healing:",
    default=(role == "Membro"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Membro 2", icon=":material/handyman:"
)

admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2, request_3, request_4, request_5]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Gestão Turnaround")

st.logo("images/horizontal.png", icon_image="images/icon.png")

page_dict = {}

if st.session_state["role"] in ["Solicitante", "Admin"]:
    page_dict["Solicitante"] = request_pages
if st.session_state["role"] in ["Membro", "Admin"]:
    page_dict["Membro"] = respond_pages
if st.session_state["role"] == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Conta": account_pages} | page_dict)
else:
    if st.session_state["role"] == "Cadastrar":
        pg = st.navigation([st.Page(new_user)])
    else:
        pg = st.navigation([st.Page(login)])

pg.run()
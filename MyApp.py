import streamlit as st
from project.utils import login, new_user

# Start roles definition for pages flow

if "role" not in st.session_state:
    st.session_state["role"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None

ROLES = [None, "Cadastrar", "Solicitante", "Membro", "Admin"]

role = st.session_state["role"]

def logout():
    st.session_state["role"] = None
    st.rerun()

logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
settings = st.Page("project/settings.py", title="Settings", icon=":material/settings:")

request_1 = st.Page(
    "project/request/request_1.py",
    title="Iniciativas",
    icon=":material/help:",
    default=(role == "Solicitante"),
)
request_2 = st.Page(
    "project/request/request_2.py", title="Abertura de Tickets", icon=":material/bug_report:"
)
request_3 = st.Page(
    "project/request/request_3.py", title="Acompanhe seu Desenvolvimento", icon=":material/bug_report:"
)
request_4 = st.Page(
    "project/request/request_4.py", title="Receita Transformada", icon=":material/bug_report:"
)
request_5 = st.Page(
    "project/request/request_5.py", title="Pesquisa NPS", icon=":material/bug_report:"
)

respond_1 = st.Page(
    "project/respond/respond_1.py",
    title="Membro 1",
    icon=":material/healing:",
    default=(role == "Membro"),
)
respond_2 = st.Page(
    "project/respond/respond_2.py", title="Membro 2", icon=":material/handyman:"
)

admin_1 = st.Page(
    "project/admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("project/admin/admin_2.py", title="Admin 2", icon=":material/security:")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2, request_3, request_4, request_5]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Gestão Turnaround")

st.logo("project/images/horizontal.png", icon_image="project/images/icon.png")

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
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from utils import conn, get_contracts, get_forms, generate_tasks

tabela_contratos = get_contracts()
lista_contratos = tabela_contratos["contrato"]

st.header("Abertura de Tickets")

st.write(st.session_state["user"])

with st.form(key="forms_new_project"):
    email = st.text_input("Email", value=st.session_state["user"])
    d1, d2 = st.columns([1,3])
    data = d1.date_input(label="Data", value="default_value_today", format="DD/MM/YYYY")
    name = d2.text_input("Nome")
    c1, c2, c3 = st.columns([3,2,2])
    contrato = c1.selectbox("Contrato", lista_contratos)
    engmanut = c2.selectbox("Tipo", ("Engenharia", "Manutenção"))
    escopo = c3.selectbox("Escopo", ("Suporte", "Proposta Financeira"))
    solicitacao = st.selectbox("Qual a sua solicitação?",
                               ("Novo Desenvolvimento",
                                "Conheci a solução e quero em meu contrato",
                                "Melhorias ou Ajustes em Desenvolvimento Entregue"))
    if solicitacao == "Novo Desenvolvimento":
        new_solution = st.text_input("Digite aqui o projeto que deseja implementar:")
        apply_solution = 0
        support_solution = 0
    if solicitacao == "Conheci a solução e quero em meu contrato":
        new_solution = 0
        support_solution = 0
        apply_solution = st.selectbox("Que solução deseja implementar?",
                                      ("Projeto 1", "Projeto 2", "Projeto 3", "Outros"),
                                      )
        if apply_solution == "Outros":
            apply_solution = st.text_input("Digite aqui o projeto que deseja implementar:")
    if solicitacao == "Melhorias ou Ajustes em Desenvolvimento Entregue":
        new_solution = 0
        apply_solution = 0
        support_solution = st.selectbox("Desenvolvimentos entregues no seu contrato:",
                                        ("Projeto 1", "Projeto 2", "Projeto 3"),
                                        )    
    #anexo = st.file_uploader("Tem anexo?")
    submit_button = st.form_submit_button("Enviar")

if submit_button:
    try:
        current_table = get_forms()
        id = max(current_table['id'])+1
        actual_update = pd.DataFrame.from_dict({
            "id":[id],
            "data_solicitacao": [data],
            "name": [name],
            "email": [email],
            "contrato": [contrato],
            "eng_manut": [engmanut],
            "escopo": [escopo],
            "solicitacao": [solicitacao],
            "new_solution": [new_solution],
            "apply_solution": [apply_solution],
            "support_solution": [support_solution]})
        aux = pd.concat([current_table, actual_update], ignore_index=False)
        new_table = conn.update(worksheet="forms",data=aux)
        st.info("Formulário sendo criado")
        generate_tasks(conn, id, solicitacao)
        st.success("Formulário enviado com sucesso!")
        st.cache_data.clear()
        time.sleep(2)
        st.rerun()
    except Exception as e:
        st.error("Erro ao enviar o formulário! Por favor atualize a página e tente novamente.")
        st.write(e)
        time.sleep(3)

# if submit_button:
#     b = anexo.getvalue()
#     with open("teste.txt", "wb") as f:
#         f.write(b)
#     df = pd.DataFrame.from_dict({"Nome": [name], "Email": [email], "Solicitação": [solicitacao]})
#     df["anexo"] = b
#     try:
#         if projeto:
#             df["Projeto"] = projeto
#             try:
#                 if outros:
#                     df["Outros"] = outros
#             except:
#                 pass
#     except:
#         pass

#    @st.cache_data
#    def convert_df(df):
#        return df.to_csv(index=False).encode('utf-8')

#    csv = convert_df(df)

#    st.download_button(
#    "Clique aqui para download",
#    csv,
#    "file.csv",
#    "text/csv",
#    key='download-csv'
#    )
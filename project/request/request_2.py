import streamlit as st
import pandas as pd
from datetime import datetime
import time
from project.utils import get_contracts, get_forms, generate_tasks, conn


tabela_contratos = get_contracts()
#tabela_contratos = pd.DataFrame.from_dict({"id": ["1", "2", "3"], "contrato": ["Braskem", "Bayer", "Dow"]})
lista_contratos = tabela_contratos["contrato"]

df_forms = get_forms()


st.header("Abertura de Tickets")

with st.container(border=True):
    email = st.text_input("Email", value=st.session_state["user"])
    d1, d2 = st.columns([1,3])
    data = d1.date_input(label="Data", value="default_value_today", format="DD/MM/YYYY")
    name = d2.text_input("Nome")
    c1, c2, c3 = st.columns([3,2,2])
    contrato = c1.selectbox("Contrato", lista_contratos)

    lista_new_solutions = df_forms.query("contrato == @contrato")["new_solution"]
    lista_apply_solutions = df_forms.query("contrato == @contrato")["apply_solution"]
    lista_desenvolvimentos = pd.concat([lista_new_solutions, lista_apply_solutions], ignore_index=True).drop_duplicates().dropna()
    
    engmanut = c2.selectbox("Tipo", ("Engenharia", "Manutenção"))
    escopo = c3.selectbox("Escopo", ("Suporte", "Proposta Financeira"))
    solicitacao = st.selectbox(key="box_solicitacao",
                               label="Qual a sua solicitação?",
                               options=
                               ("Novo Desenvolvimento",
                                "Conheci a solução e quero em meu contrato",
                                "Melhorias ou Ajustes em Desenvolvimento Entregue"))
    if solicitacao == "Novo Desenvolvimento":
        new_solution = st.text_input("Digite aqui o projeto que deseja implementar:")
        apply_solution = None
        support_solution = None
        description = None
    if solicitacao == "Conheci a solução e quero em meu contrato":
        new_solution = None
        support_solution = None
        apply_solution = st.selectbox(key="box_apply_solution",
                                      label="Que solução deseja implementar?",
                                      options=("Projeto 1", "Projeto 2", "Projeto 3", "Outros"),
                                      )
        if apply_solution == "Outros":
            apply_solution = st.text_input("Digite aqui o projeto que deseja implementar:")
        description = None
    if solicitacao == "Melhorias ou Ajustes em Desenvolvimento Entregue":
        new_solution = None
        apply_solution = None
        support_solution = st.selectbox(key="box_support_solution",
                                        label="Desenvolvimentos entregues/em andamento no seu contrato:",
                                        options=lista_desenvolvimentos,
                                        )
        description = st.text_input("Descreva aqui a melhoria ou ajuste desejado:")    
    #anexo = st.file_uploader("Tem anexo?")
    submit_button = st.button("Enviar")

if submit_button:
    try:
        current_table = df_forms
        #current_table = lista_forms
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
            "support_solution": [support_solution],
            "description": [description]})
        aux = pd.concat([current_table, actual_update], ignore_index=False)
        #lista_forms = pd.concat([current_table, actual_update], ignore_index=False)
        new_table = conn.update(worksheet="forms",data=aux)
        st.info("Formulário sendo criado")
        #generate_tasks(conn, id, solicitacao)
        generate_tasks(id, solicitacao)
        st.success("Formulário enviado com sucesso!")
        st.cache_data.clear()
        time.sleep(2)
        st.rerun()
    except Exception as e:
        st.error("Erro ao enviar o formulário! Por favor atualize a página e tente novamente.")
        st.write(e)
        time.sleep(3)
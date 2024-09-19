import streamlit as st
import pandas as pd
from datetime import datetime
import time
from project.utils import get_contracts, get_forms, generate_tasks, conn


tabela_contratos = get_contracts()
lista_contratos = tabela_contratos["contrato"]

df_forms = get_forms()
lista_solucoes_geral = df_forms["solution"].drop_duplicates().dropna()


st.header("Abertura de Tickets")

with st.container(border=True):
    email = st.text_input("Email", value=st.session_state["user"])
    d1, d2 = st.columns([1,3])
    data = d1.date_input(label="Data", value="default_value_today", format="DD/MM/YYYY")
    name = d2.text_input("Nome", value=st.session_state["name"])
    c1, c2, c3 = st.columns([3,2,2])
    contrato = c1.selectbox("Contrato", lista_contratos)

    lista_solucoes_contrato = df_forms.query("contract == @contrato")["solution"].drop_duplicates().dropna()
    
    engmanut = c2.selectbox("Tipo", ("Engenharia", "Manutenção"))
    escopo = c3.selectbox("Escopo", ("Suporte", "Proposta Financeira"))
    solicitacao = st.selectbox(key="box_solicitacao",
                               label="Qual a sua solicitação?",
                               options=
                               ("Novo Desenvolvimento",
                                "Conheci a solução e quero em meu contrato",
                                "Melhorias ou Ajustes em Desenvolvimento Entregue"))
    if solicitacao == "Novo Desenvolvimento":
        solution = st.text_input("Descreva aqui o projeto que deseja implementar:")
        description = None
    if solicitacao == "Conheci a solução e quero em meu contrato":
        solution = st.selectbox(key="box_apply_solution",
                                      label="Que solução deseja implementar?",
                                      options=lista_solucoes_geral,
                                      )
        if solution == "Outros":
            solution = st.text_input("Digite aqui o projeto que deseja implementar:")
        description = None
    if solicitacao == "Melhorias ou Ajustes em Desenvolvimento Entregue":
        solution = st.selectbox(key="box_support_solution",
                                        label="Desenvolvimentos entregues/em andamento no seu contrato:",
                                        options=lista_solucoes_contrato,
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
            "contract": [contrato],
            "eng_manut": [engmanut],
            "escope": [escopo],
            "solicitation": [solicitacao],
            "solution": [solution],
            "description": [description]})
        aux = pd.concat([current_table, actual_update], ignore_index=False)
        new_table = conn.update(worksheet="forms",data=aux)
        st.info("Formulário sendo criado")
        generate_tasks(id, solicitacao)
        st.success("Formulário enviado com sucesso!")
        st.cache_data.clear()
        time.sleep(2)
        st.rerun()
    except Exception as e:
        st.error("Erro ao enviar o formulário! Por favor atualize a página e tente novamente.")
        st.write(e)
        time.sleep(3)
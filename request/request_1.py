import streamlit as st
import pandas as pd

st.header("Solicitante 1")
st.write(f"Você está logado como {st.session_state['role']}.")

with st.form("user_input_form"):
    name = st.text_input("Nome")
    email = st.text_input("Email")
    solicitacao = st.radio("Qual a sua solicitação?",
                           ["**Novo Projeto**", "**Solução já implementada**"],
    captions=[
        "Não vi a solução aplicada",
        "Vi a solução aplicada e quero no meu contrato",
    ],
    )
    if solicitacao == "**Solução já implementada**":
        projeto = st.selectbox("Que solução deseja implementar?",
                              ("Projeto 1", "Projeto 2", "Projeto 3", "Outros"),
                              )
        if projeto == "Outros":
            outros = st.text_input("Digite aqui o projeto que deseja implementar:")
    if solicitacao == "**Novo Projeto**":
        projeto = st.text_input("Digite aqui o projeto que deseja implementar:")
    
    submit_button = st.form_submit_button("Enviar")

if submit_button:
    st.write(f"Nome: ***{name}***")
    st.write(f"Email: ***{email}***")
    st.write(f"Solicitação: {solicitacao}")
    df = pd.DataFrame.from_dict({"Nome": [name], "Email": [email], "Solicitação": [solicitacao]})
    try:
        if projeto:
            st.write(f"Projeto: {projeto}")
            df["Projeto"] = projeto
            try:
                if outros:
                    st.write(f"Projeto: {outros}")
                    df["Outros"] = outros
            except:
                pass
    except:
        pass

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
    "Clique aqui para download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )
import streamlit as st
from project.utils import get_forms, get_tasks

st.header("Acompanhe seu Desenvolvimento")
user = st.session_state["user"]
st.write("Você está logado como: ", user)

df_forms = get_forms()
df_tasks = get_tasks()

lista_desenvolvimentos = df_forms.query("email == @user")
lista_id_forms = list(lista_desenvolvimentos["id"])

lista_tarefas = df_tasks.query("id_forms in @lista_id_forms")

st.subheader("Projetos em andamento")
for form in lista_desenvolvimentos.itertuples():
    st.write(f"**Solicitação: {int(form.id)} - {form.solicitation} - {form.solution}**")

    col1, col2 = st.columns([1,9])
    with col2:
        st.dataframe(df_tasks.query("id_forms == @form.id"),
                 hide_index=True,
                 column_order=["task", "bucket", "due_date"],
                 column_config={
                     "task": st.column_config.TextColumn("Etapa"),
                     "bucket": st.column_config.TextColumn("Status"),
                     "due_date": st.column_config.DateColumn("Prazo", format="DD/MM/YYYY")
                 })
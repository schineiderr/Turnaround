import streamlit as st
from project.utils import lista_usuarios, conn

st.header("Admin 1")
st.write(f"Olá, {st.session_state['name'].split(' ')[0]}!")

placeholder = st.empty()
with placeholder.container(border=True):
   st.markdown("### Usuários")
   edited_lista_usuarios = st.data_editor(lista_usuarios,
                                          column_order=["name", "user", "permission"],
                                          use_container_width=True,
                                          hide_index=True,
                                          num_rows="dynamic",
                                          column_config={
                                             "permission": st.column_config.SelectboxColumn(options=["Solicitante", "Membro", "Admin"])
                                          })

   col1,col2,col3 = st.columns([2,1,2])
   with col2:
      save_button = st.button("Salvar")
   if save_button:
      try:
         df = conn.update(worksheet="usuarios",data=edited_lista_usuarios)
         #lista_usuarios = edited_lista_usuarios
         st.success("Usuários atualizados com sucesso!")
      except:
         st.error("Não foi possível atualizar! Contate o desenvolvedor")
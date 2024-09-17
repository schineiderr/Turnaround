import streamlit as st
# import random
# import time
# from text_generation import InferenceAPIClient

st.header("Conheça nossas Iniciativas!")

tab1, tab2 = st.tabs(["Ecossistema de Soluções", "Soluções DQOGE"])

with tab1:
    tab1.subheader("Conteúdo da primeira página")

with tab2:
    tab2.subheader("Conteúdo da segunda página")

#client = InferenceAPIClient("HuggingFaceH4/starchat-beta", token=st.secrets["HF_API_KEY"])

# # Streamed response emulator
# def response_generator(response):
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # Display chat messages from history on app rerun
# for msg in st.session_state["messages"]:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # React to user input
# if prompt := st.chat_input("Say something"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         response = client.generate(prompt).generated_text
#         st.write(response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})

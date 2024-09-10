import streamlit as st
import random
import time
from text_generation import InferenceAPIClient

client = InferenceAPIClient("HuggingFaceH4/starchat-beta", token="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")

st.header("Echo Bot")

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# React to user input
if prompt := st.chat_input("Say something"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = client.generate(prompt).generated_text
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# text = ""
# for response in client.generate_stream("Why is the sky blue?"):
#     if not response.token.special:
#         text += response.token.text

# st.write(text)

#from text_generation.inference_api import deployed_models
#st.write(deployed_models())
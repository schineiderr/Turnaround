import streamlit as st
import hashlib

st.header("Settings")
st.write(f"You are logged in as {st.session_state['role']}.")

teste = b"abc"

hash_obj = hashlib.sha256(teste)
hex_hash = hash_obj.hexdigest()
st.write(hex_hash)
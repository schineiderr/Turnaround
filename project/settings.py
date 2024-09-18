import streamlit as st
import hashlib

st.header("Settings")
st.write(f"You are logged in as {st.session_state['role']}.")

# from streamlit_google_auth import Authenticate

# authenticator = Authenticate(
#     secret_credentials_path='.streamlit/client_secret.json',
#     cookie_name='my_cookie_name',
#     cookie_key='this_is_secret',
#     redirect_uri='http://localhost:8501',
# )

# # Check if the user is already authenticated
# authenticator.check_authentification()

# # Display the login button if the user is not authenticated
# authenticator.login()

# # Display the user information and logout button if the user is authenticated
# if st.session_state['connected']:
#     st.image(st.session_state['user_info'].get('picture'))
#     st.write(f"Hello, {st.session_state['user_info'].get('name')}")
#     st.write(f"Your email is {st.session_state['user_info'].get('email')}")
#     if st.button('Log out'):
#         authenticator.logout()
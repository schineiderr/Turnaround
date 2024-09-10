import streamlit as st
import pandas as pd
from office365.sharepoint.files.file import File
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext

st.header("Admin 2")
st.write(f"Você está logado como {st.session_state['role']}.")

sharepoint_url = "https://timenow.sharepoint.com/sites/Turnaround168"
folder_url = "/Turnaround168/Documentos%20Compartilhados/Gest%C3%A3o%20Turnaround"

# First section: e-mail and password as input
placeholder = st.empty()
with placeholder.container():
    st.markdown("## **SharePoint connection with Streamlit**")
    st.markdown("--------------")
    email_user = st.text_input("E-mail")
    password_user = st.text_input("Senha", type="password")

    # Save the button status
    Button = st.button("Entrar")
    if st.session_state.get('button') != True:
      st.session_state['button'] = Button

# Authentication and connection to SharePoint
def authentication(email_user, password_user, sharepoint_url) :
  auth = AuthenticationContext(sharepoint_url) 
  auth.acquire_token_for_user(email_user, password_user)
  ctx = ClientContext(sharepoint_url, auth)
  web = ctx.web
  ctx.load(web)
  ctx.execute_query()
  return ctx

# Second section: display results
# Check if the button "Connect" has been clicked
if st.session_state['button'] :
  try :                            
    placeholder.empty()
    if "ctx" not in st.session_state :
        st.session_state["ctx"] = authentication(email_user, 
                                                 password_user,
                                                 sharepoint_url)
    
    st.write("Authentication: successfull!")
    st.write("Connected to SharePoint: **{}**".format( st.session_state["ctx"].web.properties['Title']))
  
    # Connection to the SharePoint folder
    target_folder = st.session_state["ctx"].web.get_folder_by_server_relative_url(folder_url)
    
    # Read and load items
    items = target_folder.files
    st.session_state["ctx"].load(items)
    st.session_state["ctx"].execute_query()
    
    # Save some information for each file using item.properties
    names, last_mod, relative_url = [], [], []
    for item in items:
        names.append( item.properties["Name"] )
        last_mod.append( item.properties["TimeLastModified"] )
        relative_url.append( item.properties["ServerRelativeUrl"] )
     
    # Create and display the final data frame
    Index = ["File name", "Last modified", "Relative url"]
    dataframe = pd.DataFrame([names, last_mod, relative_url], index = Index).T
    st.write("")
    st.write("")
    st.write("These are the files in the folder:")
    st.table(dataframe)
  
  # Handle the error in the authentication section
  except Exception as e:
      st.write("**Authentication error: reload the page**")
      #st.write("Erro: ", e)


'''
Links para autenticar com Sharepoint:

https://medium.com/@sam.campitiello/streamlit-connection-to-a-sharepoint-folder-part-1-30146f26456a

https://medium.com/@sam.campitiello/streamlit-connection-to-a-sharepoint-folder-part-2-236ef7925e5c

https://medium.com/@sam.campitiello/streamlit-connection-to-a-sharepoint-folder-part-3-cfdba1e08bda

Como Resolver:

https://stackoverflow.com/questions/55922791/azure-sharepoint-multi-factor-authentication-with-python

'''
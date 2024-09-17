import streamlit as st
import pandas as pd
import numpy as np

with st.container(border=True):

    st.header("Membro 1")
    st.write(f"Você está logado como {st.session_state['role']}.")

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.bar_chart(chart_data)
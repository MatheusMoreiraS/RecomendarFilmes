import streamlit as st
from utils.utils import setup_page, load_css

setup_page(titulo="Cadastro realizado!", hide_sidebar=True)
load_css(["styles/components.css"])

st.success("Cadastro realizado com sucesso!")
st.write("Agora você pode fazer login usando seu nome de usuário e senha.")
if st.button("Ir para Login", use_container_width=True):
    st.switch_page("app.py")

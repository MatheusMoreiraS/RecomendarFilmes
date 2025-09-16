import streamlit as st
import requests

# Modulo de teste da home (em construção)
API_URL = "http://127.0.0.1:5000"

# Configurações da página
st.set_page_config(
    initial_sidebar_state="collapsed"
)


# Ocultar side-bar do streamlit
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


st.title("API DE FILMES")

st.sidebar.title("MENU")


if st.button("BUSCAR RECOMENDAÇÕES"):
    try:
        response = requests.get(f"{API_URL}/filmes/mock")
        filmes = response.json()

        st.subheader('FILMES DA API')
        st.dataframe(filmes)
    except requests.exceptions.ConnectionError:
        st.error("NÃO FOI POSSÍVEL CONECTAR A API, VERIFIQUE SE O FLASK ESTA RODANDO")

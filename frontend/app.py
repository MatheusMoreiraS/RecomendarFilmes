import streamlit as st
import requests
from utils.utils import setup_page

# URLS
URL_LOGIN = "http://127.0.0.1:5000/login"
API_URL = "http://127.0.0.1:5000"

# Configuração da página

setup_page(titulo="Recomendação de filmes", hide_sidebar=True)


# Função para checar o login
def check_login(username, password):
    payload = {'username': username, "password": password}
    try:
        response = requests.post(URL_LOGIN, json=payload)
        if response.status_code == 401:
            return {"success": False, "message": "Senha ou usuário incorreto"}
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "message": "erro de conexao"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"erro de conexao{e}"}


# Função principal
def main():
    # Verificar se já está logado
    if st.session_state.get("logged_in", False):
        st.switch_page("pages/busca_filmes.py")

    # Interface de Login
    st.title("Recomendação de Filmes")
    st.markdown("### Faça seu login")

    col1, col2 = st.columns([2, 1])

    # Colunas do front end
    with col1:
        with st.form("login_form"):
            username = st.text_input("Nome de usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submitted = st.form_submit_button("ENTRAR", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("Preencha todos os campos!")
                else:
                    login_result = check_login(username, password)

                    if login_result.get("success"):
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"{login_result.get('message', 'Falha no login')}")
        if st.button("Esqueci minha senha", use_container_width=True):
            st.switch_page("pages/reset_senha.py")

    with col2:
        st.info("**Não tem conta?**")
        if st.button("Criar Conta", use_container_width=True, type="secondary"):
            st.switch_page("pages/cadastro.py")


# Execução da função principal (main)
if __name__ == "__main__":
    main()

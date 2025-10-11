import streamlit as st
import requests
from utils.utils import setup_page, load_css, is_logged_in

# URLS
URL_LOGIN = "http://127.0.0.1:5000/login"
API_URL = "http://127.0.0.1:5000"

# Configuração da página
setup_page(titulo="RotaCine Login", hide_sidebar=True)
load_css(["styles/components.css", "styles/geral.css"])


# Função para checar o login
def check_login(username, password):
    payload = {'username': username, "password": password}
    try:
        response = requests.post(URL_LOGIN, json=payload)
        if response.status_code == 401:
            return {"success": False,
                    "message": "Senha ou usuário incorreto"}
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False,
                    "message": "Erro de conexão com o servidor"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Erro de conexão: {e}"}


# Função principal
def main():
    # Verificar se já está logado
    if is_logged_in():
        st.switch_page("pages/busca_filmes.py")

    # Interface de Login
    st.markdown('<h1 class="titulo">🎬 RotaCine</h1>', unsafe_allow_html=True)
    st.markdown("### Faça seu login para continuar")
    st.markdown("Descubra novos filmes personalizados para você!")

    # Colunas do front end
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        # Container para o formulário
        with st.container():
            with st.form("login_form"):
                st.markdown("#### Acesse sua conta")
                username = st.text_input(
                    "Nome de usuário",
                    placeholder="Digite seu usuário",
                    help="Insira seu nome de usuário"
                )
                password = st.text_input(
                    "Senha",
                    type="password",
                    placeholder="Digite sua senha",
                    help="Insira sua senha"
                )

                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("ENTRAR", width='stretch')

                if submitted:
                    if not username or not password:
                        st.error(" Por favor, preencha todos os campos!")
                    else:
                        with st.spinner("Autenticando..."):
                            login_result = check_login(username, password)

                        if login_result.get("success"):
                            st.session_state["access_token"] = login_result.get('access_token')
                            st.session_state["username"] = username
                            st.success("Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(
                                f"{login_result.get('message', 'Falha no login')}")

        st.divider()
        if st.button("Esqueci minha senha", width='stretch'):
            st.switch_page("pages/reset_senha.py")

    with col2:
        with st.container():
            st.info("Não tem conta?")
            if st.button("Criar Conta", width='stretch'):
                st.switch_page("pages/cadastro.py")


# Execução da função principal (main)
if __name__ == "__main__":
    main()

import streamlit as st
import requests

# Links para conexão com o BACKEND
URL_LOGIN = "http://127.0.0.1:5000/login"
API_URL = "http://127.0.0.1:5000"

# Configuração da página
st.set_page_config(
    page_title="Recomendação de filmes - Login",
    layout="centered",
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


# Função para checar o login


def check_login(username, password):
    payload = {'username': username, "password": password}
    print(f"enviadno para a api{payload}")
    try:
        response = requests.post(URL_LOGIN, json=payload)
        print(f"status de resposta = {response.status_code}")
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
        st.switch_page("pages/home.py")

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
        st.markdown(
            "<a href='/reset_senha' style='display:block; text-align:center; color:deepskyblue; text-decoration:underline;'>Esqueci minha senha</a>",
            unsafe_allow_html=True
                    )

    with col2:
        st.info("**Não tem conta?**")
        if st.button("Criar Conta", use_container_width=True, type="secondary"):
            st.switch_page("pages/cadastro.py")


# Execução da função principal (main)
if __name__ == "__main__":
    main()

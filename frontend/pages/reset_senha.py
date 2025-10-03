import streamlit as st
import requests
from utils.utils import validar_email, setup_page

setup_page(titulo="Esqueci minha senha", hide_sidebar=True)

API_URL = "http://127.0.0.1:5000"
URL_RESET = f"{API_URL}/reset_senha"


# Solicita o reset para o backend
def solicitar_reset(email: str):
    try:
        response = requests.post(URL_RESET, json={"email": email}, timeout=10)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"success": False, "message": f"Erro de conexão: {e}"}


# Função principal
def main():
    # Título
    st.title("Esqueci minha senha")
    st.markdown("### Informe seu email para recuperar o acesso")

    # Criação do formulário
    with st.form("reset_form"):
        email = st.text_input("Email", placeholder="Digite seu email")
        submitted = st.form_submit_button("Enviar", use_container_width=True)

        # Faz a requisição
        if submitted:
            if not email or not validar_email(email):
                st.error("Digite um email válido!")
            else:
                status, resp = solicitar_reset(email)
                if status == 200 and resp.get("success"):
                    st.success("Se este email estiver cadastrado, enviaremos instruções de redefinição.")
                else:
                    st.error(f"Erro: {resp.get('message', 'Falha ao solicitar redefinição')}")

    # Voltar ao login
    if st.button("Voltar para Login", use_container_width=True, type="secondary"):
        st.switch_page("app.py")


# Executa a função principal
if __name__ == "__main__":
    main()

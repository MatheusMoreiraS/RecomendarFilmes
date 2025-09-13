import streamlit as st
import requests
import re

API_URL = "http://127.0.0.1:5000"
URL_RESET = f"{API_URL}/reset_senha"

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


# Validação simples de email
def validar_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Solicita o reset para o backend
def solicitar_reset(email: str):
    try:
        response = requests.post(URL_RESET, json={"email": email}, timeout=10)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"success": False, "message": f"Erro de conexão: {e}"}


# Função principal
def main():
    # Configurações da página
    st.set_page_config(
        page_title="Esqueci minha senha",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Título
    st.title("Esqueci minha senha")
    st.markdown("### Informe seu email para recuperar o acesso")

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

    st.divider()

    # Voltar ao login
    if st.button("⬅️ Voltar para Login", use_container_width=True, type="secondary"):
        st.switch_page("app.py")


# Executa a função principal
if __name__ == "__main__":
    main()

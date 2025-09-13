import streamlit as st
import requests
from utils.utils import validar_senha

API_URL = "http://127.0.0.1:5000"
REDEFINIR_URL = 'http://127.0.0.1:5000/redefinir'

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


token = st.query_params.get("token")  # Pega o token da URL

# Verifica o token
if token:
    st.title("Redefinir Senha")
    nova_senha = st.text_input(
            "Senha",
            type="password",
            placeholder="Mínimo 6 caracteres",
            help="Senha deve conter letras e números"
        )

    confirmar = st.text_input(
            "Confirmar Senha",
            type="password",
            placeholder="Digite a senha novamente"
        )

    senha_valida, senha_msg = validar_senha(nova_senha) if nova_senha else (False, "")
    if senha_msg:
        if senha_valida:
            st.success(f"{senha_msg}")
        else:
            st.warning(f"{senha_msg}")

    # Altera a senha
    if st.button("Alterar Senha"):
        erros = []
        if not nova_senha:
            erros.append("Senha é obrigatória")
        elif not senha_valida:
            erros.append(senha_msg)

        if nova_senha != confirmar:
            erros.append("As senhas não coincidem")

        if nova_senha == confirmar:
            resp = requests.post(f"{API_URL}/redefinir",
                                 json={"token": token, "new_pw": nova_senha})
            if resp.status_code == 200:
                st.success("Senha redefinida com sucesso! ✅")
                # st.page_link("app.py", label="Ir para página de login.")
                st.markdown(
                            "<a href='/' style='display:block; text-align:center; color:LimeGreen; text-decoration:underline;'>Página de Login</a>",
                            unsafe_allow_html=True
                            )

            else:
                st.error(resp.json().get("message"))
        else:
            st.error("As senhas não conferem")

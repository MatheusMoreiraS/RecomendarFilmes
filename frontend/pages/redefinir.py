import streamlit as st
import requests
from utils.utils import validar_senha, setup_page, load_css

setup_page(titulo="Redefinição de senha", hide_sidebar=True)
load_css(["styles/geral.css", "styles/components.css"])

API_URL = "http://127.0.0.1:5000"
REDEFINIR_URL = f'{API_URL}/redefinir'

token = st.query_params.get("token")  # Pega o token da URL

# Verifica o token
if token:
    if st.button("Voltar", help="Voltar para o login"):
        st.switch_page("app.py")

    st.markdown('<h1 class="titulo">Alteração de senha</h1>',
                unsafe_allow_html=True)
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

            else:
                st.error(resp.json().get("message"))
        else:
            st.error("As senhas não conferem")

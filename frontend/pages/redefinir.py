import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"
REDEFINIR_URL = 'http://127.0.0.1:5000/redefinir'

token = st.query_params.get("token")  # Pega o token da URL

# Verifica o token
if token:
    st.title("Redefinir Senha")
    nova_senha = st.text_input("Digite sua nova senha", type="password")
    confirmar = st.text_input("Confirme a nova senha", type="password")

    # Altera a senha
    if st.button("Alterar Senha"):
        if nova_senha == confirmar:
            resp = requests.post(f"{API_URL}/redefinir",
                                 json={"token": token, "new_pw": nova_senha})
            if resp.status_code == 200:
                st.success("Senha redefinida com sucesso! ✅")
            else:
                st.error(resp.json().get("message"))
        else:
            st.error("As senhas não conferem")

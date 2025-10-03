import streamlit as st
from utils.utils import setup_page

setup_page(titulo="Cadastro realizado!", hide_sidebar=True)


# Função principal
def main():
    st.success("Cadastro realizado com sucesso!")
    st.write("Agora você pode fazer login usando seu nome de usuário e senha.")

    # Botão único para ir ao login
    col_login = st.columns([1, 2, 1])[1]
    with col_login:
        if st.button("Ir para Login", use_container_width=True):
            st.switch_page("app.py")


if __name__ == "__main__":
    main()

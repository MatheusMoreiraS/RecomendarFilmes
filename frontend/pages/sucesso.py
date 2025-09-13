import streamlit as st


def main():
    st.set_page_config(
        page_title="Cadastro Concluído",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.success("Cadastro realizado com sucesso!")
    st.write("Agora você pode fazer login usando seu nome de usuário e senha.")

    # Botão único para ir ao login
    col_login = st.columns([1, 2, 1])[1]
    with col_login:
        if st.button("🔐 Ir para Login", use_container_width=True):
            st.switch_page("app.py")  # nome da sua página de login


if __name__ == "__main__":
    main()

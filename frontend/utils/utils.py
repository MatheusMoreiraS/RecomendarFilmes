import streamlit as st
import re
from time import sleep
from typing import List


# Validação de senha
def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    if not any(c.isalpha() for c in senha):
        return False, "A senha deve conter pelo menos uma letra"
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"


# Validação básica de email
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Configuração páginas Streamlit
def setup_page(titulo: str, layout: str = "centered", protegida: bool = False, hide_sidebar: bool = False):
    """
    Args:
        titulo: titulo da pagina
        layout: centered ou wide
        protegida: se true, precisa estar logado para ver a página
        hide_sidebar: se true, a barra será escondida
    """
    st.set_page_config(
        page_title=titulo,
        layout=layout,
        initial_sidebar_state="collapsed" if hide_sidebar else "auto"
    )

    st.markdown(
        """
        <style>
            [data-testid="stSidebarNavItems"] {display: none;}
        <style>
        """, unsafe_allow_html=True
    )

    if hide_sidebar:
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] {display: none;}
            <style>
            """, unsafe_allow_html=True,
        )
    if protegida and not st.session_state.get("logged_in", False):
        st.error("Por favor, faça login primeiro.")
        sleep(4)
        st.switch_page("app.py")

    if st.session_state.get("logged_in", False) and not hide_sidebar:
        st.sidebar.success(f"Logado como: {st.session_state.get('username')}")
        st.sidebar.header("Menu de navegação")

        st.sidebar.page_link("pages/busca_filmes.py", label="Buscar filmes")
        # st.sidebar.page_link("pages/cadastro.py", label="Cadastro")

        st.sidebar.divider()

        if st.sidebar.button(
                "Logout", use_container_width=True, type="primary"):
            st.session_state["logged_in"] = False
            st.session_state.pop("username", None)
            st.switch_page("app.py")


# Carregar arquivos CSS
def load_css(file_paths: List[str]):
    """
    Args:
        file_paths: Uma lista para os arquivos css.
    """
    full_css = ""
    for file_path in file_paths:
        try:
            with open(file_path) as f:
                full_css += f.read()
        except FileNotFoundError:
            st.error(f"Arquivo CSS não encontrado em: {file_path}")

    st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)

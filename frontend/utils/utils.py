import streamlit as st
import re
from time import sleep
from typing import List
import requests

API_URL = "http://127.0.0.1:5000"


def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    if not any(c.isalpha() for c in senha):
        return False, "A senha deve conter pelo menos uma letra"
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"


def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_logged_in():
    return st.session_state.get('access_token') not in [None, ""]


# Retorna autorização de caso tenha token
def get_auth():
    if is_logged_in():
        token = st.session_state.get('access_token')
        if token:
            return {'Authorization': f'Bearer {token}'}
    return {}


def logout():
    keys_to_clear = ['access_token', 'username']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.switch_page("app.py")


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
    if protegida and not is_logged_in():
        st.error("Por favor, faça login primeiro.")
        sleep(4)
        st.switch_page("app.py")

    if is_logged_in() and not hide_sidebar:
        st.sidebar.success(f"Logado como: {st.session_state.get('username')}")
        st.sidebar.header("Menu de navegação")

        st.sidebar.page_link("pages/busca_filmes.py", label="Buscar filmes")
        st.sidebar.page_link("pages/favoritos.py", label="Meus Favoritos")

        st.sidebar.divider()

        if st.sidebar.button("Logout", width='stretch', type="primary"):
            logout()
            st.switch_page("app.py")


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


def add_favorito(tmdb_id):
    """
    Args:
        tmdb_id = id do filme
    """
    url = f"{API_URL}/favoritos"
    payload = {"tmdb_id": tmdb_id}
    headers = get_auth()

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=10)
        data = response.json()
        if response.status_code == 200:
            st.toast(f"{data.get('message')}")

        elif response.status_code == 409:
            st.toast(f"{data.get('message')}")

        else:
            response.raise_for_status()

    except requests.RequestException as e:
        st.error(f"Erro ao comunicar com a API: {e}")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")


def carregar_favoritos():
    url = f"{API_URL}/favoritos"
    headers = get_auth()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Não foi possível carregar seus favoritos: {e}")
        return None


def remover_favorito(tmdb_id):
    """
    Args:
        tmdb_id = id do filme
    """
    url = f"{API_URL}/favoritos/{tmdb_id}"
    headers = get_auth()
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            st.toast("Filme removido com sucesso!")
            sleep(1)
            st.rerun()
        else:
            st.toast(f"{data.get('message')}")
    except requests.RequestException as e:
        st.error(f"Erro ao remover o filme: {e}")

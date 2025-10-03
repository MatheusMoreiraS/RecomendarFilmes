import streamlit as st
import requests
from time import sleep
from utils.utils import setup_page

setup_page(titulo="Rotacine", layout="wide", protegida=True)

# CSS
st.markdown("""
<style>
    /* Badge de gêneros */
    .generos {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
        margin: 2px 5px 2px 0;
        background: linear-gradient(90deg, #FF512F, #DD2476);
        color: white;
        font-weight: bold;
    }

    /* Badge de nota */
    .media-votos {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 1rem;
        margin: 6px 5px 4px 0;
        background: #FFD700;
        color: #000;
        font-weight: bold;
    }

    /* Quantidade de votos (menor e cinza) */
    .votos {
        font-size: 0.8rem;
        color: #666;
        margin-left: 6px;
    }
    h1 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    sleep(5)
    st.switch_page("app.py")
col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    st.write("")

with col2:
    st.title("RotaCine")

with col3:
    st.write("")


# Url
API_URL = "http://127.0.0.1:5000"
IMAGEM_URL = "https://image.tmdb.org/t/p/w500"

st.header("Pesquisar Filmes")
termo_pesquisa = st.text_input(
    "Digite o nome de um filme que você gosta:",
    placeholder="Ex: Batman, O Senhor dos Anéis, Interestelar..."
)

if st.button("Procurar"):
    if termo_pesquisa:
        try:
            url = f"{API_URL}/filmes/pesquisar"
            response = requests.get(url, params={'q': termo_pesquisa})
            response.raise_for_status()
            resultados = response.json()

            if resultados:
                st.success(f"Encontramos {len(resultados)} resultado(s) para '{termo_pesquisa}':")
                st.divider()

                cols = st.columns(5)

                for i, filme in enumerate(resultados):
                    col = cols[i % 5]

                    with col:
                        with st.container(border=True):
                            if filme.get("poster_path"):
                                st.image(f"{IMAGEM_URL}{filme['poster_path']}", use_container_width=True)

                            st.subheader(filme['titulo'])

                            st.markdown(
                                f"<span class='generos'>🎭 {filme['generos']}</span>",
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f"<span class='media-votos'>⭐ {filme['media_votos']:.1f}/10</span>"
                                f"<span class='votos'>({filme['qtd_votos']} votos)</span>",
                                unsafe_allow_html=True
                            )

                            with st.expander("📖 Ver Sinopse"):
                                if filme['sinopse'] == "":
                                    st.write("Sinopse não disponível")
                                st.write(filme['sinopse'])
            else:
                st.warning(f"Nenhum filme encontrado para '{termo_pesquisa}'. Tente outro termo.")
        except requests.RequestException as e:
            st.error(f"Erro ao comunicar com a API: {e}")
    else:
        st.info("Por favor, digite algo para pesquisar.")

import streamlit as st
import requests
from utils.utils import setup_page, load_css

setup_page(titulo="Rotacine", layout="wide", protegida=True)

# CSS Modernizado
load_css(['styles/geral.css', 'styles/components.css', 'styles/badges.css'])

# URLs
API_URL = "http://127.0.0.1:5000"
IMAGEM_URL = "https://image.tmdb.org/t/p/w500"

# Header
st.markdown('<h1 class="titulo">🎬 RotaCine</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Descubra filmes incríveis baseados nos seus favoritos</p>', unsafe_allow_html=True)

# Seção de pesquisa
col_search, col_button, col_filtro = st.columns([5, 1.5, 2])

with col_search:
    termo_pesquisa = st.text_input(
        "Digite o nome do filme:",
        placeholder="Ex: Batman, O Senhor dos Anéis, Interestelar...",
        label_visibility="collapsed",
        key="search_input"
    )

with col_button:
    buscar = st.button("Buscar", width="stretch")

with col_filtro:
    nota_minima = st.selectbox(
        "Filtrar por nota",
        options=[0, 5, 6, 7, 8],
        format_func=lambda x: f"⭐ Nota mínima: {x}" if x > 0 else "Todas as notas",
        label_visibility='collapsed'
    )

st.divider()

# Lógica de busca
if buscar or (termo_pesquisa and len(termo_pesquisa) > 2):
    if termo_pesquisa.strip():
        try:
            with st.spinner('Buscando filmes...'):
                url = f"{API_URL}/filmes/pesquisar"
                response = requests.get(url, params={'q': termo_pesquisa}, timeout=10)
                response.raise_for_status()
                resultados = response.json()

            # Filtro por nota
            if nota_minima > 0:
                resultados = [f for f in resultados if f.get('media_votos', 0) >= nota_minima]

            if resultados:
                st.markdown(
                    f'<div class="result-count">{len(resultados)} filme(s) encontrado(s) para "{termo_pesquisa}"</div>',
                    unsafe_allow_html=True
                )

                cols = st.columns(5, gap="medium")

                for i, filme in enumerate(resultados):
                    col = cols[i % 5]
                    with col:
                        with st.container(border=True):
                            # Poster
                            if filme.get("poster_path"):
                                st.image(
                                    f"{IMAGEM_URL}{filme['poster_path']}",
                                )

                            # Título
                            st.markdown(
                                f'<div class="movie-title">{filme["titulo"]}</div>',
                                unsafe_allow_html=True
                            )

                            # Gênero
                            if filme['generos']:
                                st.markdown(
                                    f'<span class="genero-badge">🎭 {filme["generos"]}</span>',
                                    unsafe_allow_html=True
                                )

                            # Notas
                            nota = filme['media_votos']
                            if nota >= 8:
                                classe_nota = "nota-alta"
                            elif nota >= 6:
                                classe_nota = "nota-media"
                            else:
                                classe_nota = "nota-baixa"
                            st.markdown(
                                f"<span class='votos-badge {classe_nota}'>⭐ {nota:.1f}/10</span>"
                                f"<span class='vote-count'>({filme['qtd_votos']:,} votos)</span>",
                                unsafe_allow_html=True
                            )

                            # Sinopse
                            with st.expander("Ver sinopse"):
                                sinopse = filme.get('sinopse')
                                if sinopse:
                                    st.write(sinopse)
                                else:
                                    st.info("Sinopse não disponível")

            else:
                st.warning(
                    f"🔍 Nenhum filme encontrado para **'{termo_pesquisa}'**")
                st.info("💡 **Dicas:**\n- Verifique a ortografia"
                        "\n- Tente palavras-chave diferentes"
                        "\n- Reduza a nota mínima no filtro")

        except requests.Timeout:
            st.error("Tempo limite excedido. Tente novamente.")
        except requests.RequestException as e:
            st.error(f"Erro ao comunicar com a API: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
    else:
        st.warning("Por favor, digite o nome de um filme para pesquisar.")
else:
    # Tela inicial com instruções
    st.info("Como funciona?")
    st.caption("Digite o nome de um filme que você gosta no campo acima e"
               " descubra recomendações similares.")
    st.caption("Use o filtro para refinar sua busca!")

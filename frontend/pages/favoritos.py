import streamlit as st
from utils.utils import setup_page, load_css, get_auth, remover_favorito, carregar_favoritos

setup_page(titulo="Meus Favoritos", protegida=True, layout="wide")
load_css(['styles/geral.css', 'styles/components.css', 'styles/badges.css'])

# URLs
API_URL = "http://127.0.0.1:5000"
IMAGEM_URL = "https://image.tmdb.org/t/p/w500"

st.markdown('<h1 class="titulo">❤️Filmes Favoritos</h1>',
            unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Seus filmes favoritos.</p>',
            unsafe_allow_html=True)
st.divider()

favoritos = carregar_favoritos()

if favoritos is not None:
    if not favoritos:
        st.info("Você ainda não adicionou nenhum filme aos favoritos."
                " Busque no botão abaixo")
        if st.button("Buscar Filmes"):
            st.switch_page("pages/busca_filmes.py")
    else:
        st.markdown(
            f'<div class="result-count">Você tem {len(favoritos)} filme(s) na sua lista.</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(5, gap="medium")
        for i, filme in enumerate(favoritos):
            col = cols[i % 5]
            with col:
                with st.container(border=True):
                    if st.button("Remover",
                                 key=f"rem_{filme['tmdb_id']}",
                                 width='content',
                                 type="primary"):
                        remover_favorito(filme['tmdb_id'])

                    if filme.get("poster_path"):
                        st.image(f"{IMAGEM_URL}{filme['poster_path']}")

                    st.markdown(
                        f'<div class="movie-title">{filme["titulo"]}</div>',
                        unsafe_allow_html=True)

                    if filme['generos']:
                        st.markdown(
                            f'<span class="genero-badge">🎭 {filme["generos"]}</span>',
                            unsafe_allow_html=True)

                    nota = filme.get('media_votos', 0)
                    classe_nota = "nota-alta" if nota >= 8 else "nota-media" if nota >= 6 else "nota-baixa"
                    st.markdown(
                        f"<span class='votos-badge {classe_nota}'>⭐ {nota:.1f}/10</span>"
                        f"<span class='vote-count'>({filme.get('qtd_votos', 0):,} votos)</span>",
                        unsafe_allow_html=True
                    )

                    with st.expander("Ver sinopse"):
                        sinopse = filme.get('sinopse')
                        st.write(
                            sinopse if sinopse else "Sinopse não disponível")

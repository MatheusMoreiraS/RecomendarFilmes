import streamlit as st
import requests
from utils.utils import validar_senha, validar_email, setup_page, load_css

setup_page(titulo="Cadastro", hide_sidebar=True)
load_css(["styles/geral.css", "styles/components.css"])

# URLs da API
API_URL = "http://127.0.0.1:5000"
URL_CADASTRO = f"{API_URL}/cadastro"


# Função para cadastrar o usuário na API
def cadastrar_usuario(user_data):
    try:
        response = requests.post(URL_CADASTRO, json=user_data, timeout=10)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"success": False, "message": f"Erro de conexão: {e}"}


# Função principal
def main():
    if "cadastro_ok" not in st.session_state:
        st.session_state["cadastro_ok"] = False
    if "novo_usuario" not in st.session_state:
        st.session_state["novo_usuario"] = ""

    col_back, col_title = st.columns([1, 6])

    with col_title:
        st.markdown('<h1 class="titulo">Criar Conta</h1>',
                    unsafe_allow_html=True)

    with col_back:
        if st.button("← Voltar", help="Voltar para o login", width="content"):
            st.switch_page("app.py")

    # Container do formulário
    with st.container():
        st.markdown("### Seus dados")
        st.caption("Preencha as informações abaixo para criar sua conta")

        # Formulário de cadastro
        with st.form("cadastro_form", clear_on_submit=False):
            col1, col2 = st.columns(2, gap="medium")

            lista_generos = [
                "Ação", "Aventura", "Comédia", "Drama", "Fantasia",
                "Ficção Científica", "Guerra", "Musical", "Romance",
                "Suspense", "Terror", "Animação"
            ]

            with col1:
                st.markdown("###### Informações Pessoais")
                name = st.text_input(
                    "Nome Completo",
                    placeholder="Digite seu nome completo",
                    help="Nome que será exibido no sistema"
                )
                email = st.text_input(
                    "Email",
                    placeholder="seu@email.com",
                    help="Email válido para contato e recuperação de senha"
                )

            with col2:
                st.markdown("###### Preferências")
                user = st.text_input(
                    "Nome de Usuário",
                    placeholder="Digite um nome para ser seu usuário",
                    help="Nome usado para fazer login (mín. 3 caracteres)"
                )
                generos_selecao = st.multiselect(
                    "Gêneros favoritos",
                    options=lista_generos,
                    placeholder="Escolha 3 gêneros",
                    help="Selecione seus 3 gêneros de filme favoritos",
                )

            st.markdown("###### Segurança")
            col_pass1, col_pass2 = st.columns(2, gap="medium")

            with col_pass1:
                password = st.text_input(
                    "Senha",
                    type="password",
                    placeholder="Mínimo 6 caracteres",
                    help="Senha deve conter letras e números"
                )

            with col_pass2:
                confirm_pw = st.text_input(
                    "Confirmar Senha",
                    type="password",
                    placeholder="Digite a senha novamente"
                )

            # Validação de senha em tempo real
            if password:
                senha_valida, senha_msg = validar_senha(password)
                if senha_valida:
                    st.success(f"{senha_msg}")
                else:
                    st.warning(f"{senha_msg}")

            st.divider()
            termos = st.checkbox(
                "✓ Eu aceito os termos de uso e política de privacidade",
                help="Você deve concordar com os termos para prosseguir"
            )
            submit = st.form_submit_button(
                "Criar Minha Conta",
                width='stretch',
                type="primary"
            )

            if submit:
                # Validações de erros
                erros = []

                if not name or len(name.strip()) < 2:
                    erros.append("Nome deve ter pelo menos 2 caracteres")

                if not user or len(user.strip()) < 3:
                    erros.append(
                        "Nome de usuário deve ter pelo menos 3 caracteres")

                if not email or not validar_email(email):
                    erros.append("Email inválido")

                if not password:
                    erros.append("Senha é obrigatória")
                elif not validar_senha(password)[0]:
                    erros.append(f"{validar_senha(password)[1]}")

                if password != confirm_pw:
                    erros.append("As senhas não coincidem")

                if not termos:
                    erros.append("Você deve aceitar os termos de uso")

                if len(generos_selecao) != 3:
                    erros.append("Por favor, selecione 3 gêneros")

                if erros:
                    st.error("**Corrija os seguintes problemas:**")
                    for erro in erros:
                        st.markdown(f"- {erro}")
                else:
                    with st.spinner("Criando sua conta..."):
                        payload = {
                            "user": user.strip(),
                            "name": name.strip(),
                            "email": email.strip().lower(),
                            "password": password,
                            "generos_fav": generos_selecao
                        }

                        status_code, response = cadastrar_usuario(payload)

                        if status_code == 200 and response.get("success"):
                            st.session_state["novo_usuario"] = user
                            st.success("Conta criada com sucesso!")
                            st.switch_page("pages/sucesso.py")

                        else:
                            error_msg = response.get(
                                "message", "Erro desconhecido")
                            if status_code == 409:
                                st.error(
                                    "###### Nome de usuário já existe!\n\n"
                                    "Tente outro nome de usuário."
                                )
                            elif status_code == 401:
                                st.error(
                                    "###### Email já cadastrado!\n\n"
                                    "Use outro email ou faça login."
                                )
                            else:
                                st.error(
                                    f"###### Erro ao criar conta:\n{error_msg}"
                                    )

    # Seção de ajuda
    with st.expander("💡 Precisa de ajuda?"):
        col_help1, col_help2 = st.columns(2)

        with col_help1:
            st.markdown("""
            ** Dicas para criar sua conta:**

            • **Nome de usuário:** Único, usado para login\n
            • **Senha forte:** Mínimo 6 caracteres (letras + números)\n
            • **Email válido:** Para recuperação de senha\n
            • **Gêneros:** Escolha 3 para personalizar recomendações
            """)

        with col_help2:
            st.markdown("""
            ** Problemas comuns:**

            • Usuário existe → Tente outro nome\n
            • Email inválido → Use formato válido\n
            • Senhas diferentes → Digite igual nos dois campos\n
            • Poucos gêneros → Selecione exatamente 3\n
            """)


# Executa o código
if __name__ == "__main__":
    main()

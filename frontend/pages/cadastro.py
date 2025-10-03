import streamlit as st
import requests
from utils.utils import validar_senha, validar_email, setup_page

setup_page(titulo="Cadastro", hide_sidebar=True)

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

    # Header do front-end
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("Voltar", help="Voltar para o login"):
            st.switch_page("app.py")

    with col_title:
        st.title("Criar Nova Conta")

    st.markdown("### Preencha seus dados para criar sua conta")

    # Formulário de cadastro
    with st.form("cadastro_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        lista_generos = [
            "Ação", "Aventura", "Comédia", "Drama", "Fantasia", "Ficção",
            "Guerra", "Musical", "Romance", "Suspense", "Terror", "Animação"
        ]

        with col1:
            name = st.text_input(
                "Nome Completo",
                placeholder="Digite seu nome completo",
                help="Nome que será exibido no sistema"
            )
            email = st.text_input(
                "Email",
                placeholder="seu@email.com",
                help="Email válido para contato"
            )

        with col2:
            user = st.text_input(
                "Nome de Usuário",
                placeholder="Digite um nome para ser seu usuário",
                help="Nome usado para fazer login"
            )
            generos_selecao = st.multiselect(
                "Gêneros favoritos (escolha três)",
                options=lista_generos,
                placeholder="Escolha três opções",
            )

        password = st.text_input(
            "Senha",
            type="password",
            placeholder="Mínimo 6 caracteres",
            help="Senha deve conter letras e números"
        )

        confirm_pw = st.text_input(
            "Confirmar Senha",
            type="password",
            placeholder="Digite a senha novamente"
        )

        # Validação de senha em tempo real
        senha_valida, senha_msg = validar_senha(password) if password else (False, "")
        if password:
            if senha_valida:
                st.success(f"{senha_msg}")
            else:
                st.warning(f"{senha_msg}")

        # Checkbox de termos
        termos = st.checkbox(
            "Eu aceito os termos de uso e política de privacidade",
            help="Você deve concordar para prosseguir"
        )

        # Botão de submit (dentro do form)
        submit = st.form_submit_button(
            "Criar Conta",
            use_container_width=True,
        )

        if submit:
            # Validações de erros
            erros = []

            if not name or len(name.strip()) < 2:
                erros.append("Nome deve ter pelo menos 2 caracteres")

            if not user or len(user.strip()) < 3:
                erros.append("Nome de usuário deve ter pelo menos 3 caracteres")

            if not email or not validar_email(email):
                erros.append("Email inválido")

            if not password:
                erros.append("Senha é obrigatória")
            elif not senha_valida:
                erros.append(senha_msg)

            if password != confirm_pw:
                erros.append("As senhas não coincidem")

            if not termos:
                erros.append("Você deve aceitar os termos de uso")

            if len(generos_selecao) != 3:
                erros.append("Por favor, selecione 3 gêneros.")

            # Mostrar erros ou processar cadastro
            if erros:
                st.error("Corrija os seguintes problemas:")
                st.markdown("\n".join([f"- {erro}" for erro in erros]))
            else:
                payload = {
                    "user": user.strip(),
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "password": password,
                    "generos_fav": generos_selecao
                }

                status_code, response = cadastrar_usuario(payload)

                if status_code == 200 and response.get("success"):
                    # Cadastra o usuário com sucesso
                    st.session_state["novo_usuario"] = user

                    # Redireciona para página de sucesso
                    st.switch_page("pages/sucesso.py")

                else:
                    error_msg = response.get("message", "Erro desconhecido")
                    if status_code == 409:
                        st.error("**Nome de usuário já existe!**\n\nTente outro nome de usuário.")
                    if status_code == 401:
                        st.error("**Email já cadastrado!**")
                    else:
                        st.error(f"**Erro ao criar conta:**\n{error_msg}")

    # Seção de ajuda
    with st.expander("❓ Precisa de ajuda?"):
        st.markdown("""
        **Dicas para criar sua conta:**

        • **Nome de usuário:** Deve ser único, será usado para login
        • **Senha forte:** Use pelo menos 6 caracteres com letras e números
        • **Email válido:** Necessário para recuperação de senha

        **Problemas comuns:**
        • Nome de usuário já existe → Tente outro nome
        • Email inválido → Verifique o formato (exemplo@dominio.com)
        • Senhas não coincidem → Digite a mesma senha nos dois campos
        """)

    # Footer do front-end
    st.markdown("---")
    st.caption("Recomendação de Filmes | Já tem conta? Faça login!")


# Executa o código
if __name__ == "__main__":
    main()

# Rotacine - Sistema de recomendação de filmes

Uma plataforma web projetada para oferecer recomendações de filmes personalizadas. O sistema conta com um backend robusto em Flask para gerenciamento de usuários e dados, um frontend interativo construído com Streamlit, e um ambiente de desenvolvimento encapsulado com Docker para fácil configuração.

### Funcionalidades:

Atualmente, o projeto conta com as seguintes funcionalidades: 
* **Autenticação de usuário**: Sistema seguro de login e gerenciamento de sessão com JSON Web Tokens (JWT).
* **Cadastro de novos usuários**: Permite que novos usuários se registrem, fornecendo suas credenciais e preferências de gênero de filmes.
* **Segurança de senhas**: Senhas armazenadas de forma segura
* **Recuperação de senhas**: Funcionalidade de "Esqueci minha senha" que envia um link de redefinição por email
* **Busca de filmes**: Permite que usuários pesquisem em um catálogo de milhares de filmes.
* **Sistema de favoritos**:Usuários autenticados podem adicionar, visualizar e remover filmes de sua lista de favoritos pessoal.

### Tecnologias Utilizadas

Este projeto por enquanto está dividido em duas partes principais, o backend e o frontend.

**Backend**
* Linguagem Python 3.11
* Framework Flask
* Banco de dados com SQLAlchemy com PostgreSQL (via docker)
* Segurança com Werkzeug (hashing de senhas)
* Ambiente: Docker & Docker Compose

**Frontend**
* Linguagem Python 3.11
* Framework Streamlit
* Comunicação com a API Flask

### Como executar o projeto?

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**Pré-requisitos:**
* Git
* Docker Desktop instalado e em execução
* Python 3.11+ (apenas para frontend, em breve dockerizado)

Você não precisará do PostgreSQL instalado em sua máquina.

## Configuração do Backend

**1. Clonar o repositório**
```
git clone https://github.com/MatheusMoreiraS/RecomendarFilmes
```

**2. Configurar as Variáveis de Ambiente**
A aplicação usa um arquivo .env para gerenciar senhas e chaves de API. Nós fornecemos um modelo para você começar.
```
# No Windows (Prompt de Comando ou PowerShell):
copy .env.example .env

# No macOS/Linux ou Git Bash:
cp .env.example .env
```
Abra o arquivo .env em um editor de código. Para o desenvolvimento, os valores padrão do banco de dados já devem funcionar. Se quiser testar a funcionalidade de redefinição de senha, preencha as variáveis de email (EMAIL_USER, EMAIL_PASSWORD, etc.)

**3. Iniciar com Docker Compose**
```
docker-compose up --build
```

_Dica, para ativar e verificar senhas de app: https://support.google.com/accounts/answer/185833?hl=pt-br_

## Configuração do frontend
```
# Navegue até a pasta do backend
cd RecomendarFilmes/frontend

# Crie e ative o ambiente virtual
python -m venv venv
# No windows > venv\Scripts\activate
# No macOS > venv\bin\activate

# Instale as dependências
pip install -r requirements.txt
```

## Executando a aplicação

**Terminal 2 - Com o frontend**
```
# Navegue até a pasta /frontend
# Ative o ambiente virtual

# Inicie a aplicação Streamlit

streamlit run app.py

# A aplicação irá rodar automaticamente no seu computador.
```

### Endpoints da API

A API do backend possui os seguintes endpoints. Rotas protegidas requerem um Token JWT no cabeçalho de autorização.
```
Endpoint	        Método	     Descrição	

/status	          GET	       Verifica se a API está online	
/login	          POST	       Autentica um usuário
/cadastro	      POST	       Registra um novo usuário
/reset_senha      POST         Inicia o processo de redefinição de senha
/redefinir	      POST	       Confirma a senha com um token válido
/filmes/pesquisar GET	       Busca filmes no banco de dados
/favoritos        GET	       Adiciona um filme à lista de favoritos do usuário.
/favoritos/<tmdb_id>GET	       Remove um filme da lista de favoritos do usuário.
```

Novas funcionalidades em construção

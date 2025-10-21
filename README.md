# RotaCine - Recomendação de filmes

Plataforma para oferecer recomendações de filmes personalizadas com aprendizado de máquina.

### Funcionalidades:

* **Autenticação de usuário**
* **Cadastro de novos usuários**
* **Segurança de senhas**
* **Recuperação de senhas**
* **Busca de filmes**
* **Sistema de favoritos**

### Tecnologias:

**Backend**
* Python 3.11
* Flask
* SQLAlchemy com PostgreSQL (via docker)
* Werkzeug
* Docker & Docker Compose

**Frontend**
* Python 3.11
* Streamlit

### Como executar o projeto?

Siga os passos abaixo para configurar e executar localmente.

**Pré-requisitos:**
* Git
* Docker Desktop instalado e em execução
* Python 3.11+ (apenas para o frontend, em breve dockerizado)

PostgreSQL não é necessário.

## Configuração do Backend e Docker

**1. Clone o repositório**
```
git clone https://github.com/matheusmoreiras/RecomendarFilmes
```

**2. Configure o .env**

```
# no Windows (CMD ou PowerShell) navegue até a pasta do clone:
$ cd RecomendarFilmes
$ copy .env.example .env

# No macOS/Linux ou Git Bash:
$ cp .env.example .env
```
Abra o arquivo .env em um editor de código. Os valores padrão do banco de dados já devem funcionar. Se quiser testar a redefinição de senha, preencha as variáveis de email.

_Para ativar e verificar senhas de app: https://support.google.com/accounts/answer/185833?hl=pt-br_

**3. Inicie com Docker Compose**
```
$ docker-compose up --build

# Docker desktop deve estar em execução.
```

## Configuração do frontend
```
# Navegue até a pasta do backend
$ cd RecomendarFilmes/frontend

# Crie e ative o ambiente virtual
$ python -m venv venv
# No windows > $ venv\Scripts\activate
# No macOS > $ venv\bin\activate

# Instale as dependências
pip install -r requirements.txt
```

## Execute a aplicação

**Terminal 1 - Docker**
```
# No terminal, navegue até a pasta RecomendarFilmes, com Docker Desktop aberto
$ docker-compose up
```

**Terminal 2 - Frontend**
```
# Navegue até a pasta /frontend
# Ative o ambiente virtual

# Inicie a aplicação

$ streamlit run app.py

# A aplicação iniciará em seu navegador.
```

### Endpoints da API

Rotas protegidas requerem um Token JWT no cabeçalho de autorização. Rotas do Flask;
```
Endpoint	        Método	     Descrição	

/status	               GET	       Verifica se a API está online	
/login	               POST	       Autentica um usuário
/cadastro	           POST	       Cadastra um novo usuário
/reset_senha           POST        Solicita a redefinição de senha
/redefinir	           POST	       Redefine a senha (com token válido)
/filmes/pesquisar      GET	       Busca filmes no banco de dados
/favoritos             GET	       Adiciona um filme à lista de favoritos do usuário.
/favoritos/<tmdb_id>   GET	       Remove um filme da lista de favoritos do usuário.
```

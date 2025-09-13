# Rotacine - Sistema de recomendação de filmes

Uma plataforma web projetada para oferecer recomendações de filmes personalizadas com aprendizado de máquina. O sistema conta com um backend robusto em Flask para gerenciamento de usuários e dados, e um frontend interativo construído com Streamlit.

### Funcionalidades:

Atualmente, o projeto conta com as seguintes funcionalidades: 
* **Autenticação de usuário**: Sistema seguro de login para acesso ao site.
* **Cadastro de novos usuários**: Permite que novos usuários se registrem, fornecendo suas credenciais e preferências de gênero de filmes.
* **Segurança de senhas**: Senhas armazenadas de forma segura
* **Recuperação de senhas**: Funcionalidade de "Esqueci minha senha" que envia um link de redefinição por email

### Tecnologias Utilizadas

Este projeto por enquanto está dividido em duas partes principais, o backend e o frontend.

**Backend**
* Linguagem Python 3.11
* Framework Flask
* Banco de dados com SQLAlchemy com PostgreSQL (via docker)
* Segurança com Werkzeug (hashing de senhas)

**Frontend**
* Linguagem Python 3.11
* Framework Streamlit
* Comunicação com a API Flask

### Como executar o projeto?

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**Pré-requisitos:**
* Python 3.11 ou superior
* Git
* Docker Desktop

## Configuração do Backend

**1. Clonar o repositório**
```
git clone https://github.com/MatheusMoreiraS/RecomendarFilmes
```

**2. Crie e ative um ambiente virtual**
```
# Navegue até a pasta do backend
cd RecomendarFilmes/backend

# Crie e ative o ambiente virtual
python -m venv venv
# No windows > venv\Scripts\activate
# No macOS > venv\bin\activate
```

**3. Instale as dependências**
```
pip install -r requirements .txt
```

**4. Configure o banco de dados**

O projeto utiliza um banco de dados em PostgreSQL rodando em um contâiner Docker, execute o comando abaixo no seu terminal, para baixar a imagem do PostgreSQL caso você não tiver, e iniciar um contâiner.
```
docker run --name nome-do-db -e POSTGRES_PASSWORD=sua_senha -p 5432:5432 -d postgres

# Para iniciar o containêr após desligá-lo, pode iniciar novamente com o comando:
docker start nome-do-db
```

**5. Variáveis de ambiente**

O backend precisa de algumas chaves e credenciais para funcionar, dentro da pasta backend crie um arquivo chamado .env e copie o conteúdo do env.example no repositório, seguindo o exemplo:
```
# Banco de dados
DATABASE_URL="postgresql://postgres:suasenha@localhost:5432/postgres"

# Email
EMAIL_USER="@gmail.com"
EMAIL_PASSWORD="sua_senha_de_app"

# Server
SMTP_SERVER=""
SMTP_PORT=""

# Flask

FLASK_ENV=""
SECRET_KEY=""

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

Você precisará de dois terminais para rodar o backend e o frontend simultaneamente.

**Terminal 1 - Com o backend**
```
# Navegue até a pasta /backend
# Ative o ambiente virtual

# Inicie o servidor flask
python apy.py

# O backend está funcionando na rota http://127.0.0.1:5000
```
Ao iniciar o código pela primeira vez, as tabelas do banco de dados serão criadas automaticamente no contâiner Docker.

**Terminal 2 - Com o frontend**
```
# Navegue até a pasta /frontend
# Ative o ambiente virtual

# Inicie a aplicação Streamlit

streamlit run app.py

# A aplicação irá rodar automaticamente no seu computador.
```

###Endpoints da API

A API do backend possui os seguintes endpoints:
```
Endpoint	        Método	     Descrição	

/status	          GET	       Verifica se a API está online	
/login	          POST	       Autentica um usuário
/cadastro	      POST	       Registra um novo usuário
/reset_senha      POST         Inicia o processo de redefinição de senha
/redefinir	      POST	       Confirma a senha com um token válido
/mock             GET          # Teste, retorna uma lista de filmes de exemplo
```

NOVAS FUNCIONALIDADES EM CONSTRUÇÃO

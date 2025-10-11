# Use uma imagem oficial do Python como base
FROM python:3.11.1

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de dependências primeiro
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o codigo
COPY . .

# Cmd para rodar o container
CMD ["flask", "--app", "apy", "run", "--host=0.0.0.0"]
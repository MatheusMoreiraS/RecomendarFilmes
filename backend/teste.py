import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')
ID_MOVIE = 7459

url = f"https://api.themoviedb.org/3/movie/{ID_MOVIE}"

# 2. Define os parâmetros da requisição (query parameters)
params = {
    'api_key': API_KEY,
    'language': 'pt-BR'  # Parâmetro opcional para receber a resposta em português
}

print(f"Fazendo uma requisição GET para: {url}")

try:
    # 3. Faz a requisição GET
    response = requests.get(url, params=params)

    # Lança uma exceção se a resposta for um erro (ex: 401, 404)
    response.raise_for_status()

    # 4. Converte a resposta em um dicionário Python (JSON)
    dados_do_filme = response.json()

    # 5. Exibe os dados de forma legível
    print("\n--- RESPOSTA DA API ---")
    # O 'indent=2' formata o JSON para facilitar a leitura
    print(json.dumps(dados_do_filme, indent=2, ensure_ascii=False))

except requests.RequestException as e:
    print(f"\nOcorreu um erro na requisição: {e}")

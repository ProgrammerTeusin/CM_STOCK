import os
from dotenv import load_dotenv

load_dotenv()

# Configurações gerais da aplicação carregadas via variáveis de ambiente.
# A conexão em si (engine/sessão) fica isolada em app/database/conexao.py;
# aqui ficam apenas parâmetros de comportamento da API.

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "ERRO CRÍTICO DE INFRAESTRUTURA:\n"
        "A variável de ambiente 'DATABASE_URL' não foi encontrada no arquivo .env!\n"
        "Copie o arquivo .env.example para .env e ajuste com a sua conexão do SQL Server."
    )

# Paginação padrão usada nas listagens (produtos, endereços)
PAGINACAO_TAMANHO_PADRAO = int(os.getenv("PAGINACAO_TAMANHO_PADRAO", 10))
PAGINACAO_TAMANHO_MAXIMO = int(os.getenv("PAGINACAO_TAMANHO_MAXIMO", 100))

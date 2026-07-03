import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

URL_BANCO = os.getenv("DATABASE_URL")

if not URL_BANCO:
    raise ValueError(
        "ERRO CRÍTICO DE INFRAESTRUTURA:\n"
        "A variável de ambiente 'DATABASE_URL' não foi encontrada no arquivo .env!\n"
        "Copie o arquivo .env.example para .env e ajuste com a sua conexão do SQL Server."
    )

motor = create_engine(URL_BANCO)
SessionLocal = sessionmaker(bind=motor)


#  Paginação padrão usada nas listagens (produtos, endereços)
PAGINACAO_TAMANHO_PADRAO = int(os.getenv("PAGINACAO_TAMANHO_PADRAO", 10))
PAGINACAO_TAMANHO_MAXIMO = int(os.getenv("PAGINACAO_TAMANHO_MAXIMO", 100))

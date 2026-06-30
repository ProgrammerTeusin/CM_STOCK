import os
from dotenv import load_dotenv
import pyodbc


load_dotenv()

class Config:
    """Configurações centrais da aplicação carregadas via variáveis de ambiente."""
    
    # Desativa o rastreamento de modificações do ORM para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError(
            "ERRO CRÍTICO DE INFRAESTRUTURA:\n"
            "A variável de ambiente 'DATABASE_URL' não foi encontrada no arquivo .env!\n"
            "Por favor, configure a string de conexão com o seu SQL Server local antes de iniciar."
        )

if __name__ == "__main__":
    print(pyodbc.drivers())
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

URL_BANCO = os.getenv("DATABASE_URL")

if not URL_BANCO:
    raise ValueError("Erro no arquivo .env")

motor = create_engine(URL_BANCO)
SessionLocal = sessionmaker(bind=motor)


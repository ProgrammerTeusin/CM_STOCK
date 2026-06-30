from app.database.base import Base
from app.database.conexao import motor

from app.Model import Produto
from app.Model import Contagem
from app.Model import Endereco

def criar_todas_tabelas():
    Base.metadata.create_all(bind=motor)
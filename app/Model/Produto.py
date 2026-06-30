from sqlalchemy import Column, Integer, String
from app.database.base import Base
from sqlalchemy.orm import relationship

class Produto(Base):

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), nullable=False)
    descricao = Column(String(300), nullable=False)
    unidade = Column(String(10), nullable=False)

    contagens = relationship("Contagem",back_populates="produto")

    def converter_dict(self):
        return {
            "id":self.id,
            "sku":self.sku,
            "descricao":self.descricao,
            "unidade":self.unidade
        }

    
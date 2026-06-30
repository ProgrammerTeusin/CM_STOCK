from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Contagem(Base):
    __tablename__ = "contagens"

    id = Column(Integer, primary_key=True, autoincrement=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.id"), nullable=False)

    quantidade = Column(Integer, nullable=False)
    usuario = Column(String(100), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow)

    produto = relationship("Produto", back_populates="contagens")
    endereco = relationship("Endereco", back_populates="contagem")

    def converter_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "endereco_id": self.endereco_id,
            "quantidade": self.quantidade,
            "usuario": self.usuario,
            "data_hora": self.data_hora.isoformat()
        }
    
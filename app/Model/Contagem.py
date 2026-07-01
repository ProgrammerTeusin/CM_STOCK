from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Contagem(Base):
    __tablename__ = "contagens"

    id = Column(Integer, primary_key=True, autoincrement=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=False)

    quantidade = Column(Integer, nullable=False)
    usuario = Column(String(100), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    produto = relationship("Produto", back_populates="contagens")
    endereco = relationship("Endereco", back_populates="contagens")

    def converter_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "endereco_id": self.endereco_id,
            "sku": self.produto.sku if self.produto else None,
            "endereco": self.endereco.endereco if self.endereco else None,
            "quantidade": self.quantidade,
            "usuario": self.usuario,
            "data_hora": self.data_hora.isoformat()
        }

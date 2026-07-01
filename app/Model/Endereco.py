from sqlalchemy import Column, String, Integer
from app.database.base import Base
from sqlalchemy.orm import relationship

class Endereco(Base):

    __tablename__ = "enderecos"

    id = Column(Integer, autoincrement=True, primary_key=True)
    endereco = Column(String(50), nullable=False, unique=True)
    descricao = Column(String(250))

    contagens = relationship("Contagem", back_populates="endereco")

    def converter_dict(self):
        return {
            "id": self.id,
            "endereco": self.endereco,
            "descricao": self.descricao or ""
        }

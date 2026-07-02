from app.Model.Endereco import Endereco


class Endereco_Repositorio():

    def __init__(self, sessao):
        self.sessao = sessao

    def salvar(self, endereco):
        self.sessao.add(endereco)
        return endereco

    def remover(self, endereco):
        self.sessao.delete(endereco)

    def buscar_por_codigo(self, codigo):
        return self.sessao.query(Endereco).filter_by(endereco=codigo).first()

    def buscar_por_id(self, endereco_id):
        return self.sessao.query(Endereco).filter_by(id=endereco_id).first()

    def listar(self, pagina, tamanho_pagina):
        consulta = self.sessao.query(Endereco).order_by(Endereco.endereco)
        total = consulta.count()
        itens = consulta.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()
        return itens, total

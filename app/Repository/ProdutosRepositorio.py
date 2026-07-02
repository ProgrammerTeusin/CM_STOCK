from app.Model.Produto import Produto


class Produto_Repositorio():

    def __init__(self, sessao):
        self.sessao = sessao

    def salvar(self, produto):
        self.sessao.add(produto)
        return produto

    def remover(self, produto):
        self.sessao.delete(produto)

    def buscar_por_sku(self, sku):
        return self.sessao.query(Produto).filter_by(sku=sku).first()

    def buscar_por_id(self, produto_id):
        return self.sessao.query(Produto).filter_by(id=produto_id).first()

    def listar(self, pagina, tamanho_pagina):
        consulta = self.sessao.query(Produto).order_by(Produto.sku)
        total = consulta.count()
        itens = consulta.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina).all()
        return itens, total

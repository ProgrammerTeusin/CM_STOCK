from app.Repository.ProdutosRepositorio import Produto_Repositorio
from app.Model.Produto import Produto
from app.erros import ErroValidacao, ErroNaoEncontrado, ErroConflito


class Produto_Service():

    def __init__(self, sessao):
        self.sessao = sessao
        self.repositorio = Produto_Repositorio(sessao)

    def _validar_dados(self, dados):
        campos_obrigatorios = ["sku", "descricao", "unidade"]
        faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]

        if faltando:
            raise ErroValidacao(f"Campos obrigatórios ausentes: {', '.join(faltando)}")

    def criar(self, dados):
        self._validar_dados(dados)

        if self.repositorio.buscar_por_sku(dados["sku"]):
            raise ErroConflito(f"Já existe um produto com o SKU '{dados['sku']}'")

        produto = Produto(
            sku=dados["sku"],
            descricao=dados["descricao"],
            unidade=dados["unidade"]
        )

        self.repositorio.salvar(produto)
        self.sessao.commit()
        return produto

    def atualizar(self, sku, dados):
        produto = self.buscar_por_sku(sku)

        novo_sku = dados.get("sku", produto.sku)
        if novo_sku != produto.sku and self.repositorio.buscar_por_sku(novo_sku):
            raise ErroConflito(f"Já existe um produto com o SKU '{novo_sku}'")

        produto.sku = novo_sku
        produto.descricao = dados.get("descricao", produto.descricao)
        produto.unidade = dados.get("unidade", produto.unidade)

        self.sessao.commit()
        return produto

    def remover(self, sku):
        produto = self.buscar_por_sku(sku)
        self.repositorio.remover(produto)
        self.sessao.commit()

    def buscar_por_sku(self, sku):
        produto = self.repositorio.buscar_por_sku(sku)
        if not produto:
            raise ErroNaoEncontrado(f"Produto com SKU '{sku}' não encontrado")
        return produto

    def listar(self, pagina, tamanho_pagina):
        itens, total = self.repositorio.listar(pagina, tamanho_pagina)
        return itens, total

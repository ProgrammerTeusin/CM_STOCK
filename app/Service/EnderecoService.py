from app.Repository.EnderecosRepositorio import Endereco_Repositorio
from app.Model.Endereco import Endereco
from app.erros import ErroValidacao, ErroNaoEncontrado, ErroConflito


class Endereco_Service():

    def __init__(self, sessao):
        self.sessao = sessao
        self.repositorio = Endereco_Repositorio(sessao)

    def _validar_dados(self, dados):
        if not dados.get("endereco"):
            raise ErroValidacao("Campo obrigatório ausente: endereco")

    def criar(self, dados):
        self._validar_dados(dados)

        if self.repositorio.buscar_por_codigo(dados["endereco"]):
            raise ErroConflito(f"Já existe um endereço com o código '{dados['endereco']}'")

        endereco = Endereco(
            endereco=dados["endereco"],
            descricao=dados.get("descricao")
        )

        self.repositorio.salvar(endereco)
        self.sessao.commit()
        return endereco

    def atualizar(self, codigo, dados):
        endereco = self.buscar_por_codigo(codigo)

        novo_codigo = dados.get("endereco", endereco.endereco)
        if novo_codigo != endereco.endereco and self.repositorio.buscar_por_codigo(novo_codigo):
            raise ErroConflito(f"Já existe um endereço com o código '{novo_codigo}'")

        endereco.endereco = novo_codigo
        endereco.descricao = dados.get("descricao", endereco.descricao)

        self.sessao.commit()
        return endereco

    def remover(self, codigo):
        endereco = self.buscar_por_codigo(codigo)
        self.repositorio.remover(endereco)
        self.sessao.commit()

    def buscar_por_codigo(self, codigo):
        endereco = self.repositorio.buscar_por_codigo(codigo)
        if not endereco:
            raise ErroNaoEncontrado(f"Endereço '{codigo}' não encontrado")
        return endereco

    def listar(self, pagina, tamanho_pagina):
        itens, total = self.repositorio.listar(pagina, tamanho_pagina)
        return itens, total

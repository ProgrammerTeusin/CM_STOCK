from datetime import datetime, timezone

from app.Repository.ContagensRepositorio import Contagem_Repositorio
from app.Repository.ProdutosRepositorio import Produto_Repositorio
from app.Repository.EnderecosRepositorio import Endereco_Repositorio
from app.Model.Contagem import Contagem
from app.erros import ErroValidacao, ErroNaoEncontrado


class Contagem_Service():

    def __init__(self, sessao):
        self.sessao = sessao
        self.repositorio = Contagem_Repositorio(sessao)
        self.repositorio_produtos = Produto_Repositorio(sessao)
        self.repositorio_enderecos = Endereco_Repositorio(sessao)

    def registrar(self, dados):
        campos_obrigatorios = ["sku", "endereco", "quantidade", "usuario"]
        faltando = [campo for campo in campos_obrigatorios if dados.get(campo) in (None, "")]
        if faltando:
            raise ErroValidacao(f"Campos obrigatórios ausentes: {', '.join(faltando)}")

        try:
            quantidade = int(dados["quantidade"])
        except (TypeError, ValueError):
            raise ErroValidacao("Quantidade deve ser um número inteiro")

        if quantidade < 0:
            raise ErroValidacao("Quantidade não pode ser negativa")

        produto = self.repositorio_produtos.buscar_por_sku(dados["sku"])
        if not produto:
            raise ErroNaoEncontrado(f"Produto com SKU '{dados['sku']}' não encontrado")

        endereco = self.repositorio_enderecos.buscar_por_codigo(dados["endereco"])
        if not endereco:
            raise ErroNaoEncontrado(f"Endereço '{dados['endereco']}' não encontrado")

        contagem = Contagem(
            produto_id=produto.id,
            endereco_id=endereco.id,
            quantidade=quantidade,
            usuario=dados["usuario"],
            data_hora=datetime.now(timezone.utc)
        )

        self.repositorio.salvar(contagem)
        self.sessao.commit()
        return contagem

    def historico_por_sku(self, sku, data_inicio=None, data_fim=None):
        produto = self.repositorio_produtos.buscar_por_sku(sku)
        if not produto:
            raise ErroNaoEncontrado(f"Produto com SKU '{sku}' não encontrado")

        return self.repositorio.historico_por_produto(produto.id, data_inicio, data_fim)

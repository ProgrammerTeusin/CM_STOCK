from app.Repository.ContagensRepositorio import Contagem_Repositorio
from app.Repository.EnderecosRepositorio import Endereco_Repositorio
from app.erros import ErroNaoEncontrado


class Relatorio_Service():

    def __init__(self, sessao):
        self.sessao = sessao
        self.repositorio = Contagem_Repositorio(sessao)
        self.repositorio_enderecos = Endereco_Repositorio(sessao)

    def _buscar_endereco_ou_erro(self, codigo_endereco):
        endereco = self.repositorio_enderecos.buscar_por_codigo(codigo_endereco)
        if not endereco:
            raise ErroNaoEncontrado(f"Endereço '{codigo_endereco}' não encontrado")
        return endereco

    def saldo_por_endereco(self, codigo_endereco):
        endereco = self._buscar_endereco_ou_erro(codigo_endereco)
        linhas = self.repositorio.saldo_atual_por_endereco(endereco.id)

        return [
            {
                "sku": linha["sku"],
                "descricao": linha["descricao"],
                "unidade": linha["unidade"],
                "quantidade_atual": linha["quantidade"],
                "ultima_contagem_em": linha["data_hora"].isoformat()
            }
            for linha in linhas
        ]

    def divergencia_por_endereco(self, codigo_endereco):
        endereco = self._buscar_endereco_ou_erro(codigo_endereco)
        linhas = self.repositorio.duas_ultimas_contagens_por_endereco(endereco.id)

        agrupado = {}
        for linha in linhas:
            agrupado.setdefault(linha["produto_id"], []).append(linha)

        relatorio = []
        for produto_id, contagens in agrupado.items():
            # já vêm ordenadas por data_hora desc (ordem 1 = mais recente)
            contagens.sort(key=lambda linha: linha["ordem"])
            atual = contagens[0]

            if len(contagens) == 1:
                relatorio.append({
                    "sku": atual["sku"],
                    "descricao": atual["descricao"],
                    "quantidade_atual": atual["quantidade"],
                    "quantidade_anterior": None,
                    "diferenca": None,
                    "situacao": "sem_historico"
                })
                continue

            anterior = contagens[1]
            diferenca = atual["quantidade"] - anterior["quantidade"]

            if diferenca > 0:
                situacao = "aumento"
            elif diferenca < 0:
                situacao = "reducao"
            else:
                situacao = "estavel"

            relatorio.append({
                "sku": atual["sku"],
                "descricao": atual["descricao"],
                "quantidade_atual": atual["quantidade"],
                "quantidade_anterior": anterior["quantidade"],
                "diferenca": diferenca,
                "situacao": situacao
            })

        relatorio.sort(key=lambda item: item["sku"])
        return relatorio

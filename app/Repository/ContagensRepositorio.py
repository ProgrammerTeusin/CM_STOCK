from sqlalchemy import text

from app.Model.Contagem import Contagem
from app.Model.Produto import Produto


class Contagem_Repositorio():

    def __init__(self, sessao):
        self.sessao = sessao

    def salvar(self, contagem):
        self.sessao.add(contagem)
        return contagem

    def historico_por_produto(self, produto_id, data_inicio=None, data_fim=None):
        consulta = (
            self.sessao.query(Contagem)
            .filter(Contagem.produto_id == produto_id)
        )

        if data_inicio:
            consulta = consulta.filter(Contagem.data_hora >= data_inicio)
        if data_fim:
            consulta = consulta.filter(Contagem.data_hora <= data_fim)

        return consulta.order_by(Contagem.data_hora.desc()).all()

    # ------------------------------------------------------------------
    # Consulta em SQL puro (requisito obrigatório do teste).
    #
    # Usamos ROW_NUMBER() particionado por produto para, em uma única
    # ida ao banco, obter a última contagem de cada produto em um
    # endereço — isso seria bem mais custoso resolvido em Python
    # (buscaríamos todas as contagens e ordenaríamos em memória).
    # ------------------------------------------------------------------
    def saldo_atual_por_endereco(self, endereco_id):
        sql = text("""
            WITH ultimas_contagens AS (
                SELECT
                    c.produto_id,
                    c.quantidade,
                    c.data_hora,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.produto_id
                        ORDER BY c.data_hora DESC
                    ) AS ordem
                FROM contagens c
                WHERE c.endereco_id = :endereco_id
            )
            SELECT
                p.id AS produto_id,
                p.sku,
                p.descricao,
                p.unidade,
                u.quantidade,
                u.data_hora
            FROM ultimas_contagens u
            INNER JOIN produtos p ON p.id = u.produto_id
            WHERE u.ordem = 1
            ORDER BY p.sku
        """)

        resultado = self.sessao.execute(sql, {"endereco_id": endereco_id})
        return resultado.mappings().all()

    # ------------------------------------------------------------------
    # Consulta em SQL puro usada no relatório de divergência.
    #
    # Traz, para cada produto do endereço, as duas contagens mais
    # recentes já numeradas (ordem 1 = mais recente, ordem 2 =
    # penúltima). O cálculo do delta (atual - anterior) e a
    # classificação (aumento/redução/estável) ficam no Service,
    # em Python, pois envolvem regra de negócio, não apenas dado bruto.
    # ------------------------------------------------------------------
    def duas_ultimas_contagens_por_endereco(self, endereco_id):
        sql = text("""
            SELECT
                p.id AS produto_id,
                p.sku,
                p.descricao,
                c.quantidade,
                c.data_hora,
                ROW_NUMBER() OVER (
                    PARTITION BY c.produto_id
                    ORDER BY c.data_hora DESC
                ) AS ordem
            FROM contagens c
            INNER JOIN produtos p ON p.id = c.produto_id
            WHERE c.endereco_id = :endereco_id
        """)

        resultado = self.sessao.execute(sql, {"endereco_id": endereco_id})
        linhas = resultado.mappings().all()

        return [linha for linha in linhas if linha["ordem"] <= 2]

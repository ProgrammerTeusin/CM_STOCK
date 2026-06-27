from flask import Flask

from app.database.conexao import testar_conexao_banco


def criar_app():
    app = Flask(__name__)

    @app.get("/")
    def ola_mundo():
        return {
            "status": "sucesso",
            "mensagem": "Olá, Mundo! Fundação do projeto CM_STOCK (ETAPA GENESIS) iniciada com sucesso.",
            "projeto": "Controle de Estoque por Endereçamento",
            "vaga": "Analista de Sistemas"
        }
     #  CORREÇÃO: Força o Flask a aceitar caracteres em português (UTF-8) no JSON
    app.json.ensure_ascii = False

    @app.get("/teste-banco")
    def testando_banco():
        try:
            horario_banco = testar_conexao_banco()

            return {
                "mensagem": "Conexao com o SQL Server realizada com sucesso.",
                "horario_banco": str(horario_banco)
            }, 200

        except Exception as erro:
            return {
                "mensagem": "Falha ao conectar com o SQL Server.",
                "erro": str(erro)
            }, 500

    return app
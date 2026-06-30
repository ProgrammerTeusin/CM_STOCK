from flask import Flask

from seed import executar_seed

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

    @app.route("/seed", methods=["GET","POST"])
    def seed():
        """Essa foi usada para Teste, se achar melhor execute diretamente o seed por meio de python seed.py"""
        try:
           if executar_seed():
                return {
                    "mensagem": "Tabelas principais criada com Sucesso.",
                    "Situação": "Dados inseridos com sucessos em seed"
                }, 200
           else:
               return {
                   "mensagem":"Dados não salvos"
               },500

        except Exception as erro:
            return {
                "mensagem": "Falha ao conectar com o SQL Server.",
                "erro": str(erro)
            }, 500

    return app
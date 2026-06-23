from flask import Flask


def criar_app():
    """Fábrica do Aplicativo (Application Factory)"""
    app = Flask(__name__)
    

    # ROTA INICIAL DE TESTE: Retorna um JSON de boas-vindas estruturado
    @app.route("/")
    def ola_mundo():
        return {
            "status": "sucesso",
            "mensagem": "Olá, Mundo! Fundação do projeto CM_STOCK (ETAPA GENESIS) iniciada com sucesso.",
            "projeto": "Controle de Estoque por Endereçamento",
            "vaga": "Analista de Sistemas"
        }
     #  CORREÇÃO: Força o Flask a aceitar caracteres em português (UTF-8) no JSON
    app.json.ensure_ascii = False
    return app

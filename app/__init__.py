from flask import Flask, jsonify

from app.erros import ErroDeNegocio


def criar_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False

    registrar_blueprints(app)
    registrar_tratamento_de_erros(app)

    return app


def registrar_blueprints(app):
    from app.Controller.web_controller import web_bp
    from app.Controller.produtos_controller import produtos_bp
    from app.Controller.enderecos_controller import enderecos_bp
    from app.Controller.contagens_controller import contagens_bp
    from app.Controller.relatorios_controller import relatorios_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(enderecos_bp)
    app.register_blueprint(contagens_bp)
    app.register_blueprint(relatorios_bp)


def registrar_tratamento_de_erros(app):
    """Tratamento de erros centralizado da API.

    Qualquer ErroDeNegocio levantado nos Services (validação, não
    encontrado, conflito) cai aqui e é convertido numa resposta JSON
    padronizada, com o status HTTP correto. Erros inesperados (bugs)
    também retornam um JSON consistente em vez de estourar HTML de debug.
    """

    @app.errorhandler(ErroDeNegocio)
    def tratar_erro_de_negocio(erro):
        return jsonify({"erro": erro.mensagem}), erro.status_code

    @app.errorhandler(404)
    def tratar_nao_encontrado(erro):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def tratar_metodo_nao_permitido(erro):
        return jsonify({"erro": "Método não permitido para esta rota"}), 405

    @app.errorhandler(Exception)
    def tratar_erro_inesperado(erro):
        app.logger.exception(erro)
        return jsonify({"erro": "Erro interno inesperado. Consulte os logs do servidor."}), 500

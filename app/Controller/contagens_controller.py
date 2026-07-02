from flask import Blueprint, request, jsonify

from app.database.conexao import SessionLocal
from app.Service.ContagemService import Contagem_Service

contagens_bp = Blueprint("contagens", __name__, url_prefix="/api/contagens")


@contagens_bp.route("", methods=["POST"])
def registrar():
    sessao = SessionLocal()
    try:
        dados = request.get_json(force=True, silent=True) or {}
        servico = Contagem_Service(sessao)
        contagem = servico.registrar(dados)
        return jsonify(contagem.converter_dict()), 201
    finally:
        sessao.close()


@contagens_bp.route("/produto/<sku>", methods=["GET"])
def historico(sku):
    sessao = SessionLocal()
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        servico = Contagem_Service(sessao)
        contagens = servico.historico_por_sku(sku, data_inicio, data_fim)

        return jsonify([contagem.converter_dict() for contagem in contagens])
    finally:
        sessao.close()

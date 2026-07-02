from flask import Blueprint, jsonify

from app.database.conexao import SessionLocal
from app.Service.RelatorioService import Relatorio_Service

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/api/relatorios")


@relatorios_bp.route("/saldo/<codigo_endereco>", methods=["GET"])
def saldo(codigo_endereco):
    sessao = SessionLocal()
    try:
        servico = Relatorio_Service(sessao)
        resultado = servico.saldo_por_endereco(codigo_endereco)
        return jsonify(resultado)
    finally:
        sessao.close()


@relatorios_bp.route("/divergencia/<codigo_endereco>", methods=["GET"])
def divergencia(codigo_endereco):
    sessao = SessionLocal()
    try:
        servico = Relatorio_Service(sessao)
        resultado = servico.divergencia_por_endereco(codigo_endereco)
        return jsonify(resultado)
    finally:
        sessao.close()

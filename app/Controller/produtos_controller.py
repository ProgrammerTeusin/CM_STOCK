from flask import Blueprint, request, jsonify

from app.database.conexao import SessionLocal
from app.Service.ProdutoService import Produto_Service
from app import config

produtos_bp = Blueprint("produtos", __name__, url_prefix="/api/produtos")


@produtos_bp.route("", methods=["GET"])
def listar():
    sessao = SessionLocal()
    try:
        pagina = int(request.args.get("pagina", 1))
        tamanho_pagina = min(
            int(request.args.get("tamanho_pagina", config.PAGINACAO_TAMANHO_PADRAO)),
            config.PAGINACAO_TAMANHO_MAXIMO
        )

        servico = Produto_Service(sessao)
        itens, total = servico.listar(pagina, tamanho_pagina)

        return jsonify({
            "pagina": pagina,
            "tamanho_pagina": tamanho_pagina,
            "total": total,
            "itens": [item.converter_dict() for item in itens]
        })
    finally:
        sessao.close()


@produtos_bp.route("/<sku>", methods=["GET"])
def buscar(sku):
    sessao = SessionLocal()
    try:
        servico = Produto_Service(sessao)
        produto = servico.buscar_por_sku(sku)
        return jsonify(produto.converter_dict())
    finally:
        sessao.close()


@produtos_bp.route("", methods=["POST"])
def criar():
    sessao = SessionLocal()
    try:
        dados = request.get_json(force=True, silent=True) or {}
        servico = Produto_Service(sessao)
        produto = servico.criar(dados)
        return jsonify(produto.converter_dict()), 201
    finally:
        sessao.close()


@produtos_bp.route("/<sku>", methods=["PUT"])
def atualizar(sku):
    sessao = SessionLocal()
    try:
        dados = request.get_json(force=True, silent=True) or {}
        servico = Produto_Service(sessao)
        produto = servico.atualizar(sku, dados)
        return jsonify(produto.converter_dict())
    finally:
        sessao.close()


@produtos_bp.route("/<sku>", methods=["DELETE"])
def remover(sku):
    sessao = SessionLocal()
    try:
        servico = Produto_Service(sessao)
        servico.remover(sku)
        return "", 204
    finally:
        sessao.close()

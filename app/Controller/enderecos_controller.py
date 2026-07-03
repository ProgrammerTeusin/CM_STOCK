from flask import Blueprint, request, jsonify

from app.database import conexao
from app.Service.EnderecoService import Endereco_Service


enderecos_bp = Blueprint("enderecos", __name__, url_prefix="/api/enderecos")


@enderecos_bp.route("", methods=["GET"])
def listar():
    sessao = conexao.SessionLocal()
    try:
        pagina = int(request.args.get("pagina", 1))
        tamanho_pagina = min(
            int(request.args.get("tamanho_pagina", conexao.PAGINACAO_TAMANHO_PADRAO)),
            conexao.PAGINACAO_TAMANHO_MAXIMO
        )

        servico = Endereco_Service(sessao)
        itens, total = servico.listar(pagina, tamanho_pagina)

        return jsonify({
            "pagina": pagina,
            "tamanho_pagina": tamanho_pagina,
            "total": total,
            "itens": [item.converter_dict() for item in itens]
        })
    finally:
        sessao.close()


@enderecos_bp.route("/<codigo>", methods=["GET"])
def buscar(codigo):
    sessao = SessionLocal()
    try:
        servico = Endereco_Service(sessao)
        endereco = servico.buscar_por_codigo(codigo)
        return jsonify(endereco.converter_dict())
    finally:
        sessao.close()


@enderecos_bp.route("", methods=["POST"])
def criar():
    sessao = SessionLocal()
    try:
        dados = request.get_json(force=True, silent=True) or {}
        servico = Endereco_Service(sessao)
        endereco = servico.criar(dados)
        return jsonify(endereco.converter_dict()), 201
    finally:
        sessao.close()


@enderecos_bp.route("/<codigo>", methods=["PUT"])
def atualizar(codigo):
    sessao = SessionLocal()
    try:
        dados = request.get_json(force=True, silent=True) or {}
        servico = Endereco_Service(sessao)
        endereco = servico.atualizar(codigo, dados)
        return jsonify(endereco.converter_dict())
    finally:
        sessao.close()


@enderecos_bp.route("/<codigo>", methods=["DELETE"])
def remover(codigo):
    sessao = SessionLocal()
    try:
        servico = Endereco_Service(sessao)
        servico.remover(codigo)
        return "", 204
    finally:
        sessao.close()

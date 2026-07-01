from flask import Flask, request, render_template

from app.database.conexao import SessionLocal
from app.Model.Produto import Produto
from app.Repository.ProdutosRepositorio import Produto_Repositorio

def criar_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.route("/")
    def principal():
        return render_template("index.html")

    @app.route("/salvar", methods=["POST"])
    def salvar():

        dados = request.get_json()

        sessao = SessionLocal()

        try:
            repositorio = Produto_Repositorio(sessao)

            produto = Produto(
                sku=dados["sku"],
                descricao=dados["descricao"],
                unidade=dados["unidade"]
            )

            repositorio.salvar(produto)

            return {
                "mensagem": "Produto salvo com sucesso"
            }, 201

        finally:
            sessao.close()

    return app
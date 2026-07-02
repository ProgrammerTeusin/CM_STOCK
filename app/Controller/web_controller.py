from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def inicio():
    return render_template("index.html")


@web_bp.route("/produtos")
def produtos():
    return render_template("produtos.html")


@web_bp.route("/produtos/novo")
def produto_novo():
    return render_template("produto_form.html", sku=None)


@web_bp.route("/produtos/<sku>/editar")
def produto_editar(sku):
    return render_template("produto_form.html", sku=sku)


@web_bp.route("/enderecos")
def enderecos():
    return render_template("enderecos.html")


@web_bp.route("/enderecos/novo")
def endereco_novo():
    return render_template("endereco_form.html", codigo=None)


@web_bp.route("/enderecos/<codigo>/editar")
def endereco_editar(codigo):
    return render_template("endereco_form.html", codigo=codigo)


@web_bp.route("/contagens/nova")
def contagem_nova():
    return render_template("contagem_form.html")


@web_bp.route("/relatorios/saldo")
def relatorio_saldo():
    return render_template("saldo.html")


@web_bp.route("/relatorios/divergencia")
def relatorio_divergencia():
    return render_template("divergencia.html")

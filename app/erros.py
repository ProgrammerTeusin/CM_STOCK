"""Exceções de negócio da aplicação.

Centralizamos aqui os tipos de erro esperados (validação, não encontrado,
conflito) para que o tratamento de erros da API seja único e consistente,
em vez de cada rota decidir sozinha o status HTTP que deve retornar.
"""


class ErroDeNegocio(Exception):
    """Classe base para erros de regra de negócio."""
    status_code = 400

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class ErroValidacao(ErroDeNegocio):
    """Dados inválidos ou incompletos enviados pelo cliente (422)."""
    status_code = 422


class ErroNaoEncontrado(ErroDeNegocio):
    """Recurso solicitado não existe (404)."""
    status_code = 404


class ErroConflito(ErroDeNegocio):
    """Violação de unicidade ou estado (ex.: SKU duplicado) (409)."""
    status_code = 409

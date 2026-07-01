from app.Model.Produto import Produto

class Produto_Repositorio():

    def __init__(self,sessao):
        self.sessao = sessao
    
    def salvar(self,produto):
        self.sessao.add(produto)
        return produto
    
    def remover(self,produto):
        self.sessao.delete(produto)
    
    def buscar_por_sku(self,sku):
        return self.sessao.query(Produto).filter_by(sku=sku).first()


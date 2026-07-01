from datetime import datetime, timedelta, timezone
import random

from app.database.conexao import SessionLocal
from app.Model.Produto import Produto
from app.Model.Endereco import Endereco
from app.Model.Contagem import Contagem
from app.Repository import criar_tabelas 

def executar_seed():
    criar_tabelas.criar_todas_tabelas()
    sessao = SessionLocal()

    try:
        produtos = [
            Produto(sku="SKU001", descricao="PEPSI ZERO PET 2L CAIXA C/6", unidade="CX"),
            Produto(sku="SKU002", descricao="PEPSI COLA PET 2L", unidade="UN"),
            Produto(sku="SKU003", descricao="GUARANA ANTARCTICA PET 2L CAIXA C/6", unidade="CX"),
            Produto(sku="SKU004", descricao="H2OH LIMONETO PET 1,5 SHRINK C/06", unidade="PALETE"),
            Produto(sku="SKU005", descricao="H2OH LIMONETO PET", unidade="UN"),
            Produto(sku="SKU006", descricao="AGUA MIN LEBRINHA S/GAS PVC 497ML", unidade="CX"),
            Produto(sku="SKU007", descricao="ANTARCTICA PILSEN LATA 350ML C/18", unidade="CX"),
            Produto(sku="SKU008", descricao="BRAHMA CHOPP LATA 350ML C/12", unidade="CX"),
            Produto(sku="SKU009", descricao="BRAHMA CHOPP LATA 350ML C/18", unidade="CX"),
            Produto(sku="SKU010", descricao="ANTARCTICA PILSEN LT 269ML C/15", unidade="PALETE"),
        ]
        
        enderecos = [
            Endereco(endereco="R01-P01-N01-A01", descricao="Rua 01, posição 01, número 01, pallet A01"),
            Endereco(endereco="R01-P02-N01-A03", descricao="Rua 01, posição 02, número 01, pallet A03"),
            Endereco(endereco="R02-P01-N02-A02", descricao="Rua 02, posição 01, número 02, pallet A02"),
            Endereco(endereco="R01-P02-N02-A04", descricao="Rua 01, posição 02, número 02, pallet A04"),
            Endereco(endereco="R01-P02-N04-A06", descricao="Rua 01, posição 02, número 04, pallet A06")
        ]

        sessao.add_all(produtos)
        sessao.add_all(enderecos)
        sessao.commit() 

        # Captura o momento atual em UTC estrito
        data_base = datetime.now(timezone.utc)
        contagens = []
        usuarios = ["usuario_1", "usuario_2", "usuario_3"]

        for indice in range(30):
            produto = produtos[indice % len(produtos)]
            endereco = enderecos[(indice + (indice // 10)) % len(enderecos)]

            if produto.unidade == "PALETE":
                quantidade_calculada = random.randint(1, 5)
            elif produto.unidade == "CX":
                quantidade_calculada = random.randint(10, 150)
            else:  # Caso seja "UN" (Unidade)
                quantidade_calculada = random.randint(30, 450)

            # Distribui as contagens retroativamente no tempo
            data_registro = data_base - timedelta(days=30 - indice, hours=random.randint(1, 12))

            contagem = Contagem(
                produto_id=produto.id,
                endereco_id=endereco.id,
                quantidade=quantidade_calculada,
                usuario=random.choice(usuarios),
                data_hora=data_registro
            )
            contagens.append(contagem)

        sessao.add_all(contagens)
        sessao.commit()

        print("Seed executada com sucesso. ")
        return True

    except Exception as erro:
        sessao.rollback()
        print("Erro ao executar o seed de dados.")
        print(erro)
        return False

    finally:
        sessao.close()

if __name__ == "__main__":
    executar_seed()

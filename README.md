# CM_STOCK
Sistema web de controle de estoque por enderecamento de armazem, desenvolvido como teste tecnico para a vaga de Analista de Sistemas.

O objetivo final do projeto e disponibilizar uma API REST em Flask, uma interface web simples e uma integracao com SQL Server para cadastro de produtos, enderecos de estoque e contagens.

## Tecnologias

- Python 3.10+
- Flask
- SQLAlchemy
- PyODBC
- SQL Server
- python-dotenv

## Como executar

### 1. Criar o ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No PowerShell:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

Com o ambiente virtual ativo:

```bash
pip install -r requirements.txt
```

## Estrutura do projeto

####  Framework e Validação Inicial (Proof of Concept)
De início, foi desenvolvido um protótipo funcional minimalista (o tradicional "Olá, Mundo!" em formato JSON). O objetivo desta etapa foi validar o correto funcionamento do servidor Flask, garantir que a etapa Genesis (parte inicial) do aplicativo (`criar_app`) resolvesse as rotas sem importações circulares e certificar que o isolamento do ambiente virtual (`venv`) estivesse carregando todas as dependências do arquivo `requirements.txt` com sucesso.

#### Resposta esperada
{
  "mensagem": "Olá, Mundo! Fundação do projeto CM_STOCK (ETAPA GENESIS) iniciada com sucesso.",
  "projeto": "Controle de Estoque por Endereçamento",
  "status": "sucesso",
  "vaga": "Analista de Sistemas"
}


### 3. Configurar o banco de dados

 Ajuste a variavel `DATABASE_URL` com a string de conexao do seu SQL Server dentro do arquivo .env.

Exemplo:

```env
DATABASE_URL=mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BSERVER%3DSEU_SERVIDOR%3BDATABASE%3DCM_STOCK%3BTrusted_Connection%3Dyes%3B
```

## Teste de conexao com SQL Server

Para validar a conexao com o banco:

```bash
python principal.py
```
E acesse a rota:
```
/teste-banco
```
Resultado esperado:

```bash
Conexao com o SQL Server realizada com sucesso.
Horario retornado pelo banco: ...
```

Esse teste executa uma consulta simples no SQL Server para confirmar que a aplicacao consegue carregar a variavel `DATABASE_URL`, abrir a conexao e receber resposta do banco.


Ou se preferir pode excutar diretamente o arquivo seed.py
## Executar a API inicial

Para iniciar a aplicacao Flask:

```bash
python principal.py
```

## Decisoes inicial

- A aplicacao usa o padrao de fabrica do Flask por meio da funcao `criar_app`.
- A conexao com o banco foi isolada em `app/database/conexao.py`.
- A string de conexao e carregada por variavel de ambiente para evitar dados sensiveis no codigo.
- O primeiro marco do projeto foi validar a infraestrutura antes de iniciar os endpoints e telas.

- `Controller`: recebe as requisicoes HTTP e retorna respostas JSON ou telas.
- `Service`: concentra regras de negocio e validacoes.
- `Repository`: concentra consultas e operacoes de persistencia no banco.
- `Model`: representa as tabelas e relacionamentos do banco.
- `database`: centraliza a conexao, sessao e base do SQLAlchemy.

-

## Status atual

A infraestrutura de persistência e a modelagem do domínio foram concluídas com sucesso, estabelecendo os pilares fundamentais da aplicação:

- **Geração Automatizada do Schema:** Desenvolvimento do script de criação automática das tabelas `produtos`, `enderecos` e `contagens` diretamente no Microsoft SQL Server via SQLAlchemy Puro.
- **Lógica e Consistência de Lançamento:** A tabela de `contagens` foi estruturada com regras de integridade referencial, vinculando de forma direta o produto (via SKU) e a posição no armazem (via código de endereço).
- **Auditoria Cronológica em UTC:** Implementação da captura nativa de data/hora padronizada em fuso horário UTC (formato ISO 8601), garantindo precisão absoluta para o rastreamento histórico e auditorias de inventário.
- **Persistência por camada:** repositórios dedicados para Produto, Endereço e Contagem, isolando toda consulta SQL/ORM do restante da aplicação.
- **Consulta SQL puro:** o saldo por endereço e o relatório de divergência usam `ROW_NUMBER() OVER (PARTITION BY produto_id ORDER BY data_hora DESC)` em SQL puro (via `sqlalchemy.text`), comentado em `app/Repository/ContagensRepositorio.py`, para ranquear as últimas contagens de cada produto numa única ida ao banco.


- `erros.py`: exceções de negócio (validação, não encontrado, conflito) usadas pelo tratamento de erros centralizado da API.




## Proximas etapas


1. Implementar CRUD de produtos.
2. Implementar CRUD de enderecos.
4. Implementar registro de contagens.
5. Implementar saldo por endereco e relatorio de divergencia.
6. Criar telas web consumindo a API.



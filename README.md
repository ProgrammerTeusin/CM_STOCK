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

Copie o arquivo `.env.example` para `.env` e ajuste a variavel `DATABASE_URL` com a string de conexao do seu SQL Server.

```bash
cp .env.example .env
```

Exemplo de conteudo do `.env`:

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

A aplicação está funcional de ponta a ponta: API REST completa, telas web consumindo a API e persistência em SQL Server.

- **Geração Automatizada do Schema:** script de criação automática das tabelas `produtos`, `enderecos` e `contagens` via SQLAlchemy Puro (`app/Repository/criar_tabelas.py`, executado também pelo `seed.py`).
- **Camadas:** `Controller` (Blueprints Flask, em `app/Controller`) → `Service` (regras de negócio e validações, em `app/Service`) → `Repository` (acesso a dados, em `app/Repository`) → `Model` (SQLAlchemy, em `app/Model`).
- **Tratamento de erros centralizado:** exceções de negócio (`app/erros.py`) são convertidas em respostas JSON padronizadas com o status HTTP correto (400/404/409/422), registrado em `app/__init__.py`.

- `erros.py`: exceções de negócio (validação, não encontrado, conflito) usadas pelo tratamento de erros centralizado da API.

- `Service`:  concentra validação de campos obrigatórios, unicidade de SKU/endereço e cálculo do relatório de divergência.

- **Auditoria Cronológica em UTC:** captura nativa de data/hora em UTC (ISO 8601) em cada contagem.
- **Carga de Dados (Seed):** `seed.py` popula 10 produtos, 5 endereços e 30 contagens distribuídas no tempo.

### Endpoints da API

| Recurso | Rota | Método |
|---|---|---|
| Produtos | `/api/produtos` | GET (paginado), POST |
| Produtos | `/api/produtos/<sku>` | GET, PUT, DELETE |
| Endereços | `/api/enderecos` | GET (paginado), POST |
| Endereços | `/api/enderecos/<codigo>` | GET, PUT, DELETE |
| Contagens | `/api/contagens` | POST (registrar) |
| Contagens | `/api/contagens/produto/<sku>` | GET (histórico, filtros `data_inicio`/`data_fim`) |
| Relatórios | `/api/relatorios/saldo/<endereco>` | GET |
| Relatórios | `/api/relatorios/divergencia/<endereco>` | GET |

A consulta de saldo e a de divergência usam **SQL puro** (via `sqlalchemy.text`, comentado em `app/Repository/ContagensRepositorio.py`), com `ROW_NUMBER() OVER (PARTITION BY ...)` para obter a(s) última(s) contagem(ns) de cada produto em um endereço numa única ida ao banco.

### Telas web

`/`, `/produtos`, `/produtos/novo`, `/produtos/<sku>/editar`, `/enderecos`, `/enderecos/novo`, `/enderecos/<codigo>/editar`, `/contagens/nova`, `/relatorios/saldo`, `/relatorios/divergencia`.

## Decisões de arquitetura e trade-offs

- Optei por SQLAlchemy "puro" (Core/ORM sem Flask-SQLAlchemy) para ter controle explícito da sessão e poder intercalar SQL puro nas consultas de relatório sem depender de recursos específicos de uma extensão.
- A camada `Service` concentra validação e regra de negócio (SKU/endereço únicos, quantidade não-negativa, cálculo de divergência); o `Controller` fica fino, só traduzindo request/response.
- O cálculo de aumento/redução/estável do relatório de divergência fica em Python (não em SQL) porque é regra de negócio simples sobre poucos registros por endereço; a parte pesada (ranquear as contagens por data) fica no banco via `ROW_NUMBER()`.
- Sessão por requisição (`SessionLocal()` aberta e fechada em cada rota) para simplicidade — em uma aplicação maior, valeria um middleware/`teardown_appcontext` para isso.

## O que faria diferente com mais tempo

- Testes automatizados dos Services e das consultas SQL de relatório.
- Autenticação simples protegendo os endpoints de escrita.
- Importação de contagens via CSV.
- Índices explícitos em `contagens (endereco_id, produto_id, data_hora)`, com justificativa.

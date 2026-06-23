# CM_STOCK

Este projeto consiste em um sistema completo de **Controle de Estoque por Endereçamento de Armazém**, desenvolvido como solução para o teste técnico de avaliação para a vaga de **Analista de Sistemas**.

---

### 2. Configurações Iniciais para Executar o Projeto com Eficiência

#### 2.1 Criar e Ativar o Ambiente Virtual (venv)
> **💡 Recomendação Técnica:** Para fins de isolamento e para evitar conflitos de dependências com outras bibliotecas globais do Python já instaladas no sistema operacional, recomenda-se fortemente a criação e o uso de um ambiente virtual (`venv`) exclusivo para este projeto.

Execute o comando correspondente ao seu sistema operacional:

```bash
# Criar o ambiente virtual (isolado do sistema global)
python -m venv venv

# Ativar no Windows (Prompt de Comando - CMD)
venv\Scripts\activate

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar no Linux / macOS
source venv/bin/activate
```

Ao ativar com sucesso, o terminal exibirá o prefixo `(venv)` antes do caminho da pasta, indicando que todas as instalações a partir deste ponto ficarão restritas a este projeto.

#### 2.2 Instalar as Bibliotecas Necessárias
Foi disponibilizado o arquivo `requirements.txt`, que contém todas as dependências e suas respectivas versões fixadas de forma estrita, garantindo a reprodutibilidade exata da aplicação.

Com o ambiente virtual (`venv`) devidamente ativo, execute o comando abaixo no seu terminal para realizar a instalação automatizada:

```bash
pip install -r requirements.txt
```

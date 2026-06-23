from app import criar_app

# Cria a instância da aplicação utilizando o padrão de fábrica em português
app = criar_app()

if __name__ == "__main__":
    # Executa o servidor. O modo 'debug=True' ativa o recarregamento automático
    # do código a cada alteração salva
    app.run(debug=True)
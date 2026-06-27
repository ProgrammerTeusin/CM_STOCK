from app import criar_app, db
from sqlalchemy import text


app = criar_app()
with app.app_context():
    # Executa uma consulta nativa simples no SQL Server
    resultado = db.session.execute(text("SELECT GETDATE();")).scalar()
    print(f"\n🚀 CONEXÃO COM O SQL SERVER FUNCIONOU! Horário do banco: {resultado}\n")

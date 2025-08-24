from app.database import engine
from app.models import Base

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    print("Criando tabelas do banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_database()

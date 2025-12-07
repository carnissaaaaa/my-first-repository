from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings
from models import table_registry

settings = Settings()

# Cria o motor do banco de dados
engine = create_engine(settings.DATABASE_URL)

# Cria a sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão do banco de dados (dependência do FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar as tabelas (usada em test.py)
def create_db_and_tables():
    table_registry.metadata.create_all(engine)

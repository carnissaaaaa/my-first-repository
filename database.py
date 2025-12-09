from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings
from models import table_registry

settings = Settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    table_registry.metadata.create_all(engine)

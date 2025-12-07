from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import User, table_registry

app = FastAPI(title='API de teste')

engine = create_engine("sqlite:///:memory", echo=False)


table_registry.metadata.create_all(engine)

with Session(engine) as session:
    aluno = User(
        nome_usuario="joaodasilva", senha="senha123", email="joao@email.com"
    )
    session.add(aluno)
    session.commit()
    session.refresh(aluno)

print("DADOS DO USUÁRIO:", aluno)
print("ID:", aluno.id)
print("Criado em:", aluno.created_at)

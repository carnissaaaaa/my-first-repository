from sqlalchemy.orm import Session
from models import User
from database import create_db_and_tables, engine

# Cria as tabelas no banco de dados em memória
create_db_and_tables()

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
print("Atualizado em:", aluno.updated_at)

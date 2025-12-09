from fastapi import FastAPI, HTTPException, Depends 
from http import HTTPStatus
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from schema import Receita, BaseReceita, BaseUsuario, UsuarioPublic
from models import User
from database import get_db

app = FastAPI()

receitas: List[Receita] = [
    Receita(id=1, nome="Bolo de Chocolate", ingredientes=["farinha", "açúcar", "chocolate em pó", "ovos", "leite", "óleo"], modo_de_preparo="Misture tudo e asse."),
    Receita(id=2, nome="Brigadeiro", ingredientes=["leite condensado", "chocolate em pó", "manteiga"], modo_de_preparo="Misture no fogo até desgrudar da panela."),
    Receita(id=3, nome="Pudim", ingredientes=["leite condensado", "leite", "ovos", "açúcar"], modo_de_preparo="Faça a calda, misture os ingredientes e asse em banho-maria."),
    Receita(id=4, nome="Feijoada", ingredientes=["feijão preto", "carne seca", "linguiça", "costelinha", "bacon", "alho", "cebola"], modo_de_preparo="Cozinhe o feijão e as carnes separadamente, depois junte tudo e tempere."),
    Receita(id=5, nome="Moqueca de Peixe", ingredientes=["peixe", "azeite de dendê", "leite de coco", "tomate", "cebola", "pimentões", "coentro"], modo_de_preparo="Refogue os temperos, adicione o peixe e cozinhe com leite de coco e azeite de dendê."),
    Receita(id=6, nome="Pão de Queijo", ingredientes=["polvilho doce", "queijo minas", "leite", "óleo", "ovos", "sal"], modo_de_preparo="Misture os ingredientes, faça bolinhas e asse.")
]

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
async def get_receitas():
    return receitas

@app.get("/receitas/{receita_id}", response_model=Receita, status_code=HTTPStatus.OK)
async def get_receita_by_id(receita_id: int):
    for receita in receitas:
        if receita.id == receita_id:
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.get("/receitas/nome/{receita_nome}", response_model=Receita, status_code=HTTPStatus.OK)
async def get_receita_by_name(receita_nome: str):
    for receita in receitas:
        if receita.nome.lower() == receita_nome.lower():
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
async def create_receita(receita: BaseReceita):
    for r in receitas:
        if r.nome.lower() == receita.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita com este nome já existe") 

    if not (2 <= len(receita.nome) <= 50):
       raise HTTPException (status_code=HTTPStatus.BAD_REQUEST, detail= "O nome da receita deve ter entre 2 e 50 caracteres")

    if not (1 <= len(receita.ingredientes) <= 20):
       raise HTTPException (status_code=HTTPStatus.BAD_REQUEST, detail= "A receita deve ter entre 1 e 20 ingredientes")
    
    if len(receitas) > 0:
        novo_id = receitas[-1].id + 1
    else:
        novo_id=1
    nova_receita = Receita(
        id=novo_id,
        nome=receita.nome,
        ingredientes = receita.ingredientes,
        modo_de_preparo = receita.modo_de_preparo
    )
    receitas.append(nova_receita)
    return nova_receita

@app.put("/receitas/{receita_id}",response_model=Receita, status_code=HTTPStatus.OK)
async def update_receita(receita_id: int, receita: BaseReceita):
    found_index = -1
    for i, r in enumerate(receitas):
        if r.id == receita_id:
            found_index = i
            break

    if found_index == -1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail= "Receita não encontrada")

    for i, r in enumerate(receitas):
        if i != found_index and r.nome.lower() == receita.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita com este nome já existe")

    if not receita.nome or not receita.ingredientes or not receita.modo_de_preparo:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Nenhum campo pode ser vazio")
    if any(not ing for ing in receita.ingredientes):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Nenhum ingrediente pode ser vazio")

    if not (2 <= len(receita.nome) <= 50):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres")

    if not (1 <= len(receita.ingredientes) <= 20):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter entre 1 e 20 ingredientes")

    receita.id = receita_id 
    receitas[found_index] = receita
    return receita


@app.delete("/receitas/{receita_id}",response_model=Receita, status_code=HTTPStatus.OK)
async def delete_receita(receita_id: int):
    if not receitas:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há receitas para excluir.")
    found_index = -1
    deleted_receita = None
    for i, r in enumerate(receitas):
        if r.id == receita_id:
            found_index = i
            deleted_receita = r
            break

    if found_index == -1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

    receitas.pop(found_index)
    return {"message": f"Receita '{deleted_receita.nome}' (ID: {deleted_receita.id}) foi deletada com sucesso."}


@app.post("/usuarios", response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def create_usuario(dados: BaseUsuario, db: Session = Depends(get_db)):
    # 1. Validação de e-mail duplicado (Requisito: Email único)
    existing_user = db.scalar(select(User).where(User.email == dados.email))
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe um usuário cadastrado com este email."
        )

    # 2. Criação do objeto User
    novo_usuario = User(
        nome_usuario=dados.nome_usuario,
        email=dados.email,
        senha=dados.senha # A senha deve ser hasheada em um projeto real, mas o requisito não pede
    )

    # 3. Adiciona e commita no banco de dados
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # 4. Retorna o usuário público
    return novo_usuario

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios(db: Session = Depends(get_db)):
    # 1. Consulta todos os usuários
    usuarios = db.scalars(select(User)).all()
    
    # 2. Retorna a lista (vazia ou preenchida)
    return usuarios

@app.get("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int, db: Session = Depends(get_db)):
    # 1. Consulta o usuário pelo ID
    usuario = db.scalar(select(User).where(User.id == id))
    
    # 2. Verifica se encontrou
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )
        
    # 3. Retorna o usuário
    return usuario

@app.get("/usuarios/nome/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str, db: Session = Depends(get_db)):
    # 1. Consulta o usuário pelo nome
    usuario = db.scalar(select(User).where(User.nome_usuario == nome_usuario))
    
    # 2. Verifica se encontrou
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )
        
    # 3. Retorna o usuário
    return usuario

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario, db: Session = Depends(get_db)):
    # 1. Busca o usuário a ser atualizado
    usuario = db.scalar(select(User).where(User.id == id))
    
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # 2. Validação de e-mail duplicado (excluindo o próprio usuário)
    existing_user_with_email = db.scalar(
        select(User).where(User.email == dados.email, User.id != id)
    )
    if existing_user_with_email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Já existe outro usuário com este email."
        )

    # 3. Atualiza os campos
    usuario.nome_usuario = dados.nome_usuario
    usuario.email = dados.email
    usuario.senha = dados.senha
    # O campo updated_at é atualizado automaticamente pelo `onupdate=func.now()` no models.py

    # 4. Commita a transação
    db.commit()
    db.refresh(usuario)
    
    # 5. Retorna o usuário atualizado
    return usuario

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def delete_usuario(id: int, db: Session = Depends(get_db)):
    # 1. Busca o usuário a ser deletado
    usuario = db.scalar(select(User).where(User.id == id))
    
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # 2. Deleta o usuário
    db.delete(usuario)
    db.commit()
    
    # 3. Retorna o usuário deletado (Requisito: retornar os dados do usuário deletado)
    return usuario

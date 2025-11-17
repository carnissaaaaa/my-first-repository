from fastapi import FastAPI, HTTPException 
from http import HTTPStatus
from schema import Receita, Usuario, BaseReceita, BaseUsuario, UsuarioPublic
from typing import List

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/alunos/{nome_aluno}")
async def read_aluno(nome_aluno: str):
    return {"aluno": nome_aluno}

usuarios: List[Usuario] = []

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
async def create_usuario(dados: BaseUsuario):
    for u in usuarios:
        if u.email == dados.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário cadastrado com este email.")
            
    if len(usuarios) > 0:
        novo_id = usuarios[-1].id + 1
    else:
        novo_id = 1
        
    novo_usuario = Usuario(
        id=novo_id,
        nome_usuario=dados.nome_usuario,
        email=dados.email,
        senha=dados.senha
    )
    
    usuarios.append(novo_usuario)
    return novo_usuario

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
async def get_todos_usuarios():
    return usuarios
    
@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def get_usuario_por_nome(nome_usuario: str):
    for usuario in usuarios:
        if usuario.nome_usuario.lower() == nome_usuario.lower():
            return usuario
            
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def get_usuario_por_id(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
            
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def update_usuario(id: int, dados: BaseUsuario):
    found_index = -1
    for i, u in enumerate(usuarios):
        if u.id == id:
            found_index = i
            break

    if found_index == -1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    for i, u in enumerate(usuarios):
        if i != found_index and u.email == dados.email:
             raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário com este email")

    usuario_atualizado = Usuario(
        id=id,
        nome_usuario=dados.nome_usuario,
        email=dados.email,
        senha=dados.senha
    )
    
    usuarios[found_index] = usuario_atualizado
    return usuario_atualizado

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
async def delete_usuario(id: int):
    if not usuarios:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há usuários para excluir.")

    found_index = -1
    deleted_usuario = None
    
    for i, u in enumerate(usuarios):
        if u.id == id:
            found_index = i
            deleted_usuario = u
            break

    if found_index == -1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    usuarios.pop(found_index)
    return deleted_usuario
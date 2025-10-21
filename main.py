from fastapi import FastAPI
from http import HTTPStatus
from schema import Receita, BaseReceita
from typing import List

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/alunos/{nome_aluno}")
async def read_aluno(nome_aluno: str):
    return {"aluno": nome_aluno}



receitas: List[Receita] = [
    Receita(id=1, nome="Bolo de Chocolate", ingredientes=["farinha", "açúcar", "chocolate em pó", "ovos", "leite", "óleo"], modo_de_preparo="Misture tudo e asse."),
    Receita(id=2, nome="Brigadeiro", ingredientes=["leite condensado", "chocolate em pó", "manteiga"], modo_de_preparo="Misture no fogo até desgrudar da panela."),
    Receita(id=3, nome="Pudim", ingredientes=["leite condensado", "leite", "ovos", "açúcar"], modo_de_preparo="Faça a calda, misture os ingredientes e asse em banho-maria."),
    Receita(id=4, nome="Feijoada", ingredientes=["feijão preto", "carne seca", "linguiça", "costelinha", "bacon", "alho", "cebola"], modo_de_preparo="Cozinhe o feijão e as carnes separadamente, depois junte tudo e tempere."),
    Receita(id=5, nome="Moqueca de Peixe", ingredientes=["peixe", "azeite de dendê", "leite de coco", "tomate", "cebola", "pimentões", "coentro"], modo_de_preparo="Refogue os temperos, adicione o peixe e cozinhe com leite de coco e azeite de dendê."),
    Receita(id=6, nome="Pão de Queijo", ingredientes=["polvilho doce", "queijo minas", "leite", "óleo", "ovos", "sal"], modo_de_preparo="Misture os ingredientes, faça bolinhas e asse.")
]

@app.get("/receitas", status_code=HTTPStatus.OK)
async def get_receitas():
    return receitas

@app.get("/receitas/{receita_id}")
async def get_receita_by_id(receita_id: int):
    for receita in receitas:
        if receita.id == receita_id:
            return receita
    return {"menssagem": "Receita não encontra"}

@app.get("/receitas/nome/{receita_nome}")
async def get_receita_by_name(receita_nome: str):
    for receita in receitas:
        if receita.nome.lower() == receita_nome.lower():
            return receita
    return {"menssagem": "Receita não encontrada"}



@app.post("/receitas", status_code=HTTPStatus.CREATED)
async def create_receita(receita: BaseReceita):
    for r in receitas:
        if r.nome.lower() == receita.nome.lower():
            return {"menssagem": "Receita com este nome já existe"}

    if not (2 <= len(receita.nome) <= 50):
        return {"message": "O nome da receita deve ter entre 2 e 50 caracteres"}

    if not (1 <= len(receita.ingredientes) <= 20):
        return {"message": "A receita deve ter entre 1 e 20 ingredientes"}

    if len(receitas) > 0:
        receita.id = receitas[-1].id + 1
    else:
        receita.id = 1
    
    receitas.append(receita)
    return receita




@app.put("/receitas/{receita_id}", status_code=HTTPStatus.OK)
async def update_receita(receita_id: int, receita: BaseReceita):
    found_index = -1
    for i, r in enumerate(receitas):
        if r.id == receita_id:
            found_index = i
            break

    if found_index == -1:
        return {"message": "Receita não encontrada"}

    for i, r in enumerate(receitas):
        if i != found_index and r.nome.lower() == receita.nome.lower():
            return {"message": "Já existe uma receita com este nome"}

    if not receita.nome or not receita.ingredientes or not receita.modo_de_preparo:
        return {"message": "Nenhum campo pode ser vazio"}
    if any(not ing for ing in receita.ingredientes):
        return {"message": "Nenhum ingrediente pode ser vazio"}

    if not (2 <= len(receita.nome) <= 50):
        return {"message": "O nome da receita deve ter entre 2 e 50 caracteres"}

    if not (1 <= len(receita.ingredientes) <= 20):
        return {"message": "A receita deve ter entre 1 e 20 ingredientes"}

    receita.id = receita_id 
    receitas[found_index] = receita
    return receita



@app.delete("/receitas/{receita_id}", status_code=HTTPStatus.OK)
async def delete_receita(receita_id: int):
    if not receitas:
        return {"message": "Não há receitas para excluir."}

    found_index = -1
    deleted_receita = None
    for i, r in enumerate(receitas):
        if r.id == receita_id:
            found_index = i
            deleted_receita = r
            break

    if found_index == -1:
        return {"message": "Receita não encontrada"}

    receitas.pop(found_index)
    return {"message": f"Receita '{deleted_receita.nome}' (ID: {deleted_receita.id}) foi deletada com sucesso."}


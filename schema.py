from pydantic import BaseModel
from typing import List

class BaseReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseReceita):
    id: int 
from pydantic import BaseModel
from typing import List

class BaseReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseReceita):
    id: int 
                    
class Usuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    senha: str

class BaseUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str

class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: str
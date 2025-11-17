from pydantic import BaseModel
from typing import List

class BaseReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseReceita):
    id: int 
    
    '''modelo para armazenar os dados do usuário'''       
class Usuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    senha: str
    
    '''modelo para o usuário preencher'''
class BaseUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str

    '''modelo que irá aparecer na página'''
class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: str
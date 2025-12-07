from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from datetime import datetime

# Schemas de Receita (Mantidos conforme sua instrução)
class BaseReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseReceita):
    id: int 
    
# Schema para criação e atualização (recebe a senha)
class BaseUsuario(BaseModel):
    nome_usuario: str
    email: EmailStr
    senha: str

    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v: str) -> str:
        # Requisito: A senha deve conter letras e números.
        if not any(char.isalpha() for char in v):
            raise ValueError('A senha deve conter pelo menos uma letra.')
        if not any(char.isdigit() for char in v):
            raise ValueError('A senha deve conter pelo menos um número.')
        return v

# Schema que representa o modelo do banco de dados (inclui ID e datas)
class Usuario(BaseUsuario):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema para retorno público (não inclui a senha)
class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
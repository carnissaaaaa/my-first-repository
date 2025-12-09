from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from datetime import datetime

class BaseReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseReceita):
    id: int 
    
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

class Usuario(BaseUsuario):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
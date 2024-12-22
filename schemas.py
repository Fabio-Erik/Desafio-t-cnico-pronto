from pydantic import BaseModel
from typing import Optional

class TarefaCreate(BaseModel):
    descricao: str
    estado: Optional[str] = "pendente"

class TarefaOut(TarefaCreate):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

class TarefaUpdate(BaseModel):
    descricao: Optional[str]
    estado: Optional[str]

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioOut(UsuarioCreate):
    id: int

    class Config:
        orm_mode = True

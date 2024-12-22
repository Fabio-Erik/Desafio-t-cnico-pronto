from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str

class Tarefa(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    descricao: str
    estado: str = "pendente"
    usuario_id: int = Field(foreign_key="usuario.id")

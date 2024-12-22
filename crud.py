from sqlalchemy.orm import Session
from .models import Tarefa, Usuario
from .schemas import TarefaCreate, TarefaUpdate, UsuarioCreate
from typing import List

def criar_tarefa(db: Session, tarefa: TarefaCreate, usuario_id: int):
    db_tarefa = Tarefa(**tarefa.dict(), usuario_id=usuario_id)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def listar_tarefas(db: Session) -> List[Tarefa]:
    return db.query(Tarefa).all()

def obter_tarefa(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaUpdate):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if db_tarefa:
        for key, value in tarefa.dict(exclude_unset=True).items():
            setattr(db_tarefa, key, value)
        db.commit()
        db.refresh(db_tarefa)
    return db_tarefa

def deletar_tarefa(db: Session, tarefa_id: int):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if db_tarefa:
        db.delete(db_tarefa)
        db.commit()
    return db_tarefa

def criar_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

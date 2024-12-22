from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .models import Tarefa, Usuario
from .schemas import TarefaCreate, TarefaOut, TarefaUpdate, UsuarioCreate, UsuarioOut
from .crud import criar_tarefa, listar_tarefas, obter_tarefa, atualizar_tarefa, deletar_tarefa, criar_usuario
from .auth import create_access_token, verify_password, get_password_hash
from .database import get_db
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verify_password(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/usuario/", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario_hash = get_password_hash(usuario.senha)
    db_usuario = Usuario(**usuario.dict(), senha=usuario_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.post("/tarefas/", response_model=TarefaOut)
def criar_tarefa_endpoint(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    usuario_id = 1  # Aqui você deve obter o usuário logado
    db_tarefa = criar_tarefa(db, tarefa, usuario_id)
    return db_tarefa

@app.get("/tarefas/", response_model=list[TarefaOut])
def listar_tarefas_endpoint(db: Session = Depends(get_db)):
    return listar_tarefas(db)

@app.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def visualizar_tarefa_endpoint(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = obter_tarefa(db, tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa_endpoint(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    db_tarefa = atualizar_tarefa(db, tarefa_id, tarefa)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}", response_model=TarefaOut)
def deletar_tarefa_endpoint(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = deletar_tarefa(db, tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

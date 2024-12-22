from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import SQLModel

DATABASE_URL = "sqlite:///./todolist.db"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import Optional
from datetime import datetime
from sqlmodel import Session,SQLModel,create_engine

DB_FILE = 'db.sqlite3'
engine =create_engine(f"sqlite:///{DB_FILE}", echo=True)

def get_db():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)

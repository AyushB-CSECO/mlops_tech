from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent
os.chdir(BASE_PATH)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.create_all(bind=engine)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

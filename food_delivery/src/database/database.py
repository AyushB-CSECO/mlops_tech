from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pathlib import Path
import os

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent
os.chdir(BASE_PATH)

# Database Location
DATABASE_URL = "sqlite:///data/database/info.db"

# Class from which data models will inherit
class Base(DeclarativeBase):
    pass

# DB connection engine
engine = create_engine(DATABASE_URL
            , connect_args={"check_same_thread":False})

# Session for executing DB transactions
SessionLocal = sessionmaker(bind=engine, autoflush=False
                        , autocommit=False)

# The function will create all the tables in SQLlite DB 
# based on models registered(inherit) from Base class
def create_tables():
    Base.metadata.create_all(bind=engine)



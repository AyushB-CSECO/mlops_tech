from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
connect_args_dict = {"check_same_thread":False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args_dict)

# Create session
session_local = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()



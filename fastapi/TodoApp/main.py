from fastapi import FastAPI
import models
from database import engine, create_tables

app = FastAPI()

create_tables()

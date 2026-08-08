from fastapi import FastAPI 
from .database import engine
from .import models 

app = FastAPI()

# Create database
models.Base.metadata.create_all(bind=engine)

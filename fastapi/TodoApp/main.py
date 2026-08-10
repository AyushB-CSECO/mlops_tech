from fastapi import FastAPI
from .database import engine
from .import models
from .routers import auth, todo_apis

app = FastAPI()
# Include Authentication APIs via router method
app.include_router(auth.router)
app.include_router(todo_apis.router)

# Create database
models.Base.metadata.create_all(bind=engine)
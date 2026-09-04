from fastapi import FastAPI

from database import create_tables
from routers import auth, todos

create_tables()

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
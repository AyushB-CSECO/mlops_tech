from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi import HTTPException, Path
from starlette import status
from models import Todos
# from database import create_tables
from database import SessionLocal

app = FastAPI()

# create_tables()

# Create Database object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db: Annotated[Session, Depends(get_db)]
                    , todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                        , detail="Todo not found")
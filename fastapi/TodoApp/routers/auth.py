from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel 
from argon2 import PasswordHasher
from starlette import status

from ..models import Users
from ..database import session_local

router = APIRouter()

password_hasher = PasswordHasher()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str 
    last_name: str 
    password: str
    role: str

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth", status_code = status.HTTP_201_CREATED)
async def create_user(db:db_dependency, 
                        create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = password_hasher.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()
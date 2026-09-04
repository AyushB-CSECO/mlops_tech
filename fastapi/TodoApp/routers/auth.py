from fastapi import APIRouter, Depends
from pydantic import BaseModel
from argon2 import PasswordHasher
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from database import SessionLocal


# Create Database object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

# Password Hasher
pwd_hasher = PasswordHasher()

router = APIRouter()

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,
                        db: Annotated[Session, Depends(get_db)]):
    user_request_dict = create_user_request.model_dump()
    hashed_password = pwd_hasher.hash(user_request_dict['password'])
    user_request_dict['hashed_password'] = hashed_password
    user_request_dict.pop('password', None)

    create_user_model = Users(**user_request_dict)
    db.add(create_user_model)
    db.commit()

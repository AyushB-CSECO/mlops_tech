from fastapi import APIRouter, Depends
from pydantic import BaseModel
from argon2 import PasswordHasher
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from models import Users
from database import SessionLocal


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# Create Database object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Hasher
pwd_context = PasswordHasher()

# Converts password into hashed password
def hash_password(password: str):
    return pwd_context.hash(password)

# Compare and verify user provided plain password
# against hashed password 
def verify_password(plain_password: str, hashed_password: str):
    try:
        pwd_context.verify(hashed_password, plain_password)
        return True 
    except Exception:
        return False

# Authenticate a user against his/her provided credentials
def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True


# Define APIRouter from FastAPI. This will be 
# included in main app. 
router = APIRouter()

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,
                        db: Annotated[Session, Depends(get_db)]):
    user_request_dict = create_user_request.model_dump()
    hashed_password = hash_password(user_request_dict['password'])
    user_request_dict['hashed_password'] = hashed_password
    user_request_dict.pop('password', None)

    create_user_model = Users(**user_request_dict)
    db.add(create_user_model)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[Session, Depends(get_db)]):
    is_verified = authenticate_user(form_data.username, form_data.password, db)

    if not is_verified:
        return "Failed Authentication"
    return "Successful Authentication"

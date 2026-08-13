from datetime import timedelta, timezone
from datetime import datetime as dt
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel 
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from ..models import Users
from ..database import session_local

router = APIRouter()

SECRET_KEY = '7cc27a43680bfe480f08f4bc4ceb6a0621f592edfcb5b02bc80a748d9fa5d269'
ALGORITHM = 'HS256'

password_hasher = PasswordHasher()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str 
    last_name: str 
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    try:
        if password_hasher.verify(user.hashed_password, password):
            return user
    except VerifyMismatchError:
        return False
    
def create_access_token(username: str, user_id:int, expires_delta: timedelta):
    encode = {'sub':username, 'id':user_id}
    expires = dt.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)


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

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
                                 , db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        return {'access_token': 'NA', 'token_type':'NA'}

    token = create_access_token(user.username, user.id, expires_delta=timedelta(minutes=20))
    return {'access_token': token, 'token_type':'bearer'}
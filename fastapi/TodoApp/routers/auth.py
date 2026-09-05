from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from models import Users
from database import SessionLocal


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

# Create Database object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Hasher
pwd_context = PasswordHasher()

# OAuth2Bearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

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

# JWT token parametera
SECRET_KEY = 'dd552cdcaef463bb17d39489a8f3be5d7b2765923aa6480b5cbbb90f0b2efda5'
ALGORITHM = 'HS256'
# Create JWT access token
def create_access_token(username: str, user_id:int, expires_delta: timedelta):
    encode = {'sub':username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if ((username is None) or (user_id is None)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')


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
router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/", status_code=status.HTTP_201_CREATED)
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
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')

    user = db.query(Users).filter(Users.username == form_data.username).first()
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}
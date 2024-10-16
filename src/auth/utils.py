from datetime import datetime, timedelta,timezone
from fastapi import Depends, HTTPException,status
import jwt
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select
from models import AuthUser, AuthUserBase, AuthUserPublic
from schemas import Token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def get_password_hash(password:str):
    return pwd_context.hash(password)

async def verify_password(password:str,hashed_password:str):
    return pwd_context.verify(password,hashed_password)
async def verify_user(username:str,password:str,session:Session):
    user=session.exec(
        select(AuthUser).where(AuthUser.username==username)
    ).first()
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user
async def create_access_token(username:str,expires_delta:int=0):
    user={"username":username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    user["exp"] = expire
    token = jwt.encode(user,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":token,"token_type":"Bearer"}

async def get_current_user(session:Session,token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    user=session.exec(
        select(AuthUser).where(AuthUser.username==username)
    ).first()
    if user is None:
        raise credentials_exception
    return user

async def login_user(user:AuthUserBase,session:Session):
    invalid_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user=await verify_user(user.username,user.password,session)
    if not user:
        raise invalid_exception
    return await create_access_token(user.username)

from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, create_engine
from schemas import Token
from utils import get_current_user, login_user
from models import AuthUser, AuthUserBase, AuthUserPublic
from settings import DATABASE_URI,logger

engine=create_engine(DATABASE_URI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
SessionDep=Annotated[Session, Depends(get_session)]
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app=FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def get_user(user_id:int, session:SessionDep):
    user=session.get(AuthUser, user_id)
    if user:
        logger.info(user)
        return user
    return {"message":"user not found"}


@app.get("/")
async def root():
    return {"message":"Hello World"}
@app.post("/users",response_model=AuthUser)
async def create_user(user:AuthUserBase,session:SessionDep):
    user=AuthUser.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/login",response_model=Token)
async def login(user:Annotated[OAuth2PasswordRequestForm,Depends()],session:SessionDep):
    return await login_user(user,session)

@app.post("/verify-user",response_model=AuthUserPublic)
async def verify_user(token:Annotated[str,Depends(oauth2_scheme)],session:SessionDep):
    logger.info(token)
    return await get_current_user(session,token)



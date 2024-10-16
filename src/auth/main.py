# todo: connect db
# todo: create user
# todo: login user
# todo: logout user
# todo: get tooken for user
# todo: verify user
# todo: get users

from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine,select

from models import AuthUser, AuthUserBase
from settings import DATABASE_URI,logger

engine=create_engine(DATABASE_URI)

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

@app.post("/login")
async def login(user:AuthUserBase,session:SessionDep):
    username, password = user.username, user.password
    user:AuthUser = session.exec(
        select(AuthUser).where(AuthUser.username==username)
    ).first()
    if user and user.password==password:
        return {"message":"login success"}
    return {"message":"login failed"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


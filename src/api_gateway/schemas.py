from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str

class Signup(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

from sqlmodel import Field, SQLModel


class AuthUserBase(SQLModel):
    username: str
    password: str


class AuthUser(AuthUserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class AuthUserPublic(SQLModel):
    id: int
    username: str

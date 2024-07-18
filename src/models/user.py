from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = False


class UserOut(BaseModel):
    email: str


class UserIn(BaseModel):
    email: str
    password: str

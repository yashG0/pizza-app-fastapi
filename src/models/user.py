from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    is_staff: bool = False
    is_active: bool = False
    orders: int = 0


class UserOut(BaseModel):
    email: str


class UserIn(BaseModel):
    email: str
    password: str

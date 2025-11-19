from sqlmodel import SQLModel
from datetime import datetime


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    refresh_token: str   # <--- Add this
    token_type: str

class TokenRefresh(SQLModel):
    refresh_token: str

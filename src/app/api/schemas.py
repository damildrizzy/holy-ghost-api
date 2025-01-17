from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class TongueBase(BaseModel):
    raw_string: str


class TongueCreate(TongueBase):
    pass


class Tongue(TongueBase):
    tongues_string: str

    class Config:
        orm_mode = True

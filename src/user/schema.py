from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from src.user.model import User


class UserResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password : Optional[str]

    class Config:
        orm_mode = True


class UserLogin(UserCreate):
    email: Optional[str]
    password : Optional[str]

    class Config:
        orm_mode = True


class UserTable(UserResponse):
    id : Optional[UUID]
    password: Optional[str]
    is_deleted: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class SystemUser(UserLogin):
    password: str


class HTTPError(BaseModel):
    detail: str


class LoggedInUser(BaseModel):
    id : Optional[UUID]
    email : Optional[UUID]
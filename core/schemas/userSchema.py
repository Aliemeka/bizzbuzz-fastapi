from typing import List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from .postSchema import Post


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserProfile(UserBase):
    class Config:
        from_attributes = True


class User(UserBase):
    id: UUID

    class Config:
        from_attributes = True

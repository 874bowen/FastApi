from typing import Optional

from pydantic import BaseModel, EmailStr


# title str, content str, category, Bool published schema for validation
from pydantic.schema import datetime


class PostBase(BaseModel):
    """
        This is going to give us a schema on how
        the created data should look like -
        providing validation
    """
    title: str
    content: str
    published: bool = True  # giving it a default value


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True  # tells the pydantic model to read data even when it's not a dict


class CreatUser(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


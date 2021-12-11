from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import conint
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserOut(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: PostOut
    Votes: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class EmailSchema(BaseModel):
    email: EmailStr

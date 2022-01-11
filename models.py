# python
from uuid import UUID
from typing import Optional
from datetime import date, datetime

# pydantic
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    nick_name: str = Field(
        ...,
        min_length=1,
        max_length=64,
        
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=64
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=64
    )
    user_id: UUID = Field(...)

class UserPrivate(User):

    email: EmailStr = Field(...)
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    birth_date: Optional[date] = Field(default=None)
    

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256   
    )
    created_at: datetime = Field(default= datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by_nickname: str = Field(...)
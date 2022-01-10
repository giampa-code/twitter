# python
from uuid import UUID
from typing import Optional
from datetime import date, datetime

# pydantic
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
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
    birth_date: Optional[date] = Field(default=None)

class UserPrivate(User):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256   
    )
    created_at: datetime = Field(default= datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)
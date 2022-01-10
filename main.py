# python
from uuid import UUID
from datetime import date
from typing import Optional, List

# Models
from models import User, Tweet

# fapi
from fastapi import FastAPI, status

# pydantic
from pydantic import BaseModel, EmailStr, Field


# definition of the app
app = FastAPI()


# PO 
## home


## Users
### Sign up
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a user',
    tags=['Users']
)
def signup():
    pass

### Login
@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login a user',
    tags=['Users']
)
def login():
    pass

### Show users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all users',
    tags=['Users']
)
def show_all_users():
    pass

### Show user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show a user',
    tags=['Users']
)
def show_a_user():
    pass

### Delete user
@app.delete(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Delete a user',
    tags=['Users']
)
def delete_a_user():
    pass

### Update user
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update a user',
    tags=['Users']
)
def update_a_user():
    pass

## Tweets
### show all tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_201_CREATED,
    summary='Show all tweets',
    tags=['Tweets']
)
def home():
    return {'Twitter api':'todo liso'}

### post a tweet
@app.post(
    path='/tweets',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Post a tweet',
    tags=['Tweets']
)
def post_a_tweet():
    pass

### show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['Tweets']
)
def show_a_tweet():
    pass

### delete a tweet
@app.delete(
    path='/post/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a tweet',
    tags=['Tweets']
)
def delete_a_tweet():
    pass

### delete a tweets
@app.put(
    path='/post/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update all tweets',
    tags=['Tweets']
)
def update_a_tweet():
    pass
# python
from uuid import UUID, uuid4
from datetime import date, datetime
from typing import Optional, List
import json

from fastapi.datastructures import Default

# Models
from models import User, Tweet, UserPrivate

# fapi
from fastapi import FastAPI, status, Body, Form, Path, Query, HTTPException

# pydantic
from pydantic import BaseModel, EmailStr, Field, SecretStr


# definition of the app
app = FastAPI()

# useful funcs
all_users = []
with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for user in datos:
            all_users.append(user['nick_name'])

# PO 
## Users
### Sign up
@app.post(
    path='/signup',
    status_code=status.HTTP_201_CREATED,
    summary='Register a user',
    tags=['Users']
)
def signup(
    email: EmailStr = Form(...),
    nick_name: str = Form(..., min_length=1, max_length=32, regex='^[a-zA-Z0-9_]+$'),
    last_name: str = Form(...,min_length=1,max_length=32),
    first_name: str = Form(...,min_length=1,max_length=32),
    password: str = Form(..., min_length=8, max_length=32),
    birth_date: Optional[date] = Form(default=None)
):
    """
    Sign up
    
    This path operation (PO) register a user in the app

    Parameters:

        - Request body parameter
            - email: EmailStr
            - nickname: only alphanumerics and characters
            - last_name: str 
            - first_name: str 
            - password: str 
            - birth_date: date

    Returns a confirmation
    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)

        for user in datos:
            if email in user['email']:
                raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"¡This useremail already exist!"
        )
        user_dict = {
            "nick_name": nick_name,
            "first_name": first_name,
            "last_name": last_name,
            "user_id": str(uuid4()),
            "email": email,
            "password": password,
            "birth_date": str(birth_date)
        }
        
        datos.append(user_dict)
        # Going to the top of the document
        f.seek(0)
        json.dump(datos,f)

        # append the nickname to the all nicknames list
        all_users.append(nick_name)
        return {'new user':'ok'}

### Login
@app.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    summary='Login a user',
    tags=['Users']
)
def login(email: EmailStr  = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)

        for user in datos:
            if email==user['email'] and password==user['password']:
                return {'Login':'succesfully'} 
            elif email!=user['email']:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"This account does not exist. Please create a new account"
                ) 
            elif password!=user["password"]:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"Incorrect password"
                ) 
        


### Show all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all users',
    tags=['Users']
)
def show_all_users():
    """
    This PO shows all users in the app.

    Parameters:

        - None

    Returns a json list whit all the users in the app, with the following keys:

        - first_name
        - last_name


    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        return datos

### Show user
@app.get(
    path='/users/{user_nickname}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show a user',
    tags=['Users']
)
def show_a_user(user_nickname):
    """
    This PO shows a user in the app.

    Parameters:

        - path nick_name

    Returns a json list whit all the users in the app, with the following keys:

        - nick_name
        - first_name
        - last_name
        - user_id

    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for user in datos:
            if user_nickname == user['nick_name']:
                return user
        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This user doesn't exists."
                ) 


### Delete user
@app.delete(
    path='/users/{user_nickname}',
    status_code=status.HTTP_200_OK,
    summary='Delete a user',
    tags=['Users']
)
def delete_a_user(user_nickname, password):
    """
    This PO delete a user in the app.

    Parameters:

        - delete path nick_name

    Returns a confirmation

    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for i,user in enumerate(datos):
            if user['nick_name'] == user_nickname and user['password'] == password:
                del datos[i]
                f.seek(0)
                print(datos)
                json.dump(datos,f)
                f.truncate()

                return {f'user {user_nickname}':'deleted'}
        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This user doesn't exists or wrong password."
                ) 

### Update user
@app.put(
    path='/users/{user_nickname}',
    status_code=status.HTTP_200_OK,
    summary='Update a user',
    tags=['Users']
)
def update_a_user(
        user_nickname,
        new_first_name: str = Form(...,min_length=1, max_length=64),
        new_last_name: str = Form(...,min_length=1, max_length=64),
        new_birth_date: Optional[date] = Form(default=None)

    ):
    """
    Update user
    
    This path operation (PO) updates a user in the app

    Parameters:

        - user_nickname

    Returns a json with the new basic user info:

        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open('users.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for user in datos:
            if user['nick_name'] == user_nickname:
                user['first_name'] = new_first_name
                user['last_name'] = new_last_name
                user['birth_date'] = str(new_birth_date)

                f.seek(0)
                json.dump(datos,f)
                f.truncate()
                return {f'user {user_nickname}':'updated'}

        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This user doesn't exists."
                ) 

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
    """
    This PO shows all tweets in the app.

    Parameters:

        - None

    Returns a json with the basic info of the tweet:
        
        - tweet_id: UUID = 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User  

    """
    with open('tweets.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        return datos

### post a tweet
@app.post(
    path='/tweets',
    status_code=status.HTTP_201_CREATED,
    summary='Post a tweet',
    tags=['Tweets']
)
def post_a_tweet(
    by_nickname: str = Form(...),
    content: str = Form(...)
    ):
    """
    Post a Tweet

    This PO post a tweet in the app

    Parameters:

        - Request body
            - user nickname
            - content

    Returns a confirmation
    """
    if by_nickname not in all_users:
        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This user doesn't exists."
                ) 
                 
    with open('tweets.json','r+', encoding='utf-8') as t:
        datos = json.load(t)
        tweet_dict = {
            "tweet_id": str(uuid4()),
            "content": content,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "by_nickname": by_nickname
        }

        tweet_dict['tweet_id'] = str(tweet_dict ['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict ['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict ['updated_at'])
        datos.append(tweet_dict)
        # Going to the top of the document
        t.seek(0)
        json.dump(datos,t)
        return {f'tweet by {by_nickname}':'posted ok'}

### show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['Tweets']
)
def show_a_tweet(tweet_id):
    """
    This PO shows a tweet in the app.

    Parameters:

        - tweet_id

    Returns a Tweet json
    """
    with open('tweets.json','r+', encoding='utf-8') as t:
        datos = json.load(t)
        for tweet in datos:
            if tweet['tweet_id'] == tweet_id:
                return tweet
            else:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_ACCEPTABLE,
                detail=f"This tweet doesn't exists."
                ) 

### delete a tweet
@app.delete(
    path='/post/{tweet_id}',
    status_code=status.HTTP_200_OK,
    summary='Delete a tweet',
    tags=['Tweets']
)
def delete_a_tweet(tweet_id, nickname):
    """
    This PO delete a tweet in the app.

    Parameters:

        - tweet_id

    Returns a confirmation

    """
    with open('tweets.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for i,tweet in enumerate(datos):
            if tweet['tweet_id'] == tweet_id and tweet['by_nickname'] == nickname:
                del datos[i]
                f.seek(0)
                print(datos)
                json.dump(datos,f)
                f.truncate()

                return {f'Tweet {tweet_id}':'deleted'}
        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This tweet doesn't exists"
                ) 

### update a tweets
@app.put(
    path='/post/{tweet_id}',
    status_code=status.HTTP_200_OK,
    summary='Update all tweets',
    tags=['Tweets']
)
def update_a_tweet(tweet_id, nickname, new_content):
    """
    Update twwet
    
    This path operation (PO) updates a tweet in the app

    Parameters:

        - tweet_id
        - nickname
        - new content

    Returns a confirmation
    """
    with open('tweets.json','r+', encoding='utf-8') as f:
        datos = json.load(f)
        for tweet in datos:
            if tweet['tweet_id'] == tweet_id and tweet['by_nickname'] == nickname:
                tweet['content'] = new_content
                f.seek(0)
                json.dump(datos,f)
                f.truncate()
                return {f'user {tweet_id}':'updated'}

        raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"This tweet doesn't exists or wrong user permits."
                ) 
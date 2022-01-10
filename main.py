# python
from uuid import UUID
from datetime import date
from typing import Optional

# Models
from models import User, Tweet

# fapi
from fastapi import FastAPI

# pydantic
from pydantic import BaseModel, EmailStr, Field


# definition of the app
app = FastAPI()



@app.get(path='/')
def home():
    return {'Twitter api':'todo liso'}
#python
from typing import Optional
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Query # para hacer tipado estático
from enum import Enum

#pydantic
from pydantic import BaseModel, Field, EmailStr#para crear modelos


#fast api
from fastapi import (
    FastAPI,
    Body, Query, Path, Form, Header, Cookie, UploadFile, File,
    status, HTTPException)


# instanciamos la clase FastAPI como objeto en "app"
app = FastAPI()

# Enumerations models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Cities(Enum):
    bs_as = "Buenos Aires"
    cba = "Cordoba"
    sfe = "Santa Fe"
    mdq = "Mar del Plata"

# Models

class Location(BaseModel):
    city: Cities = Field(...)
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50)
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='cacotas')
    age: int = Field(
        ...,
        gt = 0,
        le = 115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(...)
    password: str = Field(...,min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example":{
    #             'first_name': 'Facundo',
    #             'age': 22,

    #         }
    #     }

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example='pepe123')
    password: str = Field(...,min_length=8)

    

# path operation decoration. Get es la función que hace de decorador a la función que creamos abajo

@app.get("/",status_code=status.HTTP_200_OK) # path operation decorator
#path operation function
def home() -> dict:
    return {'Hello':'World','hola':'wey','probando':'autosave','una':'mas'}

# request body
# Create
@app.post(
    "/person/new",
     response_model = Person,
      response_model_exclude = {'password'},
       status_code = status.HTTP_201_CREATED,
       tags = ['Persons'],
       summary = 'Create person in the app',
       deprecated = True
       )
def create_person(person: Person = Body(...)):  # ... significa obligatorio para fAPI
    """
    Create Person

    This path operation creates a person in the app and save de info in the db.

    Parameters:
    - request body parameter:
        - **person: Person** -> a person model with first name, last name, age, hair color and marital status.
    
    Returns a person model of Person

    """
    return person

# Validaciones: query parameters

@app.get(path="/person/detail",status_code=status.HTTP_200_OK,tags = ['Persons'])
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example = 'Rochi'
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required.",
        example = 10
        )
    ):
    return {name: age}

# Validaciones: path parameters

#Exeptions
persons = [1,2,3,4,5]

@app.get(path="/person/detail/{person_id}",tags = ['Persons'])
def show_person(
    person_id: int = Path(..., gt = 0),
    title= "Title id",
    description= "This is the person id. grater than 1"
    ):
    if person_id not in persons:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "This person doesn't exist"
        )
    return {person_id: 'ok'}

# Validaciones: request body
# Update
@app.put(path="/person/{person_id}",tags = ['Persons'])
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="The person id",
        gt=0
        ),
    person: Person = Body(...),
    location: Location = Body(...)
    ):
    results = person.dict()
    results.update(location.dict())
    return results

@app.post(
    path="/login", 
    response_model=LoginOut, 
    status_code=status.HTTP_200_OK,
    response_model_exclude={'password'},
    tags = ['Persons']
    )
def login(
    username:str = Form(...),
    password:str = Form(...)
    ):
    return LoginOut(username=username, password=password)

# Cookies and headers parameters
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
    )
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent

# Files
@app.post(
    path='/post-image',
    )
def post_image(image: UploadFile = File(...)):
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read())/1024)
    }
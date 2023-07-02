#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie, File, UploadFile, HTTPException

#Model

class HairColor(Enum):
    black = "black"
    brown = "brown"
    blond = "blond"
    red = "red"
    white = "white"
    gray = "gray"
    blue = "blue"
    green = "green"
    other = "other"

class Person(BaseModel):
    id:Optional[int] = Field(default=None, title="Person ID", description="Person's ID", gt=0)
    first_name: str = Field(..., min_length=1, max_length=50, title="Person First Name", description="Person's First Name")
    last_name: str = Field(..., min_length=1, max_length=50, title="Person Last Name", description="Person's Last Name")
    age: int = Field(..., ge=18, le=115, title="Person Age", description="Person's Age")
    hair_color: Optional[HairColor] = Field(default=None, title="Person Hair Color", description="Person's Hair Color")
    is_married: Optional[bool] = Field(default=None, title="Person is Married", description="Person's Marital Status")
    password: str = Field(..., min_length=8, title="Person Password", description="Person's Password")

    class Config:
        schema_extra = {
            "example": {
                "id": 1, #Optional
                "first_name": "Pablo",
                "last_name": "Salas",
                "age": 21,
                "hair_color": "brown",
                "is_married": True,
                "password": "12345678"
            }
        }

class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, title="Person Username", description="Person's Username")
    password: str = Field(..., min_length=8, title="Person Password", description="Person's Password")
    message: str = Field(..., title="Login Message", description="Login Message")

    class Config:
        schema_extra = {
            "example": {
                "username": "pablo.salas",
                "password": "12345678",
                "message": "Login Successful"
            }
        }

# class PersonOut(BaseModel):
#     id:Optional[int] = Field(default=None, gt=0)
#     first_name: str = Field(..., min_length=1, max_length=50)
#     last_name: str = Field(..., min_length=1, max_length=50)
#     age: int = Field(..., ge=18, le=115)
#     hair_color: Optional[HairColor] = Field(default=None)
#     is_married: Optional[bool] = Field(default=None)


class Location(BaseModel):
    city: str
    state: str
    country: str

    class Config:
        schema_extra = {
            "example": {
                "city": "Lima",
                "state": "Lima",
                "country": "Peru"
            }
        }


app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    """
    Home

    This path operation returns a greeting message.

    Returns:
    - Dictionary: {"message": "Hello World"}
    """
    return {"message": "Hello World"}

# Request and Response Body

@app.post(
        "/person/new", 
        response_model=Person, 
        response_model_exclude=["password"], 
        status_code=status.HTTP_201_CREATED, 
        tags=["Person"], 
        summary="Create Person"
        )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation create a person in the app and save the information in the database

    Parameters:
    - Request Body Parameters:
        - **person: Person** -> A person model with first_name, last_name, age, hair_color, is_married and password

    Returns a person model with id, first_name, last_name, age, hair_color and is_married
    """

    return person

# Validation: Query Parameters

@app.get("/person/detail", status_code=status.HTTP_200_OK, tags=["Person"])
def show_person(name: Optional[str] = Query(
    None, 
    min_length=1, 
    max_length=50,
    title="Person Name",
    description="Person's Name",
    example="Pablo"
    ), 
    age: Optional[int] = Query(
    ..., 
    gt=18, 
    le=115,
    title="Person Age",
    description="Person's Age",
    example=21,
    deprecated=True
    )):
    """
    Show Person

    This path operation retrieves the details of a person based on the provided name and age.

    Parameters:
    - Query Parameters:
        - **name: Optional[str]** -> The name of the person
        - **age: Optional[int]** -> The age of the person

    Returns:
    - Dictionary: {"name": name, "age": age}
    """
    return {"name": name, "age": age}

# Validation: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["Person"])
def show_person(person_id: int = Path(
    ..., 
    gt=0, 
    title="Person ID",
    description="Person's ID",
    example=1
    )):
    """
    Show Person by ID

    This path operation retrieves the details of a person based on the provided person_id.

    Parameters:
    - Path Parameter:
        - **person_id: int** -> The ID of the person

    Returns:
    - Dictionary: {"Person ID": person_id, "message": "Person Found"}

    Raises:
    - HTTPException 404: If the person with the given person_id is not found
    """
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return {"Person ID": person_id, "message": "Person Found"}

# Validation: Request Body

@app.put("/person/{person_id}", status_code=status.HTTP_200_OK, tags=["Person"])
def update_person(person_id: int = Path(
    ...,
    gt=0,
    title="Person ID",
    description="Person's ID"),
    person: Person = Body(...),
    location: Location = Body(...)
    ):
    """
    Update Person

    This path operation updates the information of a person based on the provided person_id.

    Parameters:
    - Path Parameter:
        - **person_id: int** -> The ID of the person
    - Request Body Parameters:
        - **person: Person** -> A person model with updated information
        - **location: Location** -> A location model with updated information

    Returns:
    - Dictionary: The updated person information

    Raises:
    - HTTPException 404: If the person with the given person_id is not found
    """
    results = person.dict()
    results.update(location.dict())
    return results
    #return person

# Validation: Form Parameters

@app.post("/login", response_model=Login, response_model_exclude=["password"], status_code=status.HTTP_200_OK, tags=["Login"])
def login(username: str = Form(...), password: str = Form(...)):
    """
    Login

    This path operation performs user login and returns a login response.

    Parameters:
    - Form Parameters:
        - **username: str** -> The username of the person
        - **password: str** -> The password of the person

    Returns:
    - Login: A login response model containing the username, password, and login message
    """
    return Login(username=username, password=password, message="Login Successful")

# Cookies and Headers Parameters

@app.post("/contact", status_code=status.HTTP_200_OK, tags=["Contact"])
def contact(first_name: str = Form(..., max_length=20, min_length=1), 
            last_name: str = Form(..., max_length=20, min_length=1),
            email: EmailStr = Form(...),
            message: str = Form(..., max_length=200, min_length=1),
            user_agent: Optional[str] = Header(None),
            ads: Optional[str] = Cookie(None)
            ):
    """
    Contact

    This path operation handles contact requests and returns the user agent.

    Parameters:
    - Form Parameters:
        - **first_name: str** -> The first name of the person
        - **last_name: str** -> The last name of the person
        - **email: EmailStr** -> The email of the person
        - **message: str** -> The message of the contact request
    - Headers Parameters:
        - **user_agent: Optional[str]** -> The user agent
    - Cookies Parameters:
        - **ads: Optional[str]** -> The ads cookie

    Returns:
    - str: The user agent
    """
    return user_agent

# Files

@app.post("/post-image", status_code=status.HTTP_200_OK, tags=["Image"])
def post_image(image: UploadFile = File(...)):
    """
    Post Image

    This path operation handles the uploading of an image file.

    Parameters:
    - Form Parameters:
        - **image: UploadFile** -> The image file to be uploaded

    Returns:
    - Dictionary: The filename, format, and size of the uploaded image
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=3)
    }
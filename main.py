#Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status, Body

app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

    class Config():
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "example@example.com"
                }
            }

class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)

    class Config():
        schema_extra = {
            "example": {
                "password": "12345678",
                }
            }
        
class User(UserBase):
    first_name: str = Field(..., max_length=50, min_length=1)
    last_name: str = Field(..., max_length=50, min_length=1)
    birth_date: Optional[date] = Field(None)

    class Config():
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "1990-01-01"
                }
            }

class UserRegister(User):
    password: str = Field(..., min_length=8, max_length=64)

    class Config():
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "example@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "1990-01-01",
                "password": "12345678",
                }
            }

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., max_length=280, min_length=1)
    created_at: datetime = Field(datetime.now())
    updated_at: Optional[datetime] = Field(None)
    by: User = Field(...)

    class Config():
        schema_extra = {
            "example": {
                "tweet_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "Hello World!",
                "created_at": "2021-01-01 00:00:00",
                "updated_at": "2021-01-01 00:00:00",
                "by": {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "example@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "birth_date": "1990-01-01"
                    }
                }
            }

# Paths Operations

## Users

### Register a new user
@app.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED, summary="Register a new user", tags=["Users"])
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation registers a new user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister
    
    Returns a JSON with the basic information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: Optional[date]
    """
    with open("users.json", "r+", encoding="utf-8") as file:
        users = json.load(file)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        users.append(user_dict)
        file.seek(0)
        json.dump(users, file)
        return user

### Login a user
@app.post("/login", response_model=User, status_code=status.HTTP_200_OK, summary="Login a user", tags=["Users"])
def login():
    pass

### Show all users
@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, summary="Show all users", tags=["Users"])
def show_all_users():

    """
    Show all users

    This path operation shows all users in the app

    Parameters:
        -
    
    Returns a JSON list with all users in the app with the following information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: Optional[date]
    """
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
        return users

### Show a user
@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, summary="Show a user", tags=["Users"])
def show_a_user():
    pass

### Delete a user
@app.delete("/users/{user_id}/delete", response_model=User, status_code=status.HTTP_200_OK, summary="Delete a user", tags=["Users"])
def delete_a_user():
    pass

### Update a user
@app.put("/users/{user_id}/update", response_model=User, status_code=status.HTTP_200_OK, summary="Update a user", tags=["Users"])
def update_a_user():
    pass

## Tweets

### Show all tweets
@app.get("/", response_model=List[Tweet], status_code=status.HTTP_200_OK, summary="Show all tweets", tags=["Tweets"])
def home():
    """
    Home

    This path operation shows all tweets in the app

    Parameters:
        -
    
    Returns a JSON list with all tweets in the app with the following information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """

    with open("tweets.json", "r+", encoding="utf-8") as file:
        tweets = json.load(file)
        return tweets


### Post a tweet
@app.post("/post", response_model=Tweet, status_code=status.HTTP_201_CREATED, summary="Post a tweet", tags=["Tweets"])
def post(tweet: Tweet = Body(...)):
    """
    Post a tweet

    This path operation posts a new tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet
    
    Returns a JSON with the basic information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as file:
        tweets = json.load(file)
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        tweets.append(tweet_dict)
        file.seek(0)
        json.dump(tweets, file)
        return tweet

### Shwo a tweet
@app.get("/tweets/{tweet_id}", response_model=Tweet, status_code=status.HTTP_200_OK, summary="Show a tweet", tags=["Tweets"])
def show_a_tweet():
    pass

### Delete a tweet
@app.delete("/tweets/{tweet_id}/delete", response_model=Tweet, status_code=status.HTTP_200_OK, summary="Delete a tweet", tags=["Tweets"])
def delete_a_tweet():
    pass

### Update a tweet
@app.put("/tweets/{tweet_id}/update", response_model=Tweet, status_code=status.HTTP_200_OK, summary="Update a tweet", tags=["Tweets"])
def update_a_tweet():
    pass
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field()
    username: str = Field(index=True)
    age: str = Field()
    city: str = Field()
    country: str = Field()
    jon_time:str = Field()
    password_hash: str

class Comment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id : int = Field(foreign_key="user.id")


class Topic(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True)
    title:str
    timestamp: datetime = Field(default_factory=datetime.now)
    text : str
    user_id : int = Field(foreign_key="user.id")

class RegisterModel(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    username: str 
    age: str 
    city: str 
    country: str 
    password: str


class LoginModel(BaseModel):
    username: str
    password: str
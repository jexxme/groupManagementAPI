# schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    userID: int
    isAdmin: bool

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    title: str
    description: str
    maxUsers: int

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    groupID: int

    class Config:
        orm_mode = True

class DateBase(BaseModel):
    date: date
    place: str
    maxUsers: int

class DateCreate(DateBase):
    pass

class Date(DateBase):
    groupID: int

    class Config:
        orm_mode = True

class UserInGroupBase(BaseModel):
    startingDate: date

class UserInGroupCreate(UserInGroupBase):
    userID: int
    groupID: int

class UserInGroup(UserInGroupBase):
    userID: int
    groupID: int

    class Config:
        orm_mode = True

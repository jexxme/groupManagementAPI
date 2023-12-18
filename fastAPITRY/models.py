# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    passwordHash = Column(String)
    isAdmin = Column(Boolean, default=False)

class UserInGroup(Base):
    __tablename__ = 'usersInGroups'
    userID = Column(Integer, ForeignKey('users.userID'), primary_key=True)
    groupID = Column(Integer, ForeignKey('groups.groupID'), primary_key=True)
    startingDate = Column(Date, default=func.now())

class Group(Base):
    __tablename__ = 'groups'
    groupID = Column(Integer, primary_key=True, index=True)
    ownerID = Column(Integer, ForeignKey('users.userID'))
    title = Column(String)
    description = Column(String)
    maxUsers = Column(Integer)

class Date(Base):
    __tablename__ = 'dates'
    groupID = Column(Integer, ForeignKey('groups.groupID'), primary_key=True)
    date = Column(Date)
    place = Column(String)
    maxUsers = Column(Integer)

    group = relationship("Group")

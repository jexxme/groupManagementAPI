# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Change these lines
import crud
import models
import schemas
import dependencies
import database

# Create database tables
database.init_db()

app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Similarly, add routes for Group, Date, and UserInGroup.

# crud.py
from sqlalchemy.orm import Session
import models
import schemas


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, passwordHash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Similarly, add CRUD functions for Group, Date, and UserInGroup.


# Add this function to your crud.py

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

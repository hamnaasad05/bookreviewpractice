from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import hashlib

from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.models import Users

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    stmt = select(Users)
    users = db.scalars(stmt).all()
    return users

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(Users, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    created_user = Users(name=user.name, email=user.email, hashed_password=hashed)
    db.add(created_user)
    try:
        db.commit()
        db.refresh(created_user) # this means go back to the database and refresh this Python object's values with the values that exist in the database e.g. id
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered.")
    return created_user





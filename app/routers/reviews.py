from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Reviews, Users, Books
from app.schemas import ReviewCreate, ReviewUser, ReviewBook, ReviewResponse

router = APIRouter()

@router.get("/books/{isbn}/reviews",response_model=list[ReviewResponse])
def get_book_reviews(isbn: str, db: Session = Depends(get_db)):
    stmt = select(Reviews).where(Reviews.book_id==isbn)
    reviews = db.scalars(stmt).all()
    return reviews

@router.get("/users/{userid}/reviews", response_model=list[ReviewResponse])
def get_user_reviews(userid: int, db: Session= Depends(get_db)):
    user = db.get(Users, userid)
    if user is None:
        raise HTTPException(status_Code=404, detail="User not found!")
    return user.reviews

@router.post("/reviews", response_model=ReviewResponse, status_code=201)
def create_review(review: ReviewCreate, db: Session= Depends(get_db)):
    user = db.get(Users, review.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    book = db.get(Books, review.book_isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")

    created_review = Reviews(user_id= review.user_id, book_id= review.book_isbn , text_content= review.text_content, star_count= review.star_count)
    db.add(created_review)
    try:
        db.commit()
        db.refresh(created_review)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="The user has already reviewed this book.")
    return created_review

@router.get("/books/{isbn}/reviewers")
def get_users_who_reviewed_a_book(isbn: str, db: Session = Depends(get_db)):
    # SQL Query:
    # SELECT Users.name FROM Users JOIN Reviews ON (Users.id=Reviews.user_id) WHERE Reviews.bood_id = isbn
    stmt = select(Users.name).join(Reviews, Users.id==Reviews.user_id).where(Reviews.book_id==isbn)
    names = db.scalars(stmt).all()
    return names

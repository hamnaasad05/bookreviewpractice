from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas import BookCreate, BookResponse
from app.models import Books

router = APIRouter()

@router.get("/", response_model=list[BookResponse])
def get_books(genre: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Books)
    if genre is not None:
        stmt = stmt.where(Books.genre == genre)
    books = db.scalars(stmt).all()
    return books

@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = db.get(Books, isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    created_book = Books(isbn= book.isbn, name= book.name, author= book.author, genre= book.genre)
    db.add(created_book)
    try:
        db.commit()
        db.refresh(created_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN already registered.")
    
    return created_book




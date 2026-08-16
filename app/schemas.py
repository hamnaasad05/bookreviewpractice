# Pydantic -- what the API accepts/returns
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        from_attributes= True
    
class BookCreate(BaseModel):
    isbn: str
    name: str
    author: str
    genre: str

class BookResponse(BaseModel):
    isbn: str
    name: str
    author: str
    genre: str
    class Config:
        from_attributes= True

class ReviewCreate(BaseModel):
    user_id: int
    book_isbn: str
    text_content: str | None = None
    star_count: int

class ReviewUser(BaseModel):
    name: str
    class Config:
        from_attributes= True

class ReviewBook(BaseModel):
    isbn: str
    name: str
    class Config:
        from_attributes= True


class ReviewResponse(BaseModel):
    id: int
    user: ReviewUser
    book: ReviewBook
    text_content: str | None
    star_count: int
    class Config:
        from_attributes= True
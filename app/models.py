from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    reviews = relationship("Reviews", back_populates="user")

class Books(Base):
    __tablename__ = "Books"
    isbn = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    
    reviews = relationship("Reviews", back_populates="book")

class Reviews(Base):
    __tablename__ = "Reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)
    book_id = Column(String, ForeignKey("Books.isbn"), nullable=False, index=True)
    text_content = Column(String)
    star_count = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "book_id", name="uq_user_book_review"),) # same user cannot review same book twice

    user = relationship("Users", back_populates="reviews")
    book = relationship("Books", back_populates="reviews")

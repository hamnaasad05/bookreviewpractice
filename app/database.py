import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine) #session factory
Base = declarative_base()

# a FastAPI convention which hands each request its own session and closes it afterward
def get_db():
    db = SessionLocal()
    try:
        yield db # returns db to FastAPI and pauses the function
    finally:
        db.close()


from fastapi import FastAPI
from app.routers import users, books, reviews

app = FastAPI(title="Book Review App")

app.include_router(users.router, prefix="/users")
app.include_router(books.router, prefix="/books")
app.include_router(reviews.router)
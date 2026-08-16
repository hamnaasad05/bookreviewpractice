from app.database import SessionLocal
from app.models import Users, Books, Reviews
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def seed_database():
    db = SessionLocal()
    try:
        users=[
            Users(
                name="Hamna Asad",
                email="hamna@example.com",
                hashed_password=hash_password("hamnapwd123")
            ),
            Users(
                name="Varisha Tauseef",
                email="varisha@example.com",
                hashed_password=hash_password("varishapwd")
            ),
            Users(
                name="Fatema Alam",
                email="fatema@example.com",
                hashed_password=hash_password("123fatema")
            ),
        ]
        db.add_all(users)
        db.flush()

        books=[
            Books(
                isbn="9780132350884",
                name="Clean Code",
                author="Robert C. Martin",
                genre="Programming"
            ),
            Books(
                isbn="9780135957059",
                name="The Pragmatic Programmer",
                author="Andrew Hunt",
                genre="Programming"
            ),
            Books(
                isbn="9780743273565",
                name="The Great Gatsby",
                author="F. Scott Fitzgerald",
                genre="Classic"
            ),
        ]
        db.add_all(books)
        db.flush()

        reviews=[
            Reviews(
                user_id=users[0].id,
                book_id=books[0].isbn,
                text_content="A very useful book for learning good programming practices.",
                star_count=5
            ),
            Reviews(
                user_id=users[1].id,
                book_id=books[0].isbn,
                text_content="Great concepts, although some examples feel dated.",
                star_count=4
            ),
            Reviews(
                user_id=users[1].id,
                book_id=books[1].isbn,
                text_content="One of my favourite software development books.",
                star_count=5
            ),
            Reviews(
                user_id=users[2].id,
                book_id=books[2].isbn,
                text_content="A classic with an interesting story and characters.",
                star_count=4
            ),
        ]
        db.add_all(reviews)
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
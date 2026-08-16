# Book Review API

A minimal book review backend — FastAPI + SQLAlchemy + PostgreSQL, containerized with Docker.

## Tables
- **users** — id, username, email, hashed_password
- **books** — id, name, author, genre
- **reviews** — id, user_id (FK), book_id (FK), text_content, stars

## Run it

1. Clone this repo
2. Copy `.env.example` to `.env`
3. Start the containers by running `docker compose up --build -d`
4. Seed sample data: `docker compose exec app python -m app.seed`
5. Open `http://localhost:8000/docs` to test the endpoints

## Notes
- Password hashing uses SHA-256 as a simplification; production would use bcrypt/argon2.
- Schema migrations are managed with Alembic (see `alembic/versions/`).
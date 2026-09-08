from sqlalchemy import text

from app.db.database import Base, engine
from app.db import models

def init_db() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)
    print("Database ready: pgvector enabled, tables created.")

if __name__ == "__main__":
    init_db()
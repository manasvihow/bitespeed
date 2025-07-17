import os
from sqlmodel import create_engine, SQLModel

# Use the DATABASE_URL from environment variables, with a fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
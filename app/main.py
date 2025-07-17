from fastapi import FastAPI
from .database import create_db_and_tables
from .routes import identify

app = FastAPI()

app.include_router(identify.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Bitespeed Identity Service is running!"}
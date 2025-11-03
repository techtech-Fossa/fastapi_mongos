from fastapi import FastAPI
from sqlalchemy import create_engine
from pymongo import MongoClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL and MongoDB"}

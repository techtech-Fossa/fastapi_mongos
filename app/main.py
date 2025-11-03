from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL and MongoDB"}

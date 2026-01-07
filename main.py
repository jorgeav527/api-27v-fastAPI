from fastapi import FastAPI, Depends
from pymongo import MongoClient
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_USER = os.getenv("MONGO_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    client = MongoClient(MONGO_USER)
    try:
        db = client["fastapi3"]
        yield db
    finally:
        client.close()

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str

@app.post("/post/create-json-data")
async def create_one_post_json_data(post: PostBase, db=Depends(get_db)):
    new_post = {
        "title": post.title,
        "content": post.content,
        "created": datetime.now()
    }
    result = db["post"].insert_one(new_post)
    created_post = db["post"].find_one({"_id": result.inserted_id})
    return {
        "id": str(created_post["_id"]),
        "title": created_post["title"],
        "content": created_post["content"],
        "created": created_post["created"].isoformat()
    }

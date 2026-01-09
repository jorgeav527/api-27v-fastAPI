from fastapi import FastAPI, Depends, Form, HTTPException, Path, Query, Header
from pymongo import MongoClient
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import os
from bson import ObjectId

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


# En otro achivo
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


@app.get("/")
async def check():
    # Hacer un ping para ver si hay una coneccion a la base de datos
    return {"message": "Welcome to the API"}


@app.get("/post/list")
async def get_all_post(db=Depends(get_db)):
    posts = []
    for post in db["post"].find():
        posts.append(
            {
                "id": str(post["_id"]),
                "title": post["title"],
                "content": post["content"],
                "created": post.get("created", datetime.now()).isoformat(),
            }
        )
    return {"posts": posts}


@app.get("/post/{post_id}")
async def get_one_post(
    post_id: str = Path(
        ...,
        description="ID del post a obtener",
        min_length=24,
        max_length=24,
        pattern="^[0-9a-fA-F]{24}$",
    ),
    db=Depends(get_db),
):
    try:
        post = db["post"].find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return {
            # generar un eschema para visualizar este retorno
            "id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "created": post.get("created", datetime.now()).isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/posts/buscar/")
def buscar_posts(
    titulo: str | None = Query(None, min_length=1, max_length=255, description="Filtrar por título"),
    contenido: str | None = Query(None, min_length=1, max_length=255, description="Filtrar por contenido"),
    db = Depends(get_db)
):
    try:
        filtro = {}
        if titulo:
            filtro["title"] = {"$regex": titulo, "$options": "i"}
        if contenido:
            filtro["content"] = {"$regex": contenido, "$options": "i"}

        posts = []
        for post in db["post"].find(filtro):
            posts.append({
            "id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"],
            "created": post.get("created", datetime.now()).isoformat()
        })
        return {"total": len(posts), "posts": posts}
    except Exception as e:
        return {"error": str(e)}



@app.post("/post/create-json-data")
async def create_one_post_json_data(post: PostBase, db=Depends(get_db)):
    try:
        new_post = {
            "title": post.title,
            "content": post.content,
            "created": datetime.now(),
        }
        result = db["post"].insert_one(new_post)
        created_post = db["post"].find_one({"_id": result.inserted_id})
        return {
            "id": str(created_post["_id"]),
            "title": created_post["title"],
            "content": created_post["content"],
            "created": created_post["created"].isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/post/create-form-data")
async def create_one_post_form_data(
    title: str = Form(..., min_length=1, max_length=255),
    content: str = Form(...),
    db=Depends(get_db),
):
    new_post = {"title": title, "content": content, "created": datetime.now()}
    result = db["post"].insert_one(new_post)
    created_post = db["post"].find_one({"_id": result.inserted_id})
    return {
        "id": str(created_post["_id"]),
        "title": created_post["title"],
        "content": created_post["content"],
        "created": created_post["created"].isoformat(),
    }


@app.put("/post/edit/{post_id}")
async def edit_one_post(post_id: str, post: PostBase, db=Depends(get_db)):
    existing_post = db["post"].find_one({"_id": ObjectId(post_id)})
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    updated_data = {"title": post.title, "content": post.content}
    db["post"].update_one({"_id": ObjectId(post_id)}, {"$set": updated_data})
    updated_post = db["post"].find_one({"_id": ObjectId(post_id)})
    return {
        "id": str(updated_post["_id"]),
        "title": updated_post["title"],
        "content": updated_post["content"],
        "created": updated_post.get("created", datetime.now()).isoformat(),
    }


@app.delete("/post/delete/{post_id}")
async def delete_one_post(post_id: str, db=Depends(get_db)):
    post = db["post"].find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db["post"].delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted successfully"}


@app.get("/posts/secure/")
def obtener_posts_secure(
    authorization: str = Header(..., alias="Authorization", description="Token en formato 'Bearer <token>'"),
    db=Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=400,
            detail="Formato de token inválido. Use 'Bearer <token>'"
        )
    token = authorization[7:]

    if token != "secreto123":
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    posts = []
    for post in db["post"].find():
        posts.append(
            {
                "id": str(post["_id"]),
                "title": post["title"],
                "content": post["content"],
                "created": post.get("created", datetime.now()).isoformat(),
            }
        )
    return {"posts": posts}

# Hacer un enpoint para agregar cookies dentro del navegador
# Para Eliminarlo
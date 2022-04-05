from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


# title str, content str, category, Bool published
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # giving it a default value
    rating: Optional[int] = None  # fully optional field


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/createposts")
def create_posts(post: Post):
    print(post.rating)
    print(post.dict())
    return {"data": post}

# title str, content str, category, Bool published

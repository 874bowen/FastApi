from random import randrange
from typing import Optional

from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


# title str, content str, category, Bool published
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # giving it a default value
    rating: Optional[int] = None  # fully optional field


# our database as of now
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like Chapati", "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_posts_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    print(post.rating)
    print(post.dict())
    return {"data": post_dict}


@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"latest_post": post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    print(id)
    print(type(id))
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_posts_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    my_posts.pop(index)
    # return {"message": f"post {id} was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_posts_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

# for documentation go to /docs or /redoc

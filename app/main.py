import time
from random import randrange
from typing import Optional

from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


# title str, content str, category, Bool published
class Post(BaseModel):
    """
        This is going to give us a schema on how
        the created data should look like -
        providing validation
    """
    title: str
    content: str
    published: bool = True  # giving it a default value
    rating: Optional[int] = None  # fully optional field


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='123Bowen', cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connection was successful!!")
        break

    except Exception as error:
        print("Database connection failed!!")
        print("Error: ", error)
        time.sleep(2)

# our database as of now
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like Chapati", "id": 2}]


def find_posts(id):
    """
        used to find posts for delete,
        update and retrieving individual posts purposes
    """
    for p in my_posts:
        if p['id'] == id:
            return p


def find_posts_index(id):
    """:
         used to get index
    """
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
async def get_posts():
    """
        used for retrieving all posts
    """
    curr.execute(""" SELECT * FROM posts """)
    posts = curr.fetchall()
    return {"data": posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    """
    used for creating posts
    :param post:
    :return:
    """
    # we are using variables %s because we want to avoid SQL injection
    curr.execute(""" INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING * """, (post.title,
                 post.content, post.published))
    new_post = curr.fetchone()
    # this only does not save to the database you have to add this: commit()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
async def get_latest_post():
    """
        this function gets the last post
    """
    post = my_posts[len(my_posts) - 1]
    return {"latest_post": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    """
    this is used to get individual post
    :param id:
    :return:
    """
    curr.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = curr.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """:cvar
    for deleting individual post
    :param id:
    """
    curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = curr.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    my_posts.pop(index)
    # return {"message": f"post {id} was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    """:param id:
    for updating a post
    """
    index = find_posts_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

# for documentation go to /docs or /redoc

import time
from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

# specifying the hashing algorithm - bcrypt
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# for testing purposes
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


@app.get("/sqlalchemy")
async def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/posts/latest")
async def get_latest_post():
    """
        this function gets the last post
    """
    post = my_posts[len(my_posts) - 1]
    return {"latest_post": post}

# for documentation go to /docs or /redoc

import time
from random import randrange
from typing import Optional

from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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
    # rating: Optional[int] = None  # fully optional field


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


@app.get("/sqlalchemy")
async def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    """
        used for retrieving all posts
    """
    # curr.execute(""" SELECT * FROM posts """)
    # posts = curr.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    """
    used for creating posts
    :param post:
    :param db:
    :return:
    """
    # we are using variables %s because we want to avoid SQL injection
    # curr.execute(""" INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING * """, (post.title,
    # new_post = curr.fetchone()
    # this only does not save to the database you have to add this: commit()
    # conn.commit()
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
async def get_latest_post():
    """
        this function gets the last post
    """
    post = my_posts[len(my_posts) - 1]
    return {"latest_post": post}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    """
    this is used to get individual post
    :param id:
    :param db:
    :return:
    """
    # curr.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = curr.fetchone()
    # .first is used for getting just one not wasting postgreSQL resources by using .all()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """:cvar
    for deleting individual post
    :param id:
    :param db:
    """
    # curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = curr.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    """    :param post: 
    :param id:
    :param db:
    for updating a post
    """
    # curr.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #              (post.title, post.content, post.published, str(id)))
    # updated_post = curr.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_be_updated = post_query.first()
    if post_to_be_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

# for documentation go to /docs or /redoc

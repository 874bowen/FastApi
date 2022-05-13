# CRUD operation using ORM
from typing import List

from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    """
    used to CREATE posts
    :param current_user:
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
    print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
        used to READ all posts
    """
    # curr.execute(""" SELECT * FROM posts """)
    # posts = curr.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    """
    this is used to READ an individual post
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

    return post


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    """
    :param current_user:
    :param post:
    :param id:
    :param db:
    for updating a post
    """
    # curr.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #              (post.title, post.content, post.published, str(id)))
    # updated_post = curr.fetchone()
    # conn.commit()
    print(type(current_user))
    print('this is', current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_be_updated = post_query.first()
    if post_to_be_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    """
    :param current_user:
    :cvar
    for to DELETE an individual post
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
    # return post.first()

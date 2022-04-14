# CRUD operation using ORM
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users"
)


@router.get("/")
async def get_reg_org_unit(db: Session = Depends(get_db)):
    """
        used to READ all posts
    """
    curr.execute(""" SELECT * FROM posts """)
    posts = curr.fetchall()
    # posts = db.query(models.Post).all()
    return posts
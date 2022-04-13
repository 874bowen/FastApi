# CRUD operation using ORM
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.CreatUser, db: Session = Depends(get_db)):
    """
    :param db:
    :param user:
    used to CREATE USERS with hashed passwords
    """
    # hash the password user.password
    hashed_password = utils.hash_pwd(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return user

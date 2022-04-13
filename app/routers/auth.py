from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["authentication"]
)


@router.get("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access token": access_token, "token_type": "bearer"}

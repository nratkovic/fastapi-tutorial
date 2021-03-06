from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from .. import models
from .. import schemas
from ..database import get_db
from ..utils import email_sender
from ..utils import password_verifier

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):

    users_db = db.query(models.User).all()
    return users_db


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user_db = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )
    return user_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    invalid_password_exception = HTTPException(
        status_code=400,
        detail="Invalid password! Make sure it is at lest 8 letters, "
        "has at least one capital letter, number and special character",
    )

    # validate password
    valid_password = password_verifier.validate_password(
        user.password, invalid_password_exception
    )

    # hash a user password - user.password
    hashed_password = password_verifier.hash_password(valid_password)
    user.password = hashed_password

    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    new_user = models.User(**user.dict())

    if user_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists",
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    email_sender.send_confirmation_email(new_user.email)

    return new_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == user_id)

    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )

    user_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

    invalid_password_exception = HTTPException(
        status_code=400,
        detail="Invalid password! Make sure it is at lest 8 letters, "
        "has at least one capital letter, number and special character",
    )

    # validate password
    valid_password = password_verifier.validate_password(
        user.password, invalid_password_exception
    )

    # hash a user password - user.password
    hashed_password = password_verifier.hash_password(valid_password)
    user.password = hashed_password

    user_query = db.query(models.User).filter(models.User.id == user_id)

    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )

    email_query = db.query(models.User).filter(models.User.email == user.email)

    if email_query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists",
        )

    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

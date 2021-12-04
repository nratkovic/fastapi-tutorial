from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from .. import models
from .. import oauth2
from .. import schemas
from ..utils import password_verifier

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # OAuth2PasswordRequestForm returns username and password
    # {"username" = "test", "password" = "test"}
    user_db = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    if not password_verifier.verify_password(
        user_credentials.password, user_db.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # create a token
    access_token = oauth2.create_access_token(data={"uid": user_db.id})

    return {"access_token": access_token, "token_type": "bearer"}

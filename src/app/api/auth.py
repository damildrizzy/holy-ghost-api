from typing import Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from . import schemas, crud, deps
from app.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()


@router.post("login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise (HTTPException(status_code=400, detail="Incorrect Login Details"))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

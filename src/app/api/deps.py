from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database import SessionLocal
from app.models import User
from app.security import SECRET_KEY, ALGORITHM
from .schemas import TokenPayload
from .crud import get_user


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/access-token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_schema)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = get_user(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

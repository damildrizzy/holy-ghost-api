from fastapi import Depends
from fastapi.routing import APIRouter, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from gibberish import Gibberish

from app.models import Tongue, User
from . import schemas
from .deps import get_db, get_current_user

router = APIRouter()
gib = Gibberish()
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=schemas.Tongue)
@limiter.limit("10/minute")
def get_tongues(
    request: Request,
    tongue: schemas.TongueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Tongue:
    db_tongue = db.query(Tongue).filter(Tongue.raw_string == tongue.raw_string).first()
    if db_tongue:
        return db_tongue
    else:
        num_of_words = len(tongue.raw_string.split())
        tongues_string = " ".join(gib.generate_words(num_of_words))
        tongue_obj = Tongue(raw_string=tongue.raw_string, tongues_string=tongues_string)
        db.add(tongue_obj)
        db.commit()
        db.refresh(tongue_obj)
        return tongue_obj

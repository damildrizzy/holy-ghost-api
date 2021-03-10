from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from gibberish import Gibberish

from app.models import Tongue

from . import schemas
from .deps import get_db

router = APIRouter()
gib = Gibberish()


@router.post("/", response_model=schemas.Tongue)
def get_tongues(tongue: schemas.Tongue, db: Session = Depends(get_db)):
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

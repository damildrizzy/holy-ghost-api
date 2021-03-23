import emoji
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api import users, auth, tongues
from . import models
from .database import engine
from app.api.tongues import limiter

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title=emoji.emojize("Holy Ghost API :fire: :fire: :fire:"))
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(tongues.router, prefix="/tongues", tags=["tongues"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
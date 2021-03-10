from fastapi import FastAPI
from app.api import users, auth, tongues
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tongues.router, prefix="/tongues", tags=["tongues"])

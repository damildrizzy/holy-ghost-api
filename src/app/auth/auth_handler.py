from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token: str):
    return {"access_token": token}

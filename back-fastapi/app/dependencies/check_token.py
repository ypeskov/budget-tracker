from typing import Annotated

import jwt
from fastapi import Header, Request, HTTPException, status
from icecream import ic

from app.config import Settings

ic.configureOutput(includeContext=True)

settings = Settings()

SECRET_KEY = settings.SECRET_KEY


async def check_token(request: Request, auth_token: Annotated[str, Header()]) -> dict:
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        request.state.user = payload
        return payload
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

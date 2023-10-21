from pprint import pp
from typing import Annotated

import jwt
from fastapi import Header, Request, HTTPException, status

SECRET_KEY = "your-secret-key"


async def check_token(request: Request, auth_token: Annotated[str, Header()] = None) -> dict:
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        request.state.user = payload
        return payload
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")


import json
from datetime import timedelta

from fastapi import Request
from fastapi.responses import Response
from icecream import ic

from app.services.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

ic.configureOutput(includeContext=True)

async def update_token(request: Request, call_next):
    response = await call_next(request)

    if not hasattr(request.state, "user"):
        return response

    content_type = response.headers.get("content-type", "")
    if content_type.lower().startswith("application/json"):
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response_json = json.loads(response_body.decode("utf-8"))
        modified_response = json.dumps(response_json).encode("utf-8")


        user = request.state.user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_payload = create_access_token(user, access_token_expires)
        # decoded_payload = jwt.decode(new_payload, SECRET_KEY, algorithms=["HS256"])

        response.headers['Content-Length'] = str(len(modified_response))
        response.headers['new_access_token'] = new_payload
        response.headers["Access-Control-Expose-Headers"] = "new_access_token"

        return Response(content=json.dumps(response_json).encode("utf-8"),
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type)

    return response
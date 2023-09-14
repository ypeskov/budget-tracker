import uvicorn
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.accounts import router as accounts_router
from app.routes.test_check import router as test_router

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app = FastAPI()

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(accounts_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

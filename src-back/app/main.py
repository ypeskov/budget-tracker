import uvicorn
from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.test_check import router as test_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(test_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

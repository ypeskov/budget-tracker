from pprint import pprint
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

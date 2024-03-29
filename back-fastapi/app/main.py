import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.accounts import router as accounts_router
from app.routes.transations import router as transaction_router
from app.routes.categories import router as category_router
from app.routes.currencies import router as currency_router

from icecream import install
install()


app = FastAPI()

origins = ['*', ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(currency_router)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)

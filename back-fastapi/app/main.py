# import debugpy
# debugpy.listen(('0.0.0.0', 5678))
# debugpy.wait_for_client()
# print("Debugger is attached!")


# import sys
# sys.path.append("<PyCharm directory>/debug-egg/pydevd-pycharm.egg")
# # pydevd_pycharm.settrace('host.docker.internal', port=5678, stdoutToServer=True, stderrToServer=True, suspend=False)
# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from icecream import ic, install
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import Settings
from app.middleware.token_update import update_token
from app.routes.accounts import router as accounts_router
from app.routes.analytics import router as analytics_router
from app.routes.auth import router as auth_router
from app.routes.budgets import router as budgets_router
from app.routes.categories import router as category_router
from app.routes.currencies import router as currency_router
from app.routes.exchange_rates import router as exchange_rates_router
from app.routes.financial_planning import router as financial_planning_router
from app.routes.management import router as management_router
from app.routes.planned_transactions import router as planned_transactions_router
from app.routes.reports import router as reports_router
from app.routes.transations import router as transaction_router
from app.routes.user_settings import router as settings_router

install()

settings = Settings()
is_production = (settings.ENVIRONMENT == 'prod')

app = FastAPI(redirect_slashes=True,
              docs_url=None if is_production else "/docs",
              redoc_url=None if is_production else "/redoc")

origins = ['*', ]
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=update_token)

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(currency_router)
app.include_router(settings_router)
app.include_router(exchange_rates_router)
app.include_router(reports_router)
app.include_router(management_router)
app.include_router(budgets_router)
app.include_router(analytics_router)
app.include_router(planned_transactions_router)
app.include_router(financial_planning_router)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)

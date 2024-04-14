from datetime import datetime

from icecream import ic
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.Transaction import Transaction
from app.services.errors import AccessDenied
from app.models.Account import Account

ic.configureOutput(includeContext=True)


def get_account_flow(user_id: int,
                     db: Session,
                     account_id: int,
                     start_date: datetime | None,
                     end_date: datetime | None) -> dict:
    """ Get all expenses for one account within a given time period """
    account = db.query(Account).filter(Account.id == account_id).one()
    if account.user_id != user_id:
        raise AccessDenied(f'User {user_id} does not have access to account {account_id}')

    query = db.query(
        func.sum(func.coalesce(Transaction.amount, 0)).filter(Transaction.is_income == True).label('total_income'),
        func.sum(func.coalesce(Transaction.amount, 0)).filter(Transaction.is_income == False).label('total_expenses')
    ).filter(Transaction.account_id == account_id)

    filters = []
    if start_date:
        filters.append(Transaction.date_time >= start_date)
    if end_date:
        filters.append(Transaction.date_time <= end_date)

    if filters:
        query = query.filter(*filters)

    result = query.one()

    total_income = result.total_income or 0
    total_expenses = result.total_expenses or 0
    net_flow = total_income - total_expenses

    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_flow': net_flow,
    }

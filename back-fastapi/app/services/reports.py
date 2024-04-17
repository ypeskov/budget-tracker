from datetime import datetime
from decimal import Decimal

from icecream import ic
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.Transaction import Transaction
from app.services.errors import AccessDenied
from app.models.Account import Account

ic.configureOutput(includeContext=True)


def get_cash_flows(user_id: int,
                   db: Session,
                   account_ids:list[int],
                   start_date: datetime | None,
                   end_date: datetime | None) -> list[dict]:
    """ Get all expenses for accounts within a given time period """
    accounts = (db.query(Account)
                .filter(Account.id.in_(account_ids))
                .filter(Account.user_id == user_id)
                .all())

    query = db.query(
        Transaction.account_id,
        func.sum(func.coalesce(Transaction.amount, 0)).filter(Transaction.is_income == True).label('total_income'),
        func.sum(func.coalesce(Transaction.amount, 0)).filter(Transaction.is_income == False).label('total_expenses')
    ).filter(Transaction.account_id.in_(account_ids))

    filters = []
    if start_date:
        filters.append(Transaction.date_time >= start_date)
    if end_date:
        filters.append(Transaction.date_time <= end_date)

    if filters:
        query = query.filter(*filters)

    query = query.group_by(Transaction.account_id)
    results = query.all()

    cash_flows = []
    for result in results:
        ic(result)
        account_id, total_income, total_expenses = result
        total_income = Decimal(total_income or 0)
        total_expenses = Decimal(total_expenses or 0)
        net_flow = total_income - total_expenses
        cash_flows.append({
            'account_id': account_id,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_flow': net_flow
        })

    return cash_flows

from datetime import datetime, timedelta
from decimal import Decimal

from icecream import ic
from sqlalchemy import case, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction

ic.configureOutput(includeContext=True)


def get_cash_flows(user_id: int,
                   db: Session,
                   account_ids: list[int],
                   start_date: datetime | None,
                   end_date: datetime | None,
                   period: str = 'monthly') -> list[dict]:
    """ Get all cash flow transactions for accounts within a given time period and additional account information """

    accounts = db.query(
        Account.id,
        Account.name,
        Currency.code.label("currency")
    ).filter(
        Account.id.in_(account_ids),
        Account.user_id == user_id
    ).join(
        Currency, Account.currency_id == Currency.id
    ).all()

    account_info = {account.id: {"name": account.name, "currency": account.currency} for account in accounts}

    if period == 'monthly':
        label = 'transactions_month'
        period_str = 'YYYY-MM'
    elif period == 'daily':
        label = 'transactions_day'
        period_str = 'YYYY-MM-DD'
    else:
        raise ValueError(f"Invalid period: {period}")

    query = (
        db.query(
            Account.id.label('account_id'),
            func.to_char(Transaction.date_time, period_str).label(label),
            func.coalesce(func.sum(case((Transaction.is_income == True, Transaction.amount), else_=0))
                          .filter(Transaction.is_deleted == False), 0).label('total_income'),
            func.coalesce(func.sum(case((Transaction.is_income == False, Transaction.amount), else_=0))
                          .filter(Transaction.is_deleted == False), 0).label('total_expenses')
        )
        .outerjoin(Transaction, and_(Account.id == Transaction.account_id, Transaction.account_id.in_(account_ids)))
        .filter(Account.user_id == user_id, Account.id.in_(account_ids))
        .filter(Account.user_id == user_id, Account.id.in_(account_ids))
        .group_by(Account.id, func.to_char(Transaction.date_time, period_str))
    )

    additional_filters = []
    if start_date:
        additional_filters.append(Transaction.date_time >= start_date)
    if end_date:
        additional_filters.append(Transaction.date_time <= (end_date + timedelta(days=1)))

    if additional_filters:
        query = query.filter(*additional_filters)

    query = query.group_by(Transaction.account_id, Account.id,)
    results = query.all()

    cash_flows = []
    for result in results:
        account_id, period, total_income, total_expenses = result
        total_income = Decimal(total_income or 0)
        total_expenses = Decimal(total_expenses or 0)
        net_flow = total_income - total_expenses

        cash_flow = {
            'account_id': account_id,
            'account_name': account_info[account_id]["name"],
            'currency': account_info[account_id]["currency"],
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_flow': net_flow,
            'period': period,
        }

        cash_flows.append(cash_flow)

    return cash_flows

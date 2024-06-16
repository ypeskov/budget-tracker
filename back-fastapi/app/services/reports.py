from datetime import datetime, date
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger

from app.services.reports_generators.CashFlowReportGenerator import CashFlowReportGenerator
from app.services.reports_generators.BalanceReportGenerator import BalanceReportGenerator
from app.services.reports_generators.ExpensesReportGenerator import ExpensesReportGenerator

ic.configureOutput(includeContext=True)


def get_cash_flows(user_id: int,
                   db: Session,
                   start_date: datetime | None,
                   end_date: datetime | None,
                   period: str = 'monthly') -> list[dict]:
    """ Get all cash flow transactions for accounts within a given time period and additional account information """
    logger.info(f"Getting cash flow transactions for user_id: {user_id}, "
                f"start_date: {start_date}, end_date: {end_date}, period: {period}")
    cash_flow_generator = CashFlowReportGenerator(user_id, db)
    cash_flow_generator.set_parameters(period, start_date, end_date)

    return cash_flow_generator.get_data()


def get_balance_report(user_id: int,
                       db: Session,
                       account_ids: list[int],
                       balance_date: date | None) -> list[dict]:
    """ Get balance for accounts on a given date """
    balance_report_generator = BalanceReportGenerator(user_id, account_ids, db, balance_date)
    balance_data: list[dict] = balance_report_generator.prepare_raw_data().get_balances()

    return balance_data


def get_expenses_by_categories(user_id: int,
                               db: Session,
                               start_date: datetime,
                               end_date: datetime,
                               categories_ids: list = None) -> dict:
    """ Get all expenses within a given time period """

    expenses_report_generator = ExpensesReportGenerator(user_id, db, start_date, end_date, categories_ids)
    expenses = expenses_report_generator.prepare_data().get_expenses()

    return expenses

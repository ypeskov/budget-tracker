from datetime import datetime
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.services.reports_generators.CashFlowGenerator import CashFlowGenerator


ic.configureOutput(includeContext=True)


def get_cash_flows(user_id: int,
                   db: Session,
                   account_ids: list[int],
                   start_date: datetime | None,
                   end_date: datetime | None,
                   period: str = 'monthly') -> list[dict]:
    """ Get all cash flow transactions for accounts within a given time period and additional account information """
    logger.info(f"Getting cash flow transactions for user_id: {user_id}, account_ids: {account_ids}, "
                f"start_date: {start_date}, end_date: {end_date}, period: {period}")
    cash_flow_generator = CashFlowGenerator(user_id, db)
    cash_flow_generator.set_parameters(account_ids, period, start_date, end_date)

    return cash_flow_generator.get_data()

from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.config import Settings
from app.logger_config import logger
from app.services.analytics import prompts
from app.services.analytics.data_processor import ExpenseDataProcessor
from app.services.analytics.openai_client import OpenAIClient


class ExpenseAnalyzer:
    def __init__(self, settings: Settings, db: Session, user_id: int):
        self.settings = settings
        self.db = db
        self.user_id = user_id
        self.openai_client = OpenAIClient(settings)
        self.data_processor = ExpenseDataProcessor(db, user_id)

    async def analyze_spending_trends(self,
                                      start_date: date,
                                      end_date: date,
                                      limit: int = 50 # -1 for all
                                      ) -> Optional[str]:
        try:
            transactions = self.data_processor.get_transactions_data(start_date, end_date, limit)

            if not transactions:
                return "Not enough data to analyze spending trends."

            formatted_data = self.data_processor.format_for_analysis(transactions)

            analysis = await self.openai_client.analyze_expenses(prompts.SPENDING_TRENDS_PROMPT, formatted_data)

            logger.info(f"Spending trends analysis completed for user {self.user_id}")
            return analysis

        except Exception as e:
            logger.error(f"Error in spending trends analysis: {str(e)}")
            return "Error analyzing spending trends."

    async def analyze_expense_categorization(self, start_date: date, end_date: date) -> Optional[str]:
        try:
            transactions = self.data_processor.get_transactions_data(start_date, end_date, 75)

            if not transactions:
                return "Недостаточно данных для анализа категоризации расходов."

            # Focus on transactions with labels for better categorization analysis
            labeled_transactions = [tx for tx in transactions if tx['label']]

            if not labeled_transactions:
                return "Недостаточно транзакций с описаниями для анализа категоризации."

            formatted_data = self.data_processor.format_for_analysis(labeled_transactions)

            analysis = await self.openai_client.analyze_expenses(prompts.EXPENSE_CATEGORIZATION_PROMPT, formatted_data)

            logger.info(f"Expense categorization analysis completed for user {self.user_id}")
            return analysis

        except Exception as e:
            logger.error(f"Error in expense categorization analysis: {str(e)}")
            return "Произошла ошибка при анализе категоризации расходов."

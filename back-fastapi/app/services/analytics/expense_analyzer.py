from datetime import date, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.config import Settings
from app.logger_config import logger
from app.services.analytics.openai_client import OpenAIClient
from app.services.analytics.data_processor import ExpenseDataProcessor
from app.services.analytics import prompts


class ExpenseAnalyzer:
    def __init__(self, settings: Settings, db: Session, user_id: int):
        self.settings = settings
        self.db = db
        self.user_id = user_id
        self.openai_client = OpenAIClient(settings)
        self.data_processor = ExpenseDataProcessor(db, user_id)

    async def analyze_spending_trends(self, start_date: date, end_date: date, limit: int = 50) -> Optional[str]:
        try:
            transactions = self.data_processor.get_transactions_data(start_date, end_date, limit)

            if not transactions:
                return "Недостаточно данных для анализа трендов расходов."

            formatted_data = self.data_processor.format_for_analysis(transactions)

            analysis = await self.openai_client.analyze_expenses(prompts.SPENDING_TRENDS_PROMPT, formatted_data)

            logger.info(f"Spending trends analysis completed for user {self.user_id}")
            return analysis

        except Exception as e:
            logger.error(f"Error in spending trends analysis: {str(e)}")
            return "Произошла ошибка при анализе трендов расходов."

    async def get_budget_recommendations(self, start_date: date, end_date: date) -> Optional[str]:
        try:
            transactions = self.data_processor.get_transactions_data(start_date, end_date, 100)

            if not transactions:
                return "Недостаточно данных для составления рекомендаций по бюджету."

            formatted_data = self.data_processor.format_for_analysis(transactions)
            category_summary = self.data_processor.get_category_summary(start_date, end_date)

            # Add category summary to analysis data
            summary_text = "\n\nСводка по категориям:\n"
            for category, data in category_summary.items():
                if data['expense'] > 0:
                    summary_text += f"- {category}: {data['expense']:.2f} (расходы), {data['count']} транзакций\n"

            formatted_data += summary_text

            recommendations = await self.openai_client.analyze_expenses(
                prompts.BUDGET_RECOMMENDATIONS_PROMPT, formatted_data, max_tokens=400
            )

            logger.info(f"Budget recommendations generated for user {self.user_id}")
            return recommendations

        except Exception as e:
            logger.error(f"Error generating budget recommendations: {str(e)}")
            return "Произошла ошибка при составлении рекомендаций по бюджету."

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

    async def get_financial_insights(self, start_date: date, end_date: date) -> Optional[str]:
        try:
            transactions = self.data_processor.get_transactions_data(start_date, end_date, 100)

            if not transactions:
                return "Недостаточно данных для финансовых инсайтов."

            formatted_data = self.data_processor.format_for_analysis(transactions)
            category_summary = self.data_processor.get_category_summary(start_date, end_date)

            # Add additional context for insights
            context = f"\n\nДополнительный контекст:\n"
            context += f"Количество уникальных категорий: {len(category_summary)}\n"
            context += f"Период анализа: {(end_date - start_date).days} дней\n"

            formatted_data += context

            insights = await self.openai_client.analyze_expenses(
                prompts.FINANCIAL_INSIGHTS_PROMPT, formatted_data, max_tokens=500
            )

            logger.info(f"Financial insights generated for user {self.user_id}")
            return insights

        except Exception as e:
            logger.error(f"Error generating financial insights: {str(e)}")
            return "Произошла ошибка при генерации финансовых инсайтов."

    async def get_monthly_summary(self, month_date: date) -> Optional[str]:
        try:
            # Get first and last day of the month
            start_date = month_date.replace(day=1)
            if start_date.month == 12:
                end_date = start_date.replace(year=start_date.year + 1, month=1) - timedelta(days=1)
            else:
                end_date = start_date.replace(month=start_date.month + 1) - timedelta(days=1)

            transactions = self.data_processor.get_transactions_data(start_date, end_date, 150)

            if not transactions:
                return f"Нет данных о расходах за {month_date.strftime('%B %Y')}."

            formatted_data = self.data_processor.format_for_analysis(transactions)

            summary = await self.openai_client.analyze_expenses(
                prompts.MONTHLY_SUMMARY_PROMPT, formatted_data, max_tokens=250
            )

            logger.info(f"Monthly summary generated for user {self.user_id}, month: {month_date}")
            return summary

        except Exception as e:
            logger.error(f"Error generating monthly summary: {str(e)}")
            return "Произошла ошибка при создании месячного резюме."

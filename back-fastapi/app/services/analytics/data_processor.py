from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.models.Account import Account
from app.logger_config import logger


class ExpenseDataProcessor:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        
    def get_transactions_data(
        self,
        start_date: date,
        end_date: date,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            query = (
                select(
                    Transaction,
                    UserCategory.name.label('category_name'),
                    Account.name.label('account_name')
                )
                .join(UserCategory, Transaction.category_id == UserCategory.id, isouter=True)
                .join(Account, Transaction.account_id == Account.id)
                .where(
                    Transaction.user_id == self.user_id,
                    Transaction.date_time >= start_date,
                    Transaction.date_time <= end_date,
                    ~Transaction.is_transfer  # Exclude transfers
                )
                .order_by(Transaction.date_time.desc())
                .limit(limit)
            )
            
            results = self.db.execute(query).all()
            
            transactions_data = []
            for result in results:
                transaction = result.Transaction
                transactions_data.append({
                    'id': transaction.id,
                    'amount': float(transaction.amount),
                    'date': transaction.date_time.strftime('%Y-%m-%d'),
                    'label': transaction.label or '',
                    'category': result.category_name or 'Без категории',
                    'account': result.account_name,
                    'is_income': transaction.is_income
                })
                
            logger.info(f"Retrieved {len(transactions_data)} transactions for analysis")
            return transactions_data
            
        except Exception as e:
            logger.error(f"Error retrieving transactions data: {str(e)}")
            return []
            
    def format_for_analysis(self, transactions: List[Dict[str, Any]]) -> str:
        if not transactions:
            return "Нет данных о транзакциях для анализа."
            
        # Group by category
        categories = {}
        total_expense = 0
        total_income = 0
        
        for tx in transactions:
            category = tx['category']
            amount = tx['amount']
            
            if tx['is_income']:
                total_income += amount
            else:
                total_expense += amount
                if category not in categories:
                    categories[category] = {'amount': 0, 'count': 0, 'transactions': []}
                categories[category]['amount'] += amount
                categories[category]['count'] += 1
                categories[category]['transactions'].append(tx)
        
        # Format summary
        summary = f"Период: {transactions[-1]['date']} - {transactions[0]['date']}\n"
        summary += f"Общие расходы: {total_expense:.2f}\n"
        summary += f"Общие доходы: {total_income:.2f}\n\n"
        
        # Categories breakdown
        summary += "Расходы по категориям:\n"
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['amount'], reverse=True)
        
        for category_name, data in sorted_categories[:10]:  # Top 10 categories
            summary += f"- {category_name}: {data['amount']:.2f} ({data['count']} транзакций)\n"
            
        # Sample transactions
        summary += f"\nПоследние транзакции:\n"
        for tx in transactions[:5]:  # Last 5 transactions
            summary += f"- {tx['date']}: {tx['amount']:.2f} - {tx['category']} ({tx['label']})\n"
            
        return summary
        
    def get_category_summary(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        try:
            query = (
                select(
                    UserCategory.name,
                    Transaction.amount.label('amount'),
                    Transaction.is_income
                )
                .join(UserCategory, Transaction.category_id == UserCategory.id, isouter=True)
                .where(
                    Transaction.user_id == self.user_id,
                    Transaction.date_time >= start_date,
                    Transaction.date_time <= end_date,
                    ~Transaction.is_transfer
                )
            )
            
            results = self.db.execute(query).all()
            
            category_summary = {}
            for result in results:
                category = result.name or 'Без категории'
                amount = float(result.amount)
                
                if category not in category_summary:
                    category_summary[category] = {'expense': 0, 'income': 0, 'count': 0}
                    
                if result.is_income:
                    category_summary[category]['income'] += amount
                else:
                    category_summary[category]['expense'] += amount
                    
                category_summary[category]['count'] += 1
                
            return category_summary
            
        except Exception as e:
            logger.error(f"Error getting category summary: {str(e)}")
            return {}
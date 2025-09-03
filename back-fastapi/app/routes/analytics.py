from fastapi import APIRouter, Depends, HTTPException, Request, status
from icecream import ic
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.analytics_schema import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    ExpenseCategorizationRequestSchema,
)
from app.services.analytics.expense_analyzer import ExpenseAnalyzer

router = APIRouter(
    tags=['Analytics'],
    prefix='/analytics',
    dependencies=[Depends(check_token)],
)

def get_expense_analyzer(request: Request, db: Session = Depends(get_db)) -> ExpenseAnalyzer:
    if not hasattr(request.state, 'user'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user_id = request.state.user['id']
    return ExpenseAnalyzer(settings, db, user_id)

@router.post('/spending-trends', response_model=AnalysisResponseSchema)
async def analyze_spending_trends(
        request: Request,
        input_data: AnalysisRequestSchema,
        analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Analyze spending trends for the given period using AI.
    """
    logger.info(
        f"Analyzing spending trends for user {request.state.user['id']}, "
        f"period: {input_data.start_date} to {input_data.end_date}"
    )

    try:
        analysis = await analyzer.analyze_spending_trends(input_data.start_date, input_data.end_date, input_data.limit)

        if analysis is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service temporarily unavailable"
            )

        return AnalysisResponseSchema(analysis=analysis)

    except Exception as e:
        logger.error(f"Error analyzing spending trends: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error analyzing spending trends"
        )


@router.post('/expense-categorization/', response_model=AnalysisResponseSchema)
async def analyze_expense_categorization(
        request: Request,
        input_data: ExpenseCategorizationRequestSchema,
        analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer),
) -> AnalysisResponseSchema:
    """
    Analyze and suggest improvements for expense categorization using AI.
    """
    logger.info(
        f"Analyzing expense categorization for user {request.state.user['id']}, "
        f"period: {input_data.start_date} to {input_data.end_date}"
    )

    try:
        analysis = await analyzer.analyze_expense_categorization(input_data.start_date, input_data.end_date)

        if analysis is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис анализа категоризации временно недоступен",
            )

        return AnalysisResponseSchema(analysis=analysis)

    except Exception as e:
        logger.error(f"Error analyzing expense categorization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error analyzing expense categorization",
        )

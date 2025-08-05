from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.config import Settings
from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.analytics_schema import (
    SpendingTrendsRequestSchema,
    BudgetRecommendationsRequestSchema,
    ExpenseCategorizationRequestSchema,
    FinancialInsightsRequestSchema,
    MonthlySummaryRequestSchema,
    AnalysisResponseSchema,
    ErrorResponseSchema
)
from app.services.analytics.expense_analyzer import ExpenseAnalyzer


router = APIRouter(
    tags=['Analytics'],
    prefix='/analytics',
    dependencies=[Depends(check_token)],
)


def get_expense_analyzer(request: Request, db: Session = Depends(get_db)) -> ExpenseAnalyzer:
    settings = Settings()
    user_id = request.state.user['id']
    return ExpenseAnalyzer(settings, db, user_id)


@router.post('/spending-trends/', response_model=AnalysisResponseSchema)
async def analyze_spending_trends(
    request: Request,
    input_data: SpendingTrendsRequestSchema,
    analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Analyze spending trends for the given period using AI.
    """
    logger.info(f"Analyzing spending trends for user {request.state.user['id']}, "
                f"period: {input_data.start_date} to {input_data.end_date}")
    
    try:
        analysis = await analyzer.analyze_spending_trends(
            input_data.start_date,
            input_data.end_date,
            input_data.limit
        )
        
        if analysis is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис анализа временно недоступен"
            )
            
        return AnalysisResponseSchema(analysis=analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing spending trends: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при анализе трендов расходов"
        )


@router.post('/budget-recommendations/', response_model=AnalysisResponseSchema)
async def get_budget_recommendations(
    request: Request,
    input_data: BudgetRecommendationsRequestSchema,
    analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Get AI-powered budget recommendations based on spending history.
    """
    logger.info(f"Generating budget recommendations for user {request.state.user['id']}, "
                f"period: {input_data.start_date} to {input_data.end_date}")
    
    try:
        recommendations = await analyzer.get_budget_recommendations(
            input_data.start_date,
            input_data.end_date
        )
        
        if recommendations is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис рекомендаций временно недоступен"
            )
            
        return AnalysisResponseSchema(analysis=recommendations)
        
    except Exception as e:
        logger.error(f"Error generating budget recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при составлении рекомендаций по бюджету"
        )


@router.post('/expense-categorization/', response_model=AnalysisResponseSchema)
async def analyze_expense_categorization(
    request: Request,
    input_data: ExpenseCategorizationRequestSchema,
    analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Analyze and suggest improvements for expense categorization using AI.
    """
    logger.info(f"Analyzing expense categorization for user {request.state.user['id']}, "
                f"period: {input_data.start_date} to {input_data.end_date}")
    
    try:
        analysis = await analyzer.analyze_expense_categorization(
            input_data.start_date,
            input_data.end_date
        )
        
        if analysis is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис анализа категоризации временно недоступен"
            )
            
        return AnalysisResponseSchema(analysis=analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing expense categorization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при анализе категоризации расходов"
        )


@router.post('/financial-insights/', response_model=AnalysisResponseSchema)
async def get_financial_insights(
    request: Request,
    input_data: FinancialInsightsRequestSchema,
    analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Get personalized financial insights and advice using AI.
    """
    logger.info(f"Generating financial insights for user {request.state.user['id']}, "
                f"period: {input_data.start_date} to {input_data.end_date}")
    
    try:
        insights = await analyzer.get_financial_insights(
            input_data.start_date,
            input_data.end_date
        )
        
        if insights is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис финансовых инсайтов временно недоступен"
            )
            
        return AnalysisResponseSchema(analysis=insights)
        
    except Exception as e:
        logger.error(f"Error generating financial insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при генерации финансовых инсайтов"
        )


@router.post('/monthly-summary/', response_model=AnalysisResponseSchema)
async def get_monthly_summary(
    request: Request,
    input_data: MonthlySummaryRequestSchema,
    analyzer: ExpenseAnalyzer = Depends(get_expense_analyzer)
) -> AnalysisResponseSchema:
    """
    Get AI-generated monthly financial summary.
    """
    logger.info(f"Generating monthly summary for user {request.state.user['id']}, "
                f"month: {input_data.month_date}")
    
    try:
        summary = await analyzer.get_monthly_summary(input_data.month_date)
        
        if summary is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис месячных резюме временно недоступен"
            )
            
        return AnalysisResponseSchema(analysis=summary)
        
    except Exception as e:
        logger.error(f"Error generating monthly summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при создании месячного резюме"
        )
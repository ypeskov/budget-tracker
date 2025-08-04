from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class AnalysisRequestSchema(BaseModel):
    start_date: date = Field(..., description="Start date for analysis period")
    end_date: date = Field(..., description="End date for analysis period")
    limit: Optional[int] = Field(default=50, ge=10, le=2000, description="Maximum number of transactions to analyze")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class SpendingTrendsRequestSchema(AnalysisRequestSchema):
    pass


class BudgetRecommendationsRequestSchema(BaseModel):
    start_date: date = Field(..., description="Start date for analysis period")
    end_date: date = Field(..., description="End date for analysis period")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class ExpenseCategorizationRequestSchema(BaseModel):
    start_date: date = Field(..., description="Start date for analysis period")
    end_date: date = Field(..., description="End date for analysis period")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class FinancialInsightsRequestSchema(BaseModel):
    start_date: date = Field(..., description="Start date for analysis period")
    end_date: date = Field(..., description="End date for analysis period")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class MonthlySummaryRequestSchema(BaseModel):
    month_date: date = Field(..., description="Any date within the month to summarize")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class AnalysisResponseSchema(BaseModel):
    analysis: str = Field(..., description="AI-generated analysis text")
    status: str = Field(default="success", description="Response status")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)


class ErrorResponseSchema(BaseModel):
    error: str = Field(..., description="Error message")
    status: str = Field(default="error", description="Response status")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_camel)

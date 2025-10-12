from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, field_validator
from pydantic.alias_generators import to_camel


class RecurrenceFrequencyEnum(str, Enum):
    """Frequency of recurring transactions"""

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class RecurrenceRuleSchema(BaseModel):
    """
    Schema for recurrence rule configuration.

    Examples:
    - Daily: {"frequency": "daily", "interval": 1, "count": 30}
    - Weekly on Monday: {"frequency": "weekly", "interval": 1, "day_of_week": 0, "end_date": "2025-12-31"}
    - Monthly on 15th: {"frequency": "monthly", "interval": 1, "day_of_month": 15, "count": 12}
    - Yearly: {"frequency": "yearly", "interval": 1, "end_date": "2030-01-01"}
    """

    frequency: RecurrenceFrequencyEnum
    interval: int = Field(
        ge=1, default=1, description="Repeat every N days/weeks/months/years"
    )
    end_date: datetime | None = Field(
        None, description="Optional end date (exclusive with count)"
    )
    count: int | None = Field(
        None,
        ge=1,
        description="Optional number of occurrences (exclusive with end_date)",
    )
    day_of_week: int | None = Field(
        None, ge=0, le=6, description="Day of week for weekly (0=Monday, 6=Sunday)"
    )
    day_of_month: int | None = Field(
        None, ge=1, le=31, description="Day of month for monthly"
    )

    @field_validator('end_date', 'count')
    @classmethod
    def validate_end_condition(cls, v, info):
        """Ensure only one of end_date or count is specified"""
        if v is not None:
            data = info.data
            if 'end_date' in data and 'count' in data:
                if data.get('end_date') is not None and data.get('count') is not None:
                    raise ValueError("Cannot specify both end_date and count")
        return v

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class CreatePlannedTransactionSchema(BaseModel):
    """Schema for creating a planned transaction"""

    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    label: str = ""
    notes: str | None = ""
    is_income: bool
    planned_date: datetime
    is_recurring: bool = False
    recurrence_rule: RecurrenceRuleSchema | None = None

    @field_validator('recurrence_rule')
    @classmethod
    def validate_recurrence_rule(cls, v, info):
        """Ensure recurrence_rule is provided when is_recurring is True"""
        if info.data.get('is_recurring') and v is None:
            raise ValueError("recurrence_rule is required when is_recurring is True")
        if not info.data.get('is_recurring') and v is not None:
            raise ValueError(
                "recurrence_rule should not be provided when is_recurring is False"
            )
        return v

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class UpdatePlannedTransactionSchema(CreatePlannedTransactionSchema):
    """Schema for updating a planned transaction"""

    id: int
    is_active: bool | None = None

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class ResponsePlannedTransactionSchema(BaseModel):
    """Schema for planned transaction response"""

    id: int
    user_id: int
    currency_id: int
    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    label: str
    notes: str | None
    is_income: bool
    planned_date: datetime
    is_recurring: bool
    recurrence_rule: dict | None
    is_executed: bool
    executed_transaction_id: int | None
    execution_date: datetime | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class PlannedTransactionOccurrenceSchema(BaseModel):
    """
    Schema for a single occurrence of a recurring planned transaction.
    Used in projection calculations.
    """

    planned_transaction_id: int
    occurrence_date: datetime
    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    is_income: bool
    label: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class FutureBalanceRequestSchema(BaseModel):
    """Schema for requesting future balance calculation"""

    target_date: datetime
    account_ids: list[int] | None = Field(
        None, description="Optional list of account IDs. If None, all accounts."
    )
    include_inactive: bool = Field(
        False, description="Include inactive planned transactions"
    )

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class AccountBalanceProjectionSchema(BaseModel):
    """Schema for individual account balance projection"""

    account_id: int
    account_name: str
    currency_code: str
    current_balance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    projected_balance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    total_planned_income: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    total_planned_expenses: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class FutureBalanceResponseSchema(BaseModel):
    """Schema for future balance calculation response"""

    target_date: datetime
    base_currency_code: str
    total_current_balance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    total_projected_balance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    total_planned_income: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    total_planned_expenses: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    income_count: int = Field(0, description="Total number of income occurrences")
    expenses_count: int = Field(0, description="Total number of expense occurrences")
    accounts: list[AccountBalanceProjectionSchema]

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class BalanceProjectionRequestSchema(BaseModel):
    """Schema for requesting balance projection over time"""

    start_date: datetime = Field(
        default_factory=datetime.now, description="Start date for projection"
    )
    end_date: datetime
    period: Literal['daily', 'weekly', 'monthly'] = Field(
        default='daily', description="Aggregation period"
    )
    account_ids: list[int] | None = Field(
        None, description="Optional list of account IDs"
    )
    include_inactive: bool = Field(
        False, description="Include inactive planned transactions"
    )

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class BalanceProjectionPointSchema(BaseModel):
    """Schema for a single point in balance projection"""

    date: datetime
    balance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    income: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    expenses: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class BalanceProjectionResponseSchema(BaseModel):
    """Schema for balance projection response"""

    start_date: datetime
    end_date: datetime
    period: str
    base_currency_code: str
    projection_points: list[BalanceProjectionPointSchema]

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )

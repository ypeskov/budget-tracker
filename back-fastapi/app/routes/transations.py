from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.models.TransactionTemplate import TransactionTemplate
from app.schemas.transaction_schema import (
    CreateTransactionSchema,
    ResponseTransactionSchema,
    ResponseTransactionTemplateSchema,
    TemplateIdsSchema,
    UpdateTransactionSchema,
)
from app.services.errors import AccessDenied, InvalidAccount, InvalidCategory
from app.services.transaction_management.errors import InvalidTransaction
from app.services.transactions import (
    create_template,
    create_transaction,
    delete,
    delete_templates,
    get_templates,
    get_transaction_details,
    get_transactions,
    update,
)
from app.utils.sanitize_transaction_filters import prepare_filters

ic.configureOutput(includeContext=True)

router = APIRouter(tags=["Transactions"], prefix="/transactions", dependencies=[Depends(check_token)])


@router.post("/", response_model=ResponseTransactionSchema | None)
def add_user_transaction(
    transaction_dto: CreateTransactionSchema,
    request: Request,
    db: Session = Depends(get_db),
):
    """Add a new transaction for a user"""

    try:
        transaction = create_transaction(transaction_dto, request.state.user["id"], db)
        if transaction_dto.is_template:
            create_template(transaction_dto, request.state.user["id"], db)
        return transaction
    except AccessDenied:
        logger.error("Access denied")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except InvalidCategory:
        logger.error(f"Invalid category: {transaction_dto}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid category")
    except InvalidAccount:
        logger.error(f"Invalid account: {transaction_dto}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid account")
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create transaction",
        )


@router.get("/", response_model=list[ResponseTransactionSchema])
def get_user_transactions(request: Request, db: Session = Depends(get_db)):
    """Get all transactions for a user"""
    params = dict(request.query_params)
    prepare_filters(params)

    try:
        transactions = get_transactions(request.state.user["id"], db, dict(params))
        return transactions
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get transactions",
        )


@router.get("/templates", response_model=list[ResponseTransactionTemplateSchema])
def get_user_templates(request: Request, db: Session = Depends(get_db)):
    """Get all templates for a user"""
    templates: list[TransactionTemplate] = get_templates(request.state.user["id"], db)

    return templates


@router.delete("/templates", response_model=list[ResponseTransactionTemplateSchema])
def delete_user_templates(
    request: Request,
    ids: str = Query(..., description="Comma-separated list of template IDs", examples=["1,2,3"]),
    db: Session = Depends(get_db),
):
    """Delete all templates for a user"""
    try:
        template_ids_schema = TemplateIdsSchema(ids=ids)
        template_ids = template_ids_schema.get_ids_list()

        delete_templates(request.state.user["id"], db, template_ids)
        updated_templates = get_templates(request.state.user["id"], db)

        return updated_templates
    except ValueError as e:
        logger.error(f"Error deleting templates: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete templates",
        )


@router.delete("/templates/validate", response_model=list[int])
def validate_template_ids(
    ids: str = Query(..., description="Comma-separated list of template IDs", examples=["1,2,3"]),
):
    """Validate template IDs format and return parsed list"""
    try:
        template_ids_schema = TemplateIdsSchema(ids=ids)
        return template_ids_schema.get_ids_list()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{transaction_id}", response_model=ResponseTransactionSchema)
def get_transaction(transaction_id: int, request: Request, db: Session = Depends(get_db)) -> ResponseTransactionSchema:
    """Get transaction details"""
    return get_transaction_details(transaction_id, request.state.user["id"], db)


@router.put("/", response_model=ResponseTransactionSchema)
def update_transaction(
    transaction_details: UpdateTransactionSchema,
    request: Request,
    db: Session = Depends(get_db),
) -> ResponseTransactionSchema:
    """Update transaction details and create a template if the transaction is a template"""
    try:
        transaction = update(transaction_details, request.state.user["id"], db)

        if transaction_details.is_template:
            create_template(transaction_details, request.state.user["id"], db)

        return transaction
    except InvalidTransaction as e:
        logger.error(f"Error updating transaction: {e.detail}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=e.detail)
    except AccessDenied:
        logger.error("Error updating transaction: Access denied")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except InvalidCategory:
        logger.error(f"Invalid category: {transaction_details}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid category")
    except HTTPException as e:
        logger.error(f"Error updating transaction: {e.detail}")
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update transaction",
        )


@router.delete("/{transaction_id}", response_model=ResponseTransactionSchema)
def delete_transaction(
    transaction_id: int, request: Request, db: Session = Depends(get_db)
) -> ResponseTransactionSchema:
    """Delete transaction"""
    try:
        transaction = delete(transaction_id, request.state.user["id"], db)
        return ResponseTransactionSchema.model_validate(transaction)
    except InvalidTransaction as e:
        logger.error(f"Error deleting transaction: {e.detail}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=e.detail)
    except AccessDenied:
        logger.error("Error deleting transaction: Access denied")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete transaction",
        )

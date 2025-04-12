from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.models.api_models import ErrorResponse, TransactionFilterParams
from app.models.up_models import TransactionResponse, TransactionsResponse
from app.services.up_api_service import UpBankApiService
from app.utils.helpers import AccountType

router = APIRouter()


@router.get(
    "/",
    response_model=TransactionsResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get all transactions",
    description="Returns all transactions with optional filtering",
)
async def get_transactions(
    account_type: AccountType = Query(..., description="Account type to query"),
    since: Optional[datetime] = Query(None, description="Filter transactions since this date"),
    until: Optional[datetime] = Query(None, description="Filter transactions until this date"),
    category: Optional[str] = Query(None, description="Filter by category ID"),
    status: Optional[str] = Query(None, description="Filter by transaction status"),
    page_size: int = Query(20, description="Number of items per page"),
    page_cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get all transactions with optional filtering."""
    return await service.get_transactions(
        account_type=account_type,
        since=since,
        until=until,
        category=category,
        status=status,
        page_size=page_size,
        page_cursor=page_cursor,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get transaction by ID",
    description="Returns a specific transaction by ID",
)
async def get_transaction(
    transaction_id: str = Path(..., description="Transaction ID"),
    account_type: AccountType = Query(..., description="Account type to query"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get a specific transaction by ID."""
    return await service.get_transaction(account_type, transaction_id)


@router.get(
    "/account/{account_id}",
    response_model=TransactionsResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get transactions for account",
    description="Returns transactions for a specific account with optional filtering",
)
async def get_account_transactions(
    account_id: str = Path(..., description="Account ID"),
    account_type: AccountType = Query(..., description="Account type to query"),
    since: Optional[datetime] = Query(None, description="Filter transactions since this date"),
    until: Optional[datetime] = Query(None, description="Filter transactions until this date"),
    category: Optional[str] = Query(None, description="Filter by category ID"),
    status: Optional[str] = Query(None, description="Filter by transaction status"),
    page_size: int = Query(20, description="Number of items per page"),
    page_cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get transactions for a specific account."""
    return await service.get_account_transactions(
        account_type=account_type,
        account_id=account_id,
        since=since,
        until=until,
        category=category,
        status=status,
        page_size=page_size,
        page_cursor=page_cursor,
    ) 
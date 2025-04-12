from typing import Any

from fastapi import APIRouter, Depends, Path, Query

from app.models.api_models import AccountFilterParams, ErrorResponse
from app.models.up_models import AccountResponse, AccountsResponse
from app.services.up_api_service import UpBankApiService
from app.utils.helpers import AccountType

router = APIRouter()


@router.get(
    "/",
    response_model=AccountsResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get all accounts",
    description="Returns all accounts for the specified account type",
)
async def get_accounts(
    account_type: AccountType = Query(..., description="Account type to query"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get all accounts for the specified account type."""
    return await service.get_accounts(account_type)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get account by ID",
    description="Returns a specific account by ID",
)
async def get_account(
    account_id: str = Path(..., description="Account ID"),
    account_type: AccountType = Query(..., description="Account type to query"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get a specific account by ID."""
    return await service.get_account(account_type, account_id) 
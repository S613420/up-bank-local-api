from typing import Any, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.models.api_models import CategoryParams, ErrorResponse
from app.models.up_models import CategoriesResponse, CategoryResponse
from app.services.up_api_service import UpBankApiService
from app.utils.helpers import AccountType

router = APIRouter()


@router.get(
    "/",
    response_model=CategoriesResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get all categories",
    description="Returns all categories with optional parent filter",
)
async def get_categories(
    account_type: AccountType = Query(..., description="Account type to query"),
    parent: Optional[str] = Query(None, description="Filter by parent category ID"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get all categories with optional parent filter."""
    return await service.get_categories(account_type, parent)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get category by ID",
    description="Returns a specific category by ID",
)
async def get_category(
    category_id: str = Path(..., description="Category ID"),
    account_type: AccountType = Query(..., description="Account type to query"),
    service: UpBankApiService = Depends(lambda: UpBankApiService()),
) -> Any:
    """Get a specific category by ID."""
    return await service.get_category(account_type, category_id) 
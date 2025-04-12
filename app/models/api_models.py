from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.utils.helpers import AccountType


class ErrorResponse(BaseModel):
    detail: str


class PaginationParams(BaseModel):
    page_size: Optional[int] = Field(20, description="Number of items per page")
    page: Optional[int] = Field(1, description="Page number")


class TransactionFilterParams(PaginationParams):
    account_type: AccountType = Field(..., description="Account type to query")
    since: Optional[datetime] = Field(None, description="Filter transactions since this date")
    until: Optional[datetime] = Field(None, description="Filter transactions until this date")
    category: Optional[str] = Field(None, description="Filter by category ID")
    status: Optional[str] = Field(None, description="Filter by transaction status")
    tag: Optional[str] = Field(None, description="Filter by tag ID")


class AccountFilterParams(BaseModel):
    account_type: AccountType = Field(..., description="Account type to query")


class TagsParams(BaseModel):
    account_type: AccountType = Field(..., description="Account type to query")


class CategoryParams(BaseModel):
    account_type: AccountType = Field(..., description="Account type to query")
    parent: Optional[str] = Field(None, description="Filter by parent category ID") 
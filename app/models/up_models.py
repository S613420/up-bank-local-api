from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AccountOwnershipType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    JOINT = "JOINT"


class AccountType(str, Enum):
    SAVER = "SAVER"
    TRANSACTIONAL = "TRANSACTIONAL"


class AccountAttributes(BaseModel):
    display_name: str = Field(..., alias="displayName")
    account_type: AccountType = Field(..., alias="accountType")
    ownership_type: AccountOwnershipType = Field(..., alias="ownershipType")
    balance: Dict[str, Any]
    created_at: datetime = Field(..., alias="createdAt")


class AccountRelationships(BaseModel):
    transactions: Dict[str, Any]


class Account(BaseModel):
    type: str
    id: str
    attributes: AccountAttributes
    relationships: AccountRelationships


class AccountResponse(BaseModel):
    data: Account


class AccountsResponse(BaseModel):
    data: List[Account]


class TransactionStatus(str, Enum):
    HELD = "HELD"
    SETTLED = "SETTLED"


class HoldInfo(BaseModel):
    amount: Dict[str, Any]
    foreign_amount: Optional[Dict[str, Any]] = Field(None, alias="foreignAmount")


class TransactionAttributes(BaseModel):
    status: TransactionStatus
    raw_text: Optional[str] = Field(None, alias="rawText")
    description: str
    message: Optional[str] = None
    hold_info: Optional[HoldInfo] = Field(None, alias="holdInfo")
    round_up: Optional[Dict[str, Any]] = Field(None, alias="roundUp")
    cashback: Optional[Dict[str, Any]] = None
    amount: Dict[str, Any]
    foreign_amount: Optional[Dict[str, Any]] = Field(None, alias="foreignAmount")
    created_at: datetime = Field(..., alias="createdAt")
    settled_at: Optional[datetime] = Field(None, alias="settledAt")


class TransactionRelationships(BaseModel):
    account: Dict[str, Any]
    category: Optional[Dict[str, Any]] = None
    parent_category: Optional[Dict[str, Any]] = Field(None, alias="parentCategory")
    tags: Optional[Dict[str, Any]] = None


class Transaction(BaseModel):
    type: str
    id: str
    attributes: TransactionAttributes
    relationships: TransactionRelationships


class TransactionResponse(BaseModel):
    data: Transaction


class TransactionsResponse(BaseModel):
    data: List[Transaction]
    links: Optional[Dict[str, Any]] = None


class CategoryAttributes(BaseModel):
    name: str


class CategoryRelationships(BaseModel):
    parent: Optional[Dict[str, Any]] = None
    children: Optional[Dict[str, Any]] = None


class Category(BaseModel):
    type: str
    id: str
    attributes: CategoryAttributes
    relationships: CategoryRelationships


class CategoryResponse(BaseModel):
    data: Category


class CategoriesResponse(BaseModel):
    data: List[Category] 
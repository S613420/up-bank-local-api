import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.models.up_models import (
    AccountResponse,
    AccountsResponse,
    CategoriesResponse,
    CategoryResponse,
    TransactionResponse,
    TransactionsResponse,
)
from app.utils.helpers import AccountType, format_headers, get_token_for_account

logger = logging.getLogger("up_bank_api")


class UpBankApiService:
    """Service for interacting with the Up Bank API."""

    def __init__(self):
        self.base_url = settings.up_api_base_url

    async def _make_request(
        self,
        account_type: AccountType,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Up Bank API.
        
        Args:
            account_type: The account type to use for authentication
            endpoint: The API endpoint to call
            method: HTTP method to use
            params: Query parameters
            data: Request body data
            
        Returns:
            The JSON response from the API
            
        Raises:
            HTTPException: If the API request fails
        """
        token = get_token_for_account(account_type)
        headers = format_headers(token)
        url = f"{self.base_url}/{endpoint}"
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=30.0,
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            status_code = e.response.status_code
            
            try:
                error_body = e.response.json()
                if "errors" in error_body and len(error_body["errors"]) > 0:
                    error_detail = error_body["errors"][0].get("detail", str(e))
            except Exception:
                error_detail = str(e)
                
            logger.error(f"HTTP error: {status_code} - {error_detail}")
            raise HTTPException(status_code=status_code, detail=error_detail)
            
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error communicating with Up Bank API: {str(e)}")
    
    async def get_accounts(self, account_type: AccountType) -> AccountsResponse:
        """Get all accounts for the specified account type."""
        response = await self._make_request(account_type, "accounts")
        return AccountsResponse.model_validate(response)
    
    async def get_account(self, account_type: AccountType, account_id: str) -> AccountResponse:
        """Get a specific account by ID."""
        response = await self._make_request(account_type, f"accounts/{account_id}")
        return AccountResponse.model_validate(response)
    
    async def get_transactions(
        self,
        account_type: AccountType,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        page_size: int = 20,
        page_cursor: Optional[str] = None,
    ) -> TransactionsResponse:
        """Get transactions with optional filters."""
        params = {"page[size]": page_size}
        
        if page_cursor:
            params["page[after]"] = page_cursor
        if since:
            params["filter[since]"] = since.isoformat()
        if until:
            params["filter[until]"] = until.isoformat()
        if category:
            params["filter[category]"] = category
        if status:
            params["filter[status]"] = status
            
        response = await self._make_request(account_type, "transactions", params=params)
        return TransactionsResponse.model_validate(response)
    
    async def get_transaction(self, account_type: AccountType, transaction_id: str) -> TransactionResponse:
        """Get a specific transaction by ID."""
        response = await self._make_request(account_type, f"transactions/{transaction_id}")
        return TransactionResponse.model_validate(response)
    
    async def get_account_transactions(
        self,
        account_type: AccountType,
        account_id: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        page_size: int = 20,
        page_cursor: Optional[str] = None,
    ) -> TransactionsResponse:
        """Get transactions for a specific account."""
        params = {"page[size]": page_size}
        
        if page_cursor:
            params["page[after]"] = page_cursor
        if since:
            params["filter[since]"] = since.isoformat()
        if until:
            params["filter[until]"] = until.isoformat()
        if category:
            params["filter[category]"] = category
        if status:
            params["filter[status]"] = status
            
        response = await self._make_request(account_type, f"accounts/{account_id}/transactions", params=params)
        return TransactionsResponse.model_validate(response)
    
    async def get_categories(self, account_type: AccountType, parent: Optional[str] = None) -> CategoriesResponse:
        """Get categories with optional parent filter."""
        params = {}
        if parent:
            params["filter[parent]"] = parent
            
        response = await self._make_request(account_type, "categories", params=params)
        return CategoriesResponse.model_validate(response)
    
    async def get_category(self, account_type: AccountType, category_id: str) -> CategoryResponse:
        """Get a specific category by ID."""
        response = await self._make_request(account_type, f"categories/{category_id}")
        return CategoryResponse.model_validate(response) 
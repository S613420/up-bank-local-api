import logging
from enum import Enum
from typing import Any, Dict, Optional

from app.core.config import settings

# Configure logging
logger = logging.getLogger("up_bank_api")


class AccountType(str, Enum):
    """Enum for types of accounts to query."""
    USER1 = "user1"
    USER2 = "user2"
    SHARED = "shared"


def get_token_for_account(account_type: AccountType) -> str:
    """
    Get the appropriate API token based on the account type.
    
    Args:
        account_type: The type of account to get the token for
        
    Returns:
        The API token for the specified account
        
    Raises:
        ValueError: If the requested token is not available
    """
    token_map = {
        AccountType.USER1: settings.user1_up_token,
        AccountType.USER2: settings.user2_up_token,
        AccountType.SHARED: settings.shared_up_token,
    }
    
    token = token_map.get(account_type)
    if token is None:
        if account_type == AccountType.USER1 or account_type == AccountType.USER2:
            raise ValueError(
                f"API token for account type '{account_type}' is not configured. "
                f"Please add {account_type.upper()}_UP_TOKEN to your .env file."
            )
        else:
            raise ValueError(
                f"API token for account type '{account_type}' is not configured. "
                f"If you want to use a shared account, please add SHARED_UP_TOKEN to your .env file."
            )
    
    return token


def format_headers(token: str) -> Dict[str, str]:
    """
    Format headers for Up Bank API requests.
    
    Args:
        token: The Up Bank API token
        
    Returns:
        Dict with properly formatted headers
    """
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    } 
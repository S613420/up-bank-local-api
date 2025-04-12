from fastapi import APIRouter

from app.api.routes import accounts, categories, transactions

# Create main router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"]) 
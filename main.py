import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("up_bank_api")


def check_env_variables():
    """Check if necessary environment variables are set."""
    missing_vars = []
    
    if not settings.user1_up_token:
        missing_vars.append("USER1_UP_TOKEN")
    
    if not settings.user2_up_token:
        missing_vars.append("USER2_UP_TOKEN")
    
    if missing_vars:
        logger.warning(
            f"Missing environment variables: {', '.join(missing_vars)}. "
            f"Please add them to your .env file."
        )
        
        # Check if .env file exists
        if not os.path.exists(".env"):
            logger.warning(
                ".env file not found! "
                "Please create a .env file based on .env.example."
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    """
    # Startup logic
    logger.info("Starting Up Bank Local API...")
    check_env_variables()
    yield
    # Shutdown logic
    logger.info("Shutting down Up Bank Local API...")


def create_application() -> FastAPI:
    """
    Create the FastAPI application with settings and routes.
    """
    application = FastAPI(
        title="Up Bank Local API",
        description="A local API wrapper for the Up Bank REST API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Set up CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    application.include_router(api_router, prefix="/api/v1")

    return application


app = create_application()


@app.get("/")
async def root():
    """Root endpoint that provides basic API info."""
    
    # Check token status
    token_status = {
        "user1": "configured" if settings.user1_up_token else "missing",
        "user2": "configured" if settings.user2_up_token else "missing",
        "shared": "configured" if settings.shared_up_token else "not configured (optional)",
    }
    
    return {
        "name": "Up Bank Local API",
        "version": "0.1.0",
        "status": "running",
        "documentation": "/docs",
        "tokens_status": token_status,
    }


def main():
    """Entry point for the application."""
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    main()

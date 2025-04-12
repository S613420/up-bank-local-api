from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Up Bank API configuration
    up_api_base_url: str = "https://api.up.com.au/api/v1"
    user1_up_token: str | None = Field(None, description="User 1 Up Bank API token")
    user2_up_token: str | None = Field(None, description="User 2 Up Bank API token")
    shared_up_token: str | None = Field(None, description="Shared Up Bank account API token")
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    
    # Configure environment variables loading
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Create a global settings instance
settings = Settings() 
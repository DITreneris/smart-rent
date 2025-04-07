"""
SmartRent application settings.
"""
from typing import List, Union, Optional
import os
from pydantic import BaseSettings, AnyHttpUrl, validator

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development, staging, production
    LOG_LEVEL: str = "INFO"
    
    # JWT Authentication
    SECRET_KEY: str = "your_jwt_secret_key_here"
    REFRESH_TOKEN_SECRET_KEY: str = "your_refresh_token_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "smartrent"
    
    # Blockchain Configuration
    ETHEREUM_RPC_URL: str = "https://goerli.infura.io/v3/your_infura_key_here"
    ETHEREUM_CHAIN_ID: int = 5  # Goerli testnet
    
    # Transaction Monitoring
    TX_POLLING_INTERVAL: int = 5  # seconds
    TX_MAX_ATTEMPTS: int = 60  # 5 minutes at 5-second intervals
    
    # CORS Settings
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @validator("CORS_ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string to list if needed."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Security Settings
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Email Settings (Optional)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    # Feature Flags
    ENABLE_WALLET_AUTH: bool = True
    ENABLE_GOOGLE_AUTH: bool = False
    ENABLE_DOCUMENT_STORAGE: bool = True
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Override settings with environment variables
if os.getenv("SECRET_KEY"):
    settings.SECRET_KEY = os.getenv("SECRET_KEY")

if os.getenv("REFRESH_TOKEN_SECRET_KEY"):
    settings.REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY") 
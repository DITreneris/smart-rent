import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SmartRent"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CSRF_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            try:
                v = eval(v)  # Safely evaluate string representation of list
            except:
                return [i.strip() for i in v.split(",")]
        return v

    # Database Configuration (SQL - legacy)
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    
    # MongoDB Configuration (for off-chain storage)
    MONGO_CONNECTION_STRING: str = "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = "smartrent"
    MONGO_TEST_DB_NAME: str = "smartrent_test"
    MONGO_GRIDFS_BUCKET: str = "uploads"
    
    # Web3 Configuration
    WEB3_PROVIDER_URL: str
    CONTRACT_ADDRESS: str
    CHAIN_ID: int = 11155111  # Sepolia Testnet
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Admin User
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    ADMIN_FULL_NAME: str
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Storage Configuration
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"]
    STORE_DOCUMENTS_IN_DB: bool = True  # Whether to store document files in MongoDB

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 
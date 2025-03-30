from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "SmartRent"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/smartrent")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Blockchain
    WEB3_PROVIDER_URI: str = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")

settings = Settings() 
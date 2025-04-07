"""
SmartRent application settings.
"""
from typing import Optional
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "smartrent_dev")
    
    # Web3 Provider
    WEB3_PROVIDER_URI: str = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", "1"))
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Smart Contract
    SMARTRENT_CONTRACT_ADDRESS: str = os.getenv(
        "SMARTRENT_CONTRACT_ADDRESS", 
        "0x0000000000000000000000000000000000000000"
    )
    
    # Transaction Monitoring
    TX_POLLING_INTERVAL: int = int(os.getenv("TX_POLLING_INTERVAL", "5"))  # seconds
    TX_MAX_ATTEMPTS: int = int(os.getenv("TX_MAX_ATTEMPTS", "60"))  # 5 minutes at 5s interval
    
    # Hyperledger Fabric
    HYPERLEDGER_HOST: str = os.getenv("HYPERLEDGER_HOST", "localhost:7051")
    HYPERLEDGER_CHANNEL: str = os.getenv("HYPERLEDGER_CHANNEL", "mychannel")
    HYPERLEDGER_CHAINCODE: str = os.getenv("HYPERLEDGER_CHAINCODE", "smartrent")
    
    # Cryptocurrency Networks
    CRYPTO_API_KEY: str = os.getenv("CRYPTO_API_KEY", "")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings() 
"""
App models.

Note: These models are kept as SQLAlchemy models for reference and 
potential hybrid SQL/MongoDB usage. However, the primary storage 
is now MongoDB for schema flexibility and document-oriented data.
"""

from app.models.user import User, UserRole
from app.models.property import (
    PropertyType,
    PropertyStatus,
    PropertyImage,
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
    PropertySearchParams,
)
from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.models.proposal import Proposal, ProposalStatus
from app.models.contract_asset import ContractAsset, ContractStatus
from app.models.property_photo import PropertyPhoto
from app.models.rental_info import RentalInfo, RentalStatus
from app.models.payment import Payment, PaymentStatus
from app.models.document import Document, DocumentType
from app.models.auth import (
    TokenResponse,
    LoginRequest,
    WalletLoginRequest,
    RefreshTokenRequest,
    UserRegistrationRequest,
    WalletRegistrationRequest,
    WalletNonceResponse,
    UserResponse
)

__all__ = [
    'User',
    'UserRole',
    'PropertyType',
    'PropertyStatus',
    'PropertyImage',
    'PropertyCreate',
    'PropertyResponse',
    'PropertyUpdate',
    'PropertySearchParams',
    'Transaction',
    'TransactionStatus',
    'TransactionType',
    'Proposal',
    'ProposalStatus',
    'ContractAsset',
    'ContractStatus',
    'PropertyPhoto',
    'RentalInfo',
    'RentalStatus',
    'Payment',
    'PaymentStatus',
    'Document',
    'DocumentType',
    "TokenResponse",
    "LoginRequest",
    "WalletLoginRequest",
    "RefreshTokenRequest",
    "UserRegistrationRequest",
    "WalletRegistrationRequest",
    "WalletNonceResponse",
    "UserResponse"
] 
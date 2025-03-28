from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ContractStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContractBase(BaseModel):
    property_id: int
    start_date: datetime
    end_date: datetime
    monthly_rent: int
    security_deposit: int


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    monthly_rent: Optional[int] = None
    security_deposit: Optional[int] = None
    status: Optional[ContractStatus] = None
    contract_address: Optional[str] = None


class ContractResponse(ContractBase):
    id: int
    tenant_id: int
    landlord_id: int
    status: ContractStatus
    contract_address: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 
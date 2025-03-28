from pydantic import BaseModel
from typing import Dict, Any


class UserApproval(BaseModel):
    approved: bool
    notes: str = None


class PropertyApproval(BaseModel):
    approved: bool
    notes: str = None


class PendingCount(BaseModel):
    users: int
    properties: int


class DashboardStats(BaseModel):
    tenant_count: int
    landlord_count: int
    pending_approvals: PendingCount
    property_stats: Dict[str, int]
    contract_stats: Dict[str, int] 
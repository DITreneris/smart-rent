"""
Verification service and result models.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VerificationResult:
    """Result of a cross-network transaction verification."""
    
    success: bool
    timestamp: datetime = None
    network_confirmations: int = 0
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        
        if self.details is None:
            self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "timestamp": self.timestamp.isoformat(),
            "network_confirmations": self.network_confirmations,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VerificationResult':
        """Create from dictionary."""
        timestamp = None
        if "timestamp" in data:
            try:
                timestamp = datetime.fromisoformat(data["timestamp"])
            except (ValueError, TypeError):
                timestamp = datetime.utcnow()
        
        return cls(
            success=data.get("success", False),
            timestamp=timestamp,
            network_confirmations=data.get("network_confirmations", 0),
            details=data.get("details", {})
        ) 
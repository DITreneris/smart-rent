"""
Transactions Router

API endpoints for transaction management, history, and receipts.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime
import uuid

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.transaction import Transaction as DBTransaction, TransactionStatus, TransactionType
from app.middlewares.csrf import csrf_protect

router = APIRouter()


class TransactionBase(BaseModel):
    hash: Optional[str] = None
    status: TransactionStatus
    description: str
    type: TransactionType
    amount: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    confirmations: Optional[int] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None
    

class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: UUID4
    user_id: Optional[UUID4] = None
    property_id: Optional[UUID4] = None
    timestamp: datetime
    receipt_url: Optional[str] = None
    
    class Config:
        orm_mode = True


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(csrf_protect())])
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transaction record
    """
    # Create new transaction in database
    db_transaction = DBTransaction(
        id=uuid.uuid4(),
        user_id=current_user.id,
        hash=transaction.hash,
        status=transaction.status,
        description=transaction.description,
        type=transaction.type,
        amount=transaction.amount,
        from_address=transaction.from_address or current_user.wallet_address,
        to_address=transaction.to_address,
        confirmations=transaction.confirmations,
        error=transaction.error,
        metadata=transaction.metadata or {},
        timestamp=datetime.utcnow()
    )
    
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    
    return db_transaction


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    status: Optional[TransactionStatus] = None,
    transaction_type: Optional[TransactionType] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's transaction history with optional filters
    """
    # Build query
    query = select(DBTransaction).where(DBTransaction.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(DBTransaction.status == status)
    if transaction_type:
        query = query.filter(DBTransaction.type == transaction_type)
        
    # Apply pagination
    query = query.order_by(DBTransaction.timestamp.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    return transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID4,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific transaction by ID
    """
    query = select(DBTransaction).where(
        DBTransaction.id == transaction_id,
        DBTransaction.user_id == current_user.id
    )
    result = await db.execute(query)
    transaction = result.scalars().first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
        
    return transaction


@router.get("/transactions/{transaction_id}/receipt", response_class=FileResponse)
async def get_transaction_receipt(
    transaction_id: UUID4,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get receipt for a completed transaction
    """
    query = select(DBTransaction).where(
        DBTransaction.id == transaction_id,
        DBTransaction.user_id == current_user.id
    )
    result = await db.execute(query)
    transaction = result.scalars().first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
        
    if transaction.status != TransactionStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receipts are only available for completed transactions"
        )
        
    if not transaction.receipt_url:
        # Generate receipt if not already generated
        # This would call a service to generate the receipt
        receipt_url = f"/receipts/{transaction.hash}.pdf"
        transaction.receipt_url = receipt_url
        db.add(transaction)
        await db.commit()
    
    # In a real implementation, this would return the actual PDF file
    # For now, we'll just return a placeholder response
    return {
        "receipt_url": transaction.receipt_url,
        "transaction_id": str(transaction.id),
        "transaction_hash": transaction.hash
    }


@router.put("/transactions/{transaction_id}/status", response_model=TransactionResponse, dependencies=[Depends(csrf_protect())])
async def update_transaction_status(
    transaction_id: UUID4,
    status: TransactionStatus,
    confirmations: Optional[int] = None,
    error: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the status of a transaction
    """
    query = select(DBTransaction).where(
        DBTransaction.id == transaction_id,
        DBTransaction.user_id == current_user.id
    )
    result = await db.execute(query)
    transaction = result.scalars().first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
        
    # Update transaction status
    transaction.status = status
    
    # Update confirmations if provided
    if confirmations is not None:
        transaction.confirmations = confirmations
        
    # Update error if provided
    if error is not None:
        transaction.error = error
        
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    
    return transaction 
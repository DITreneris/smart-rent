from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
import json

from app.api.deps import get_current_active_user, get_current_active_landlord, get_db
from app.models.property import Property
from app.models.user import User
from app.schemas.property import Property as PropertySchema, PropertyCreate, PropertyUpdate

router = APIRouter()

@router.get 
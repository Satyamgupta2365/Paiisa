from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from database.db import get_db
from models.schemas import TransactionOut, SpendingInsights
from services.transaction_service import transaction_service

router = APIRouter(prefix="/api/v1/users/{user_id}", tags=["transactions"])

@router.get("/transactions", response_model=List[TransactionOut])
async def get_user_transactions(user_id: uuid.UUID, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await transaction_service.list_for_user(db, user_id, limit)

@router.get("/insights", response_model=SpendingInsights)
async def get_user_insights(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await transaction_service.insights(db, user_id)

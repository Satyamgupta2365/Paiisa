from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.schemas import RecommendRequest, RecommendResponse
from services.offer_service import offer_service
from services.gemini_service import gemini_service

router = APIRouter(prefix="/api/v1", tags=["recommend"])

@router.post("/recommend-payment", response_model=RecommendResponse)
async def recommend_payment(req: RecommendRequest, db: AsyncSession = Depends(get_db)):
    options = await offer_service.get_payment_options(db, req.amount, req.category)
    if not options:
        raise HTTPException(status_code=422, detail="No active offers found.")
    
    # Primary: Gemini AI recommendation
    return await gemini_service.recommend(req.amount, req.category, options)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid

from database.db import get_db
from models.schemas import OfferCreate, OfferOut
from database.models import Offer

router = APIRouter(prefix="/api/v1/offers", tags=["offers"])

@router.get("", response_model=List[OfferOut])
async def get_offers(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Offer).where(Offer.is_active == True))
    return res.scalars().all()

@router.post("", response_model=OfferOut, status_code=201)
async def create_offer(req: OfferCreate, db: AsyncSession = Depends(get_db)):
    offer = Offer(**req.dict())
    db.add(offer)
    await db.flush()
    await db.commit()
    return offer

@router.delete("/{offer_id}", status_code=204)
async def delete_offer(offer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = res.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer.is_active = False
    await db.flush()
    await db.commit()

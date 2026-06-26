from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from database.db import get_db
from models.schemas import UserCreate, UserOut
from database.models import User

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("", response_model=UserOut, status_code=201)
async def create_user(req: UserCreate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == req.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")
        
    user = User(**req.dict())
    db.add(user)
    await db.flush()
    await db.commit()
    return user

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

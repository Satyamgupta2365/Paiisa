import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from database.models import User, Transaction, PaymentMethod
from datetime import datetime

async def seed():
    engine = create_async_engine(settings.DATABASE_URL.replace("postgresql+asyncpg", "sqlite+aiosqlite"))
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    satyam_id = uuid.UUID('23050620-0500-0000-0000-000000000000')
    
    async with async_session() as db:
        user = await db.get(User, satyam_id)
        if not user:
            print("Creating Satyam Account with ID 2305062005 mapping...")
            user = User(
                id=satyam_id,
                name="Satyam",
                email="satyam@example.com",
                phone="2305062005",
                preferred_payment_method=PaymentMethod.UPI
            )
            db.add(user)
            await db.commit()
            print("Satyam created.")
        else:
            print("Satyam already exists.")

if __name__ == "__main__":
    asyncio.run(seed())

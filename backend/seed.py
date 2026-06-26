import asyncio
import uuid
from datetime import datetime, timedelta
from database.db import engine, Base, AsyncSessionLocal
from database.models import User, Offer, PaymentMethod

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        demo_user_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
        demo_user = User(
            id=demo_user_id,
            name="Demo User",
            email="demo@spendpilot.com"
        )
        db.add(demo_user)

        now = datetime.utcnow()
        offers = [
            Offer(payment_method=PaymentMethod.UPI, cashback_percentage=3.0, max_cashback=150, min_amount=0, valid_until=now + timedelta(days=90)),
            Offer(payment_method=PaymentMethod.UPI, cashback_percentage=5.0, max_cashback=200, min_amount=500, category="food", valid_until=now + timedelta(days=60)),
            Offer(payment_method=PaymentMethod.CREDIT_CARD, cashback_percentage=10.0, max_cashback=1000, min_amount=2000, category="electronics", valid_until=now + timedelta(days=30)),
            Offer(payment_method=PaymentMethod.CREDIT_CARD, cashback_percentage=5.0, max_cashback=500, min_amount=1000, valid_until=now + timedelta(days=60)),
            Offer(payment_method=PaymentMethod.DEBIT_CARD, cashback_percentage=2.0, max_cashback=100, min_amount=0, valid_until=now + timedelta(days=90)),
            Offer(payment_method=PaymentMethod.WALLET, cashback_percentage=5.0, max_cashback=250, min_amount=200, valid_until=now + timedelta(days=45)),
            Offer(payment_method=PaymentMethod.WALLET, cashback_percentage=8.0, max_cashback=300, min_amount=300, category="travel", valid_until=now + timedelta(days=30)),
            Offer(payment_method=PaymentMethod.NET_BANKING, cashback_percentage=1.5, max_cashback=75, min_amount=1000, valid_until=now + timedelta(days=90)),
        ]
        db.add_all(offers)
        
        try:
            await db.commit()
            print(f"Seed complete. Demo user: ID={demo_user_id}, Email=demo@spendpilot.com")
        except Exception as e:
            await db.rollback()
            print(f"Seed failed (perhaps already seeded?): {e}")

if __name__ == "__main__":
    asyncio.run(seed())

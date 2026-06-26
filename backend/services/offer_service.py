from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from database.models import Offer, PaymentMethod
from models.schemas import PaymentOption

class OfferService:
    async def get_payment_options(self, db: AsyncSession, amount: float, category: str) -> List[PaymentOption]:
        result = await db.execute(select(Offer).where(Offer.is_active == True))
        active_offers = result.scalars().all()

        options = []
        best_savings = 0.0

        for method in PaymentMethod:
            matches = [off for off in active_offers if off.payment_method == method and off.applies_to(amount, category)]
            if matches:
                best_offer = max(matches, key=lambda o: o.cashback_percentage)
                savings = best_offer.calculate_cashback(amount)
                cashback = best_offer.cashback_percentage
            else:
                savings = 0.0
                cashback = 0.0
                
            best_savings = max(best_savings, savings)
            
            options.append({
                "method": method,
                "cashback": cashback,
                "savings": savings,
                "score": 0.0
            })

        for opt in options:
            if best_savings > 0:
                opt["score"] = opt["savings"] / best_savings
                
        # clamp to [0,1]
        for opt in options:
            opt["score"] = max(0.0, min(1.0, opt["score"]))

        options.sort(key=lambda x: x["score"], reverse=True)
        return [PaymentOption(**opt) for opt in options]

offer_service = OfferService()

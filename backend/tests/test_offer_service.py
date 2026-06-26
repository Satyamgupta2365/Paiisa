import pytest
from services.offer_service import offer_service
from database.models import PaymentMethod, Offer
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_get_payment_options(db_session, sample_offers):
    db_session.add_all(sample_offers)
    await db_session.commit()
    
    options = await offer_service.get_payment_options(db_session, 1000, "electronics")
    
    assert len(options) == len(PaymentMethod)
    
    # Credit Card should be highest for 1000 electronics
    best_opt = options[0]
    assert best_opt.method == PaymentMethod.CREDIT_CARD
    assert best_opt.savings == 100.0  # 10% of 1000

@pytest.mark.asyncio
async def test_offer_filters():
    now = datetime.utcnow()
    # Expired offer
    off1 = Offer(payment_method=PaymentMethod.UPI, cashback_percentage=10, valid_until=now - timedelta(days=1))
    # Min amount not met
    off2 = Offer(payment_method=PaymentMethod.CREDIT_CARD, cashback_percentage=10, min_amount=5000)
    
    assert not off1.applies_to(1000, "food")
    assert not off2.applies_to(1000, "food")
    
    off3 = Offer(payment_method=PaymentMethod.WALLET, cashback_percentage=50, max_cashback=100)
    assert off3.calculate_cashback(5000) == 100.0 # Capped at 100

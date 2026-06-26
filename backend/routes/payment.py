from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.schemas import PaymentRequest, PaymentResponse
from services.offer_service import offer_service
from services.payment_service import pine_labs_service
from services.transaction_service import transaction_service
from database.models import TransactionStatus

router = APIRouter(prefix="/api/v1", tags=["payment"])

@router.post("/process-payment", response_model=PaymentResponse)
async def process_payment(req: PaymentRequest, db: AsyncSession = Depends(get_db)):
    options = await offer_service.get_payment_options(db, req.amount, req.category)
    selected_option = next((opt for opt in options if opt.method == req.payment_method), None)
    
    cashback_earned = selected_option.savings if selected_option else 0.0

    try:
        gateway_res = await pine_labs_service.initiate_payment(req.amount, req.payment_method, req.user_id)
        gateway_status = gateway_res.get("status", "FAILED")
        pine_txn_id = gateway_res.get("txnId")
        
        status = TransactionStatus.SUCCESS if gateway_status == "SUCCESS" else TransactionStatus.FAILED
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pine Labs Error: {str(e)}")

    if status != TransactionStatus.SUCCESS:
        cashback_earned = 0.0

    txn = await transaction_service.create(
        db, 
        user_id=req.user_id, 
        amount=req.amount, 
        category=req.category, 
        payment_method=req.payment_method, 
        cashback_earned=cashback_earned, 
        pine_txn_id=pine_txn_id, 
        status=status
    )
    
    await db.commit()
    
    return PaymentResponse(
        status=status,
        transaction_id=str(txn.id),
        cashback_earned=cashback_earned,
        message="Payment successful" if status == TransactionStatus.SUCCESS else "Payment failed"
    )

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database.db import get_db
from models.schemas import (
    TapRuleUpdate, TapRuleOut,
    TapPaymentRequest, TapPaymentResponse,
    TapLogOut
)
from services.tap_service import tap_service
from typing import List

router = APIRouter(prefix="/api/v1/tap", tags=["tap"])


@router.get("/rules/{user_id}", response_model=TapRuleOut)
async def get_tap_rules(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a user's financial constitution (spending rules for AI agents)."""
    return await tap_service.get_rules(user_id, db)


@router.put("/rules/{user_id}", response_model=TapRuleOut)
async def update_tap_rules(user_id: UUID, data: TapRuleUpdate, db: AsyncSession = Depends(get_db)):
    """Update a user's financial constitution."""
    return await tap_service.update_rules(user_id, data, db)


@router.post("/request", response_model=TapPaymentResponse)
async def tap_payment_request(req: TapPaymentRequest, db: AsyncSession = Depends(get_db)):
    """
    Pillar 5 — Trusted Agent Protocol (TAP)
    External AI agents (Claude, Gemini, GPT-4) submit spending requests here.
    PAISA evaluates the request against the user's financial constitution and
    returns an APPROVED or REJECTED decision with a logged audit trail.
    MCP-compatible response format.
    """
    return await tap_service.evaluate_request(req, db)


@router.get("/logs/{user_id}", response_model=List[TapLogOut])
async def get_tap_logs(user_id: UUID, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """Get the immutable audit trail of all AI agent spending requests."""
    logs = await tap_service.get_logs(user_id, db, limit=limit)
    return [
        TapLogOut(
            id=log.id,
            agent_id=log.agent_id,
            requested_amount=log.requested_amount,
            category=log.category,
            merchant_id=log.merchant_id,
            decision=log.decision,
            reason=log.reason,
            created_at=log.created_at
        )
        for log in logs
    ]

"""
Travel Guardian Routes — All 5 Pillars
Primary: Google Gemini 2.0 Flash | Fallback: Groq llama-3.3-70b-versatile
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.schemas import (
    TravelScanRequest, TravelScanResponseV2, TravelFixRequest,
    SalaryAffordabilityRequest, SalaryAffordabilityResponse,
    TripBudgetRequest, TripBudgetResponse,
    VirtualCardRequest, VirtualCardResponse,
)
from services.travel_service import travel_service
from services.gemini_service import gemini_service
from services.groq_travel_service import (
    analyze_salary_affordability as groq_affordability,
    plan_trip_budget as groq_budget,
    generate_virtual_card,
    get_ai_travel_tips as groq_tips,
)

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])


# ── Gemini-first helpers ──────────────────────────────────────────────────────

async def _get_travel_tips(destination: str, issues: list) -> list:
    """Try Gemini first, fall back to Groq for travel tips."""
    if gemini_service.is_available:
        tips = await gemini_service.get_travel_tips(destination, [i.dict() if hasattr(i, 'dict') else i for i in issues])
        if tips and len(tips) >= 2:
            return tips
    return groq_tips(destination, [i.dict() if hasattr(i, 'dict') else i for i in issues])


async def _analyze_affordability(salary_text: str, destination: str, trip_cost: float) -> dict:
    """Try Gemini first, fall back to Groq for affordability analysis."""
    if gemini_service.is_available:
        result = await gemini_service.analyze_salary_affordability(salary_text, destination, trip_cost)
        if result and "net_salary" in result:
            return result
    return groq_affordability(salary_text=salary_text, destination=destination, trip_cost=trip_cost)


async def _plan_budget(destination: str, duration_days: int, trip_budget: float) -> dict:
    """Try Gemini first, fall back to Groq for budget planning."""
    if gemini_service.is_available:
        result = await gemini_service.plan_trip_budget(destination, duration_days, trip_budget)
        if result and "breakdown" in result:
            return result
    return groq_budget(destination=destination, duration_days=duration_days, trip_budget=trip_budget)


# ── 1. Pre-departure Scan (enhanced with AI tips) ──────────────────────────────

@router.post("/scan", response_model=TravelScanResponseV2)
async def scan_travel(req: TravelScanRequest):
    """
    48-hour pre-departure financial health scan.
    Checks card status, forex, credit limit, insurance.
    Returns issues + AI-generated personalised tips via Gemini / Groq.
    """
    base = travel_service.scan(
        destination=req.destination or "Tokyo, Japan",
        user_id=req.user_id
    )
    ai_tips = await _get_travel_tips(req.destination or "Tokyo, Japan", base.issues)

    return TravelScanResponseV2(
        destination=base.destination,
        hours_to_departure=base.hours_to_departure,
        issues=base.issues,
        risk_score=base.risk_score,
        all_clear=base.all_clear,
        ai_tips=ai_tips,
    )


# ── 2. One-tap Fix All ────────────────────────────────────────────────────────

@router.post("/fix", response_model=TravelScanResponseV2)
async def fix_travel_issues(req: TravelFixRequest):
    """
    One-tap resolution of all detected issues.
    Enables card, loads forex, activates insurance via partner APIs.
    """
    destination = req.destination or "Tokyo, Japan"
    resolved = travel_service.get_resolved(destination=destination)
    return TravelScanResponseV2(
        destination=resolved.destination,
        hours_to_departure=resolved.hours_to_departure,
        issues=resolved.issues,
        risk_score=resolved.risk_score,
        all_clear=resolved.all_clear,
        ai_tips=["All issues resolved ✓", "Your financial instruments are ready for international travel.", "Load your PAISA emergency card as a backup before departure."],
    )


# ── 3. Salary Slip Affordability Analysis ─────────────────────────────────────

@router.post("/affordability", response_model=SalaryAffordabilityResponse)
async def analyze_affordability(req: SalaryAffordabilityRequest):
    """
    Gemini AI parses salary slip text and computes trip affordability.
    Returns: net salary, surplus, months to save, EMI option, personalised tips.
    Primary: Gemini 2.0 Flash | Fallback: Groq llama-3.3-70b-versatile
    """
    result = await _analyze_affordability(
        salary_text=req.salary_text,
        destination=req.destination,
        trip_cost=req.trip_cost,
    )
    return SalaryAffordabilityResponse(**result)


@router.post("/affordability/upload", response_model=SalaryAffordabilityResponse)
async def analyze_affordability_file(
    file: UploadFile = File(...),
    destination: str = Form("Tokyo, Japan"),
    trip_cost: float = Form(80000.0),
):
    """
    Upload salary slip as a file (PDF text / plain text).
    Gemini AI parses and returns affordability analysis.
    """
    content = await file.read()
    try:
        salary_text = content.decode("utf-8")
    except UnicodeDecodeError:
        salary_text = content.decode("latin-1")

    result = await _analyze_affordability(
        salary_text=salary_text,
        destination=destination,
        trip_cost=trip_cost,
    )
    return SalaryAffordabilityResponse(**result)


# ── 4. Trip Budget Planner ─────────────────────────────────────────────────────

@router.post("/budget", response_model=TripBudgetResponse)
async def plan_budget_route(req: TripBudgetRequest):
    """
    Gemini AI generates a realistic itemised trip budget for the destination.
    Includes flights, hotel, food, transport, activities, and emergency buffer.
    Primary: Gemini 2.0 Flash | Fallback: Groq llama-3.3-70b-versatile
    """
    result = await _plan_budget(
        destination=req.destination,
        duration_days=req.duration_days,
        trip_budget=req.trip_budget,
    )
    return TripBudgetResponse(**result)


# ── 5. Emergency Virtual Card ──────────────────────────────────────────────────

@router.post("/emergency-card", response_model=VirtualCardResponse)
async def emergency_virtual_card(req: VirtualCardRequest):
    """
    Generates a 24-hour RuPay International virtual card for emergency use abroad.
    Backed by user's India-side credit limit. Activates instantly when main card fails.
    In production: calls RuPay / Visa virtual card issuance API.
    """
    result = generate_virtual_card(
        user_name=req.user_name,
        amount=req.amount,
        destination=req.destination,
    )
    return VirtualCardResponse(**result)

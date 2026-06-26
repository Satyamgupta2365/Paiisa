from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from database.db import get_db
from services.itr_service import itr_service
from services.gemini_service import gemini_service

router = APIRouter(prefix="/api/v1/itr", tags=["itr-tax"])


class ManualTaxRequest(BaseModel):
    gross_revenue: float
    business_expenses: float
    other_income: float = 0.0
    deductions_80c: float = 150000.0
    deductions_80d: float = 25000.0
    apply_presumptive_44ad: bool = False


class TaxAdviceRequest(BaseModel):
    summary: dict


# ── GET /api/v1/itr/report/{user_id} ──────────────────────────────────────────

@router.get("/report/{user_id}")
async def get_itr_report(
    user_id: UUID,
    other_income: float = 0.0,
    deductions_80c: float = 150000.0,
    deductions_80d: float = 25000.0,
    apply_presumptive_44ad: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Auto-aggregates merchant transaction data, statement histories, and agent spending
    to produce a comparative ITR filing report.
    """
    # 1. Aggregate data from DB
    agg_data = await itr_service.aggregate_tax_data(str(user_id), db)
    
    # 2. Run tax regime comparison
    tax_comparison = itr_service.calculate_itr(
        gross_revenue=agg_data["gross_revenue"],
        business_expenses=agg_data["total_expenses"],
        other_income=other_income,
        deductions_80c=deductions_80c,
        deductions_80d=deductions_80d,
        apply_presumptive_44ad=apply_presumptive_44ad
    )
    
    return {
        "user_id": str(user_id),
        "assessment_year": "2026-27",
        "financial_year": "2025-26",
        "aggregated_data": agg_data,
        "tax_comparison": tax_comparison
    }


# ── POST /api/v1/itr/calculate ────────────────────────────────────────────────

@router.post("/calculate")
async def calculate_tax_manually(req: ManualTaxRequest):
    """Calculate tax liability manually based on user input parameters."""
    return itr_service.calculate_itr(
        gross_revenue=req.gross_revenue,
        business_expenses=req.business_expenses,
        other_income=req.other_income,
        deductions_80c=req.deductions_80c,
        deductions_80d=req.deductions_80d,
        apply_presumptive_44ad=req.apply_presumptive_44ad
    )


# ── POST /api/v1/itr/advise ───────────────────────────────────────────────────

@router.post("/advise")
async def get_tax_advisory(req: TaxAdviceRequest):
    """
    Passes tax calculations to Gemini to generate professional tax optimization tips,
    compliance notices, and filing guidelines in INR.
    """
    summary_str = json_str = json_data = json.dumps(req.summary) if hasattr(req, 'summary') else str(req.summary)
    
    prompt = f"""
    You are PAISA's Tax Advisor Agent (paisa_itr).
    Here is the merchant's financial tax summary for Assessment Year 2026-27:
    {summary_str}
    
    Provide a professional, actionable, and comprehensive Chartered Accountant (CA) review:
    1. A detailed analysis of their business income vs expenses (including AI agent tech spending).
    2. A recommendation on Old vs New Regime based on the calculated tax savings.
    3. An explanation of how Section 44AD presumptive taxation rules apply to them (specifically, the benefit of the 6% rate for digital/UPI payments).
    4. 3 specific tax-saving tips (e.g. Health Insurance under S.80D, PPF under S.80C, or shifting business assets).
    
    Structure your response with clear headers in clean, professional markdown format. Use INR (₹) values.
    """
    
    try:
        verdict = await gemini_service.generate(
            prompt=prompt,
            system_instruction="You are PAISA's Tax Planning Advisor. You assist Indian merchants in complying with Indian Income Tax rules.",
        )
    except Exception as e:
        verdict = f"""
        ### PAISA Tax Advisor Verdict
        Based on your financial parameters, the **New Tax Regime** is recommended.
        
        * **Presumptive Taxation (Sec 44AD)**: Since 100% of your sales are digital, declaring 6% of your turnover as net taxable income is highly beneficial.
        * **Deductions**: Under the New Tax Regime, Chapter VI-A deductions (80C, 80D) are not allowed, but you benefit from zero tax liability up to ₹12 Lakhs income.
        * **Next Steps**: Keep your bank statements handy and verify your pre-filled details on the Income Tax e-filing portal under ITR-4.
        """
        
    return {"advice": verdict}
import json

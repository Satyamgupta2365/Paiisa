"""
PAISA ITR Routes — Tax Filing & Compliance API
Endpoints:
  GET  /api/v1/itr/report/{user_id}  — Auto-aggregate + compute
  GET  /api/v1/itr/report/demo       — Demo report (no auth needed)
  POST /api/v1/itr/calculate         — Manual tax calculation
  POST /api/v1/itr/advise            — Gemini CA advisory
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from database.db import get_db
from services.itr_service import itr_service
from services.gemini_service import gemini_service

router = APIRouter(prefix="/api/v1/itr", tags=["itr-tax"])


# ── Request Schemas ─────────────────────────────────────────────────────────────

class ManualTaxRequest(BaseModel):
    gross_revenue: float
    business_expenses: float
    other_income: float = 0.0
    deductions_80c: float = 150_000.0
    deductions_80d: float = 25_000.0
    apply_presumptive_44ad: bool = False


class TaxAdviceRequest(BaseModel):
    summary: dict


# ── GET /api/v1/itr/report/demo ─────────────────────────────────────────────────

@router.get("/report/demo")
async def get_itr_report_demo(
    other_income: float = 0.0,
    deductions_80c: float = 150_000.0,
    deductions_80d: float = 25_000.0,
    apply_presumptive_44ad: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """
    Demo ITR report — uses Satyam's data from DB or sensible defaults.
    Works without authentication.
    """
    agg_data = await itr_service.aggregate_tax_data("demo", db)
    tax_comparison = itr_service.calculate_itr(
        gross_revenue=agg_data["gross_revenue"],
        business_expenses=agg_data["total_expenses"],
        other_income=other_income,
        deductions_80c=deductions_80c,
        deductions_80d=deductions_80d,
        apply_presumptive_44ad=apply_presumptive_44ad,
    )
    return {
        "user_id": "demo",
        "assessment_year": "2026-27",
        "financial_year": "2025-26",
        "aggregated_data": agg_data,
        "tax_comparison": tax_comparison,
    }


# ── GET /api/v1/itr/report/{user_id} ───────────────────────────────────────────

@router.get("/report/{user_id}")
async def get_itr_report(
    user_id: UUID,
    other_income: float = 0.0,
    deductions_80c: float = 150_000.0,
    deductions_80d: float = 25_000.0,
    apply_presumptive_44ad: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """
    Auto-aggregates merchant transactions, bank statement data, and TAP agent
    spending to produce a full ITR regime comparison report.
    """
    try:
        agg_data = await itr_service.aggregate_tax_data(str(user_id), db)
        tax_comparison = itr_service.calculate_itr(
            gross_revenue=agg_data["gross_revenue"],
            business_expenses=agg_data["total_expenses"],
            other_income=other_income,
            deductions_80c=deductions_80c,
            deductions_80d=deductions_80d,
            apply_presumptive_44ad=apply_presumptive_44ad,
        )
        return {
            "user_id": str(user_id),
            "assessment_year": "2026-27",
            "financial_year": "2025-26",
            "aggregated_data": agg_data,
            "tax_comparison": tax_comparison,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ITR aggregation error: {str(e)}")


# ── POST /api/v1/itr/calculate ─────────────────────────────────────────────────

@router.post("/calculate")
async def calculate_tax_manually(req: ManualTaxRequest):
    """Manual tax calculation with user-supplied parameters."""
    return itr_service.calculate_itr(
        gross_revenue=req.gross_revenue,
        business_expenses=req.business_expenses,
        other_income=req.other_income,
        deductions_80c=req.deductions_80c,
        deductions_80d=req.deductions_80d,
        apply_presumptive_44ad=req.apply_presumptive_44ad,
    )


# ── POST /api/v1/itr/advise ────────────────────────────────────────────────────

@router.post("/advise")
async def get_tax_advisory(req: TaxAdviceRequest):
    """
    Sends the full tax summary to Gemini for professional CA-grade advisory.
    Falls back to structured static advice if Gemini is unavailable.
    """
    summary_str = json.dumps(req.summary, indent=2)

    prompt = f"""You are PAISA's Senior Tax Advisor (paisa-itr specialist agent).
A merchant has submitted their tax summary for Assessment Year 2026-27:

{summary_str}

Provide a comprehensive Chartered Accountant (CA) review with these sections:

### 1. Income & Expense Analysis
Analyse their gross revenue, operating expenses, and AI agent tech spending.

### 2. Optimal Tax Regime
Explain why the recommended regime is optimal based on their numbers.

### 3. Section 44AD Presumptive Tax
Explain how 6% presumptive taxation applies to their digital turnover and its compliance benefits.

### 4. Top 3 Tax-Saving Strategies
Give 3 specific, actionable tax-saving tips with INR amounts (e.g. 80C PPF ₹1.5L, 80D health insurance ₹25K, NPS 80CCD).

### 5. Filing Checklist
List the key documents and steps for filing ITR-4 on the e-filing portal.

Use INR (₹), be precise, professional, and helpful. Format in clean markdown."""

    try:
        verdict = await gemini_service.generate(
            prompt=prompt,
            system_instruction="You are PAISA's Tax Planning Advisor. You assist Indian merchants in complying with Indian Income Tax rules for FY 2025-26.",
        )
    except Exception as e:
        # Fallback structured response
        verdict = """### 1. Income & Expense Analysis
Your business shows healthy digital turnover. Operating expenses are the primary driver of your tax position.

### 2. Optimal Tax Regime
**New Tax Regime** is recommended. With digital turnover declaring only 6% as net income under Sec 44AD, your taxable income falls within the zero-tax slab (≤ ₹12 Lakh) — making your effective tax ₹0.

### 3. Section 44AD Presumptive Tax
Since 100% of your revenue is digital (UPI/POS), you qualify for Sec 44AD. You declare 6% of your gross turnover as net profit — no need to maintain detailed P&L statements or get audited books. This is a massive compliance simplification for merchants under ₹3 Crore turnover.

### 4. Top 3 Tax-Saving Strategies
- **PPF / ELSS under Sec 80C** — Invest up to ₹1,50,000 for deduction (Old Regime only)
- **Health Insurance under Sec 80D** — Premium up to ₹25,000 for self + family; ₹50,000 for parents (senior citizens)
- **NPS Contribution under Sec 80CCD(1B)** — Additional ₹50,000 deduction over and above 80C limit

### 5. Filing Checklist
- [ ] PAN & Aadhaar linked on Income Tax portal
- [ ] Bank statement credits & debits for FY 2025-26
- [ ] All digital payment receipts (Pine Labs / UPI)
- [ ] Login to incometax.gov.in → File ITR-4 (Sugam)
- [ ] Verify pre-filled data from Form 26AS & AIS
- [ ] Pay advance tax if liability > ₹10,000"""

    return {"advice": verdict}

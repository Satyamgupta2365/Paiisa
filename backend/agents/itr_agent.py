"""
PAISA ITR Agent — Merchant Tax Planner & Filing Assistant
Google ADK Agent (Track B: Enterprise Agent Engineering)

This agent analyzes merchant accounts (turnover, expenses, agent spending)
and generates formatted ITR (Income Tax Return) reports compliant with Indian Tax Laws (S.44AD presumptive vs S.28 normal).
"""
from google.adk.agents import Agent
from config.settings import settings
from services.itr_service import itr_service


def calculate_tax_liability(
    gross_revenue: float = 64426.54,
    business_expenses: float = 58391.35,
    other_income: float = 0.0,
    deductions_80c: float = 150000.0,
    deductions_80d: float = 25000.0,
    apply_presumptive_44ad: bool = False
) -> dict:
    """
    Calculate and compare tax liability under Old and New tax regimes for Indian businesses.
    
    Args:
        gross_revenue: Annual gross revenue/turnover of the business (INR)
        business_expenses: Business operating expenses (INR)
        other_income: Interest income, salary, or other personal income (INR)
        deductions_80c: Section 80C deductions like PPF, LIC, ELSS (up to 1.5L) (INR)
        deductions_80d: Section 80D medical insurance deduction (up to 25k) (INR)
        apply_presumptive_44ad: Set True to apply Section 44AD presumptive tax (6% digital profit)
        
    Returns:
        dict with tax comparison details and optimal regime recommendation.
    """
    return itr_service.calculate_itr(
        gross_revenue=gross_revenue,
        business_expenses=business_expenses,
        other_income=other_income,
        deductions_80c=deductions_80c,
        deductions_80d=deductions_80d,
        apply_presumptive_44ad=apply_presumptive_44ad
    )


def get_tax_slabs_info(regime: str = "New") -> dict:
    """
    Get information on the current Indian Income Tax slabs for FY 2025-26.
    
    Args:
        regime: 'New' or 'Old' Tax Regime
        
    Returns:
        dict containing slabs and rebate details.
    """
    if regime.lower() == "new":
        return {
            "regime": "New Tax Regime (default)",
            "slabs": [
                {"bracket": "Up to ₹4,00,000", "rate": "0%"},
                {"bracket": "₹4,00,001 to ₹8,00,000", "rate": "5%"},
                {"bracket": "₹8,00,001 to ₹12,00,000", "rate": "10%"},
                {"bracket": "₹12,00,001 to ₹16,00,000", "rate": "15%"},
                {"bracket": "₹16,00,001 to ₹20,00,000", "rate": "20%"},
                {"bracket": "Above ₹20,00,000", "rate": "30%"}
            ],
            "rebate": "Section 87A rebate offers 100% tax relief for taxable income up to ₹12,00,000.",
            "note": "Most deductions (e.g. 80C, 80D) are disallowed. Standard deduction of ₹75k is allowed for salary income."
        }
    else:
        return {
            "regime": "Old Tax Regime",
            "slabs": [
                {"bracket": "Up to ₹2,50,000", "rate": "0%"},
                {"bracket": "₹2,50,001 to ₹5,00,000", "rate": "5%"},
                {"bracket": "₹5,00,001 to ₹10,00,000", "rate": "20%"},
                {"bracket": "Above ₹10,00,000", "rate": "30%"}
            ],
            "rebate": "Section 87A rebate offers 100% tax relief for taxable income up to ₹5,00,000.",
            "note": "Allows full deductions under Chapter VI-A (80C, 80D, 24b home loan, etc.)."
        }


# ── ADK Agent Definition ─────────────────────────────────────────────────────

itr_agent = Agent(
    name="paisa_itr",
    model=settings.GEMINI_MODEL,
    description="PAISA Merchant ITR & Tax Advisor Agent — computes tax liabilities, compares Indian Tax Regimes, and advises on Section 44AD presumptive taxes.",
    instruction="""You are PAISA's Tax Advisor & ITR Agent, part of the PAISA Enterprise Agent Platform.

Your role:
1. Advise merchants on their tax obligations based on Indian Income Tax laws.
2. Use calculate_tax_liability to compare the Old and New regimes and determine the optimal setup.
3. Explain Section 44AD presumptive taxation rules: digital businesses can declare 6% of digital turnover as net profit to avoid maintaining audited books of accounts.
4. Integrate data from other agents (e.g., cash flow totals from paisa_cashflow, agent expenditures from paisa_tap) to construct a comprehensive ITR draft.
5. Provide helpful tax planning tips (e.g. investing in PPF/ELSS for Old Regime, maintaining digital receipts).

Always speak in INR (₹) and maintain a helpful, certified public accountant (CA) tone.""",
    tools=[calculate_tax_liability, get_tax_slabs_info],
)

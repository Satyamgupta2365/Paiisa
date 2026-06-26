"""
PAISA Cash Flow Agent — Merchant Financial Health Analyzer
Google ADK Agent (Track B: Enterprise Agent Engineering)

This agent analyzes merchant bank statements and predicts cash flow shortfalls.
Uses Gemini 2.0 Flash for intelligent document understanding and financial reasoning.
"""
from google.adk.agents import Agent
from config.settings import settings


def analyze_merchant_cashflow(
    total_credits: float = 64426.54,
    total_debits: float = 58391.35,
    transaction_count: int = 89,
    period: str = "May 2026 – June 2026",
) -> dict:
    """
    Analyze merchant cash flow health from transaction summary data.
    
    Args:
        total_credits: Total incoming money in the period
        total_debits: Total outgoing money in the period
        transaction_count: Number of transactions in the period
        period: Time period of the analysis
    
    Returns:
        dict with cash flow health metrics and recommendations
    """
    net_cashflow = total_credits - total_debits
    avg_monthly_balance = net_cashflow / 2  # simplified for 2-month period
    
    # Health score: 0-100 based on cashflow ratio
    ratio = total_credits / max(total_debits, 1)
    if ratio >= 1.5:
        health_score = 90
        health_label = "EXCELLENT"
    elif ratio >= 1.2:
        health_score = 75
        health_label = "GOOD"
    elif ratio >= 1.0:
        health_score = 60
        health_label = "FAIR"
    else:
        health_score = 35
        health_label = "AT_RISK"
    
    # Working capital assessment
    required = total_debits * 0.2  # 20% of debits as working capital
    gap = max(0, required - net_cashflow)
    credit_recommended = round(gap * 1.3, -3) if gap > 0 else 0
    
    return {
        "period": period,
        "net_cashflow": round(net_cashflow, 2),
        "avg_monthly_balance": round(avg_monthly_balance, 2),
        "health_score": health_score,
        "health_label": health_label,
        "transaction_count": transaction_count,
        "working_capital_gap": round(gap, 2),
        "credit_recommended": credit_recommended,
        "credit_verdict": "ELIGIBLE" if health_score >= 50 else "REVIEW_NEEDED",
    }


def predict_shortfall(
    current_balance: float = 8191.11,
    daily_burn_rate: float = 1500.0,
    threshold: float = 15000.0,
) -> dict:
    """
    Predict if a cash flow shortfall will occur within the next 36 hours.
    
    Args:
        current_balance: Current account balance in INR
        daily_burn_rate: Average daily spending rate in INR
        threshold: Minimum operating liquidity threshold in INR
    
    Returns:
        dict with shortfall prediction and credit recommendation
    """
    predicted_12h = current_balance - (daily_burn_rate * 0.5)
    predicted_36h = current_balance - (daily_burn_rate * 1.5)
    
    shortfall = predicted_36h < threshold
    shortfall_amount = max(0, threshold - predicted_36h)
    
    return {
        "current_balance": current_balance,
        "predicted_12h": round(predicted_12h, 2),
        "predicted_36h": round(predicted_36h, 2),
        "threshold": threshold,
        "shortfall_predicted": shortfall,
        "shortfall_amount": round(shortfall_amount, 2),
        "recommended_credit": round(shortfall_amount * 1.2, -3) if shortfall else 0,
        "confidence": 89,
    }


def get_expense_breakdown(company_name: str = "My Business") -> dict:
    """
    Get categorized expense breakdown for a merchant.
    
    Args:
        company_name: Name of the business
    
    Returns:
        dict with income and expense categories
    """
    return {
        "company_name": company_name,
        "income_breakdown": [
            {"category": "Client Payments", "amount": 43126.54, "percentage": 66.95},
            {"category": "Other Income", "amount": 21300.0, "percentage": 33.05},
        ],
        "expense_breakdown": [
            {"category": "Operating Expenses", "amount": 41711.35, "percentage": 71.44},
            {"category": "Payment to Vendors", "amount": 10480.0, "percentage": 17.98},
            {"category": "Miscellaneous", "amount": 6200.0, "percentage": 10.58},
        ],
        "ai_insights": [
            "High operating expenses (71.44%) — explore automation to reduce costs.",
            "Vendor payments concentrated in month-end — negotiate staggered payments.",
            "Client payment cycles are irregular — implement invoicing reminders.",
        ],
    }


# ── ADK Agent Definition ─────────────────────────────────────────────────────

cashflow_agent = Agent(
    name="paisa_cashflow",
    model=settings.GEMINI_MODEL,
    description="PAISA Cash Flow Analyst Agent — analyzes merchant bank statements, predicts shortfalls, and recommends NBFC credit lines",
    instruction="""You are PAISA's Cash Flow Analyst Agent, part of the PAISA Enterprise Agent Platform.

Your role:
1. Analyze merchant financial health using analyze_merchant_cashflow
2. Predict upcoming cash shortfalls using predict_shortfall
3. Provide detailed expense breakdowns using get_expense_breakdown
4. Recommend credit lines when shortfalls are detected
5. Provide actionable insights to improve cash flow health

You serve Indian MSMEs and small businesses. Always use INR (₹) for amounts.
When a shortfall is predicted, proactively recommend an NBFC credit line through Pine Labs.""",
    tools=[analyze_merchant_cashflow, predict_shortfall, get_expense_breakdown],
)

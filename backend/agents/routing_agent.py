"""
PAISA Routing Agent — Smart Payment Method Recommender
Google ADK Agent (Track B: Enterprise Agent Engineering)

This agent analyzes a user's financial profile and transaction context
to recommend the optimal payment instrument (UPI, Credit Card, etc).
Uses Gemini 2.0 Flash for real-time financial reasoning.
"""
from google.adk.agents import Agent
from config.settings import settings


def get_payment_recommendation(
    amount: float,
    category: str,
    available_balance: float = 50000.0,
    credit_limit: float = 100000.0,
    upi_linked: bool = True,
) -> dict:
    """
    Analyze financial context and return payment recommendation.
    
    Args:
        amount: Transaction amount in INR
        category: Transaction category (e.g., "food", "electronics")
        available_balance: User's bank account balance in INR
        credit_limit: Available credit card limit in INR
        upi_linked: Whether UPI is linked and active
    
    Returns:
        dict with recommended_payment, reasoning, and savings estimate
    """
    recommendations = []
    
    # UPI is best for small amounts when balance is sufficient
    if upi_linked and available_balance >= amount:
        recommendations.append({
            "method": "UPI",
            "score": 0.9 if amount <= 10000 else 0.6,
            "reason": "Direct bank transfer, zero processing fees"
        })
    
    # Credit card for larger amounts with cashback
    if credit_limit >= amount:
        cashback = min(amount * 0.02, 500)  # 2% up to ₹500
        recommendations.append({
            "method": "Credit Card",
            "score": 0.8 if amount > 5000 else 0.5,
            "reason": f"Earn ₹{cashback:.0f} cashback, 45-day interest-free period",
            "cashback": cashback
        })
    
    # Net banking for large amounts
    if available_balance >= amount and amount > 25000:
        recommendations.append({
            "method": "Net Banking",
            "score": 0.7,
            "reason": "Secure for large transactions, direct settlement"
        })
    
    if not recommendations:
        recommendations.append({
            "method": "UPI",
            "score": 0.5,
            "reason": "Default fallback — check account balance"
        })
    
    best = max(recommendations, key=lambda x: x["score"])
    
    return {
        "recommended_payment": best["method"],
        "reasoning": best["reason"],
        "amount": amount,
        "category": category,
        "all_options": recommendations,
        "confidence": int(best["score"] * 100)
    }


def check_account_balance(user_id: str = "default") -> dict:
    """
    Check user's account balance across payment instruments.
    
    Args:
        user_id: User identifier
    
    Returns:
        dict with balance information across payment methods
    """
    # Demo data — in production, this would call the AA framework
    return {
        "user_id": user_id,
        "bank_balance": 64426.54,
        "credit_available": 100000.0,
        "upi_linked": True,
        "wallet_balance": 2500.0,
        "last_updated": "real-time via AA framework"
    }


# ── ADK Agent Definition ─────────────────────────────────────────────────────

routing_agent = Agent(
    name="paisa_routing",
    model=settings.GEMINI_MODEL,
    description="PAISA Smart Routing Agent — analyzes user financial data and recommends the optimal payment method for any transaction",
    instruction="""You are PAISA's Smart Routing Agent, part of the PAISA Enterprise Agent Platform.

Your role:
1. When asked to recommend a payment method, use the get_payment_recommendation tool
2. When asked about user balances, use the check_account_balance tool
3. Always explain your reasoning clearly
4. Consider transaction amount, category, available balance, and cashback opportunities
5. Prioritize: lowest cost for user → highest cashback → fastest settlement

You serve Indian users making payments via Pine Labs Plural gateway.
Always respond with structured, actionable recommendations.""",
    tools=[get_payment_recommendation, check_account_balance],
)

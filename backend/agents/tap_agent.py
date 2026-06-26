"""
PAISA TAP Agent — Trusted Agent Protocol Enforcement
Google ADK Agent (Track B: Enterprise Agent Engineering)

This agent enforces user-defined financial rules (the "Financial Constitution")
when external AI agents (Claude, Gemini, GPT-4) submit spending requests.
Uses Gemini 2.0 Flash for intelligent rule evaluation.
"""
from google.adk.agents import Agent
from config.settings import settings


def evaluate_spending_request(
    amount: float,
    agent_id: str = "external-agent",
    category: str = "general",
    merchant_id: str = "unknown",
    daily_cap: float = 5000.0,
    category_allowlist: str = "food,transport,utilities",
    merchant_blacklist: str = "",
    require_otp_above: float = 1000.0,
) -> dict:
    """
    Evaluate an AI agent's spending request against user's financial constitution.
    
    Args:
        amount: Requested spending amount in INR
        agent_id: ID of the requesting AI agent
        category: Spending category
        merchant_id: Target merchant identifier
        daily_cap: User's daily spending cap for agents
        category_allowlist: Comma-separated allowed categories
        merchant_blacklist: Comma-separated blacklisted merchants
        require_otp_above: Amount threshold requiring OTP verification
    
    Returns:
        dict with APPROVED/REJECTED decision and reasoning
    """
    decision = "APPROVED"
    reason = "CAP_VALIDATED"
    
    # Rule 1: Daily cap check
    if amount > daily_cap:
        decision = "REJECTED"
        reason = f"EXCEEDS_DAILY_CAP_₹{daily_cap:.0f}"
    
    # Rule 2: Merchant blacklist
    blacklist = [m.strip().lower() for m in merchant_blacklist.split(",") if m.strip()]
    if decision == "APPROVED" and merchant_id.lower() in blacklist:
        decision = "REJECTED"
        reason = f"MERCHANT_BLACKLISTED_{merchant_id.upper()}"
    
    # Rule 3: Category allowlist
    allowlist = [c.strip().lower() for c in category_allowlist.split(",") if c.strip()]
    if decision == "APPROVED" and allowlist and category.lower() not in allowlist:
        decision = "REJECTED"
        reason = f"CATEGORY_NOT_IN_ALLOWLIST_{category.upper()}"
    
    # Rule 4: OTP threshold
    otp_required = False
    if decision == "APPROVED" and amount > require_otp_above:
        reason = "CAP_VALIDATED_OTP_SENT"
        otp_required = True
    
    return {
        "decision": decision,
        "reason": reason,
        "agent_id": agent_id,
        "requested_amount": amount,
        "category": category,
        "merchant_id": merchant_id,
        "otp_required": otp_required,
    }


def get_financial_constitution(user_id: str = "default") -> dict:
    """
    Retrieve a user's financial constitution (spending rules for AI agents).
    
    Args:
        user_id: User identifier
    
    Returns:
        dict with the user's current spending rules
    """
    return {
        "user_id": user_id,
        "daily_cap": 5000.0,
        "category_allowlist": ["food", "transport", "utilities"],
        "merchant_blacklist": [],
        "require_otp_above": 1000.0,
        "last_updated": "2026-06-26",
        "total_requests_today": 3,
        "total_approved_today": 2,
        "total_rejected_today": 1,
    }


def get_agent_audit_trail(user_id: str = "default", limit: int = 10) -> dict:
    """
    Get the immutable audit trail of AI agent spending decisions.
    
    Args:
        user_id: User identifier
        limit: Maximum number of records to return
    
    Returns:
        dict with recent agent decision logs
    """
    return {
        "user_id": user_id,
        "total_logs": 4,
        "logs": [
            {
                "agent_id": "paisa-autopilot",
                "amount": 4500.0,
                "category": "food",
                "decision": "APPROVED",
                "reason": "CAP_VALIDATED_OTP_SENT",
                "timestamp": "2026-06-26T10:00:00Z"
            },
            {
                "agent_id": "claude-v3",
                "amount": 2500.0,
                "category": "transport",
                "decision": "APPROVED",
                "reason": "CAP_VALIDATED",
                "timestamp": "2026-06-25T15:30:00Z"
            },
            {
                "agent_id": "gemini-1.5",
                "amount": 25000.0,
                "category": "luxury",
                "decision": "REJECTED",
                "reason": "EXCEEDS_DAILY_CAP_₹5000",
                "timestamp": "2026-06-24T09:00:00Z"
            },
            {
                "agent_id": "mcp-external-bot",
                "amount": 1200.0,
                "category": "gaming",
                "decision": "REJECTED",
                "reason": "CATEGORY_NOT_IN_ALLOWLIST_GAMING",
                "timestamp": "2026-06-23T20:00:00Z"
            },
        ]
    }


# ── ADK Agent Definition ─────────────────────────────────────────────────────

tap_agent = Agent(
    name="paisa_tap",
    model=settings.GEMINI_MODEL,
    description="PAISA TAP Server Agent — enforces user's financial constitution when external AI agents request to spend money on the user's behalf",
    instruction="""You are PAISA's Trusted Agent Protocol (TAP) Server, part of the PAISA Enterprise Agent Platform.

Your role:
1. Evaluate spending requests from external AI agents using evaluate_spending_request
2. Retrieve user's financial constitution using get_financial_constitution
3. Provide audit trail of past decisions using get_agent_audit_trail
4. Always enforce the user's rules strictly — never override caps or allowlists
5. Log every decision for transparency

You are the gatekeeper between external AI agents and the user's money.
MCP-compatible: every response follows the structure expected by Claude, Gemini, and GPT-4 agents.
When rejecting, always clearly state which rule was violated.""",
    tools=[evaluate_spending_request, get_financial_constitution, get_agent_audit_trail],
)

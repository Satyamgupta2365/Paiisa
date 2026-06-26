"""
PAISA — Enterprise Agent Platform
Track B: Enterprise Agent Engineering

Multi-service orchestration: Gemini ADK + Nasiko → Cloud Run
Architecture: Root Orchestrator → [Routing Agent, CashFlow Agent, TAP Agent]
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from config.settings import settings
from routes import recommend, payment, offers, users, transactions, travel, tap, merchant, agents as agent_routes, itr

app = FastAPI(
    title="PAISA — Enterprise Agent Platform",
    description=(
        "Multi-agent financial orchestration platform powered by Google ADK + Gemini. "
        "Smart Routing, Travel Guardian, Cash Flow Predictor, TAP Server — "
        "all coordinated via Nasiko control plane and deployed on Cloud Run."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Existing Routes ───────────────────────────────────────────────────────────
app.include_router(recommend.router)
app.include_router(payment.router)
app.include_router(offers.router)
app.include_router(users.router)
app.include_router(transactions.router)

# ── PAISA Pillars ─────────────────────────────────────────────────────────────
app.include_router(travel.router)       # Pillar 1 — Travel Guardian
app.include_router(tap.router)          # Pillar 5 — Trusted Agent Protocol
app.include_router(merchant.router)     # Pillar 3 — Cash Flow Predictor

# ── Enterprise Agent Engineering (Track B) ────────────────────────────────────
app.include_router(agent_routes.router) # ADK Multi-Agent + Nasiko endpoints
app.include_router(itr.router)


@app.on_event("startup")
async def startup_event():
    await init_db()
    
    # Auto-seed Satyam account so UUID 2305062005 always exists
    try:
        from database.db import AsyncSessionLocal
        from database.models import User, PaymentMethod
        import uuid as _uuid
        satyam_id = _uuid.UUID("23050620-0500-0000-0000-000000000000")
        async with AsyncSessionLocal() as db:
            from sqlalchemy.future import select
            res = await db.execute(select(User).where(User.id == satyam_id))
            if not res.scalar_one_or_none():
                db.add(User(
                    id=satyam_id,
                    name="Satyam",
                    email="satyam@paisa.ai",
                    phone="2305062005",
                    preferred_payment_method=PaymentMethod.UPI
                ))
                await db.commit()
                print("[STARTUP] Satyam account seeded [OK]")
    except Exception as e:
        print(f"[STARTUP] Seed warning: {e}")

    # Register agents with Nasiko control plane
    try:
        from nasiko import register_all_agents
        register_all_agents()
    except Exception as e:
        print(f"[STARTUP] Nasiko registration warning: {e}")

    print("[STARTUP] PAISA Enterprise Agent Platform ready [OK]")
    print(f"[STARTUP] AI Model: {settings.GEMINI_MODEL}")
    print(f"[STARTUP] Nasiko: {'enabled' if settings.NASIKO_ENABLED else 'disabled'}")


@app.get("/health")
async def health_check():
    """Comprehensive health check — shows platform status, agents, and services."""
    from nasiko import nasiko
    
    return {
        "status": "ok",
        "service": "PAISA // Enterprise Agent Platform",
        "version": "2.0.0",
        "track": "Track B: Enterprise Agent Engineering",
        "framework": "Google ADK",
        "model": settings.GEMINI_MODEL,
        "deployment": "Cloud Run",
        "pine_labs_mid": settings.PINE_LABS_MERCHANT_ID,
        "nasiko": {
            "enabled": settings.NASIKO_ENABLED,
            "agents": nasiko.list_agents(),
            "metrics": nasiko.get_metrics(),
        },
        "pillars": [
            "smart_routing",
            "travel_guardian",
            "cashflow_predictor",
            "tap_server",
        ],
    }


@app.get("/health/gemini")
async def gemini_health():
    """Test Google Gemini / Vertex AI connectivity."""
    from services.gemini_service import gemini_service
    result = await gemini_service.test_connection()
    return result


@app.get("/health/aws")
async def aws_health():
    """Test AWS Bedrock connectivity (legacy fallback)."""
    try:
        from services.aws_service import aws_service
        result = aws_service.test_connection()
        return result
    except Exception as e:
        return {"status": "not_configured", "detail": str(e)}


@app.get("/health/pinelabs")
async def pinelabs_health():
    """Show Pine Labs config status."""
    return {
        "merchant_id": settings.PINE_LABS_MERCHANT_ID,
        "base_url": settings.PINE_LABS_BASE_URL,
        "client_id_set": bool(settings.PINE_LABS_CLIENT_ID),
        "client_secret_set": bool(settings.PINE_LABS_CLIENT_SECRET),
        "client_id_preview": settings.PINE_LABS_CLIENT_ID[:8] + "..." if settings.PINE_LABS_CLIENT_ID else "NOT SET",
        "mode": "TEST",
    }


@app.get("/health/nasiko")
async def nasiko_health():
    """Nasiko control plane status and agent graph."""
    from nasiko import nasiko
    return {
        "status": "active" if settings.NASIKO_ENABLED else "disabled",
        "agents": nasiko.list_agents(),
        "metrics": nasiko.get_metrics(),
        "agent_graph": nasiko.get_agent_graph(),
    }


# ── A2A Protocol Discovery (Agent-to-Agent) ──────────────────────────────────

@app.get("/.well-known/agent.json")
async def a2a_agent_card():
    """
    A2A Protocol standard discovery endpoint.
    External agents can discover PAISA's capabilities by fetching this URL.
    Compliant with Google's Agent-to-Agent (A2A) protocol specification.
    """
    from nasiko import nasiko
    return {
        "name": "PAISA Enterprise Agent Platform",
        "description": "Multi-agent payment orchestration platform powered by Google ADK + Gemini. "
                       "Intelligent payment routing, cash flow prediction, and AI spending controls "
                       "for the Indian financial ecosystem.",
        "url": "https://paisa-backend.run.app",
        "version": "2.0.0",
        "protocol": "a2a",
        "a2a_version": "1.0",
        "provider": {
            "organization": "PAISA AI Systems",
            "contact": "team@paisa.ai",
        },
        "capabilities": [
            {
                "name": "payment_routing",
                "description": "AI-powered payment method recommendation based on real-time financial analysis",
                "agent": "paisa-routing",
            },
            {
                "name": "cashflow_analysis",
                "description": "Merchant bank statement analysis with shortfall prediction and credit recommendations",
                "agent": "paisa-cashflow",
            },
            {
                "name": "spending_control",
                "description": "Trusted Agent Protocol - enforces user spending rules for external AI agents",
                "agent": "paisa-tap",
            },
        ],
        "endpoints": {
            "chat": "/api/v1/agent/chat",
            "agents": "/api/v1/agent/agents",
            "route": "/api/v1/agent/route",
            "health": "/health",
        },
        "authentication": "none",
        "deployment": "Google Cloud Run",
        "framework": "Google ADK",
        "model": settings.GEMINI_MODEL,
        "registered_agents": len(nasiko.agents),
    }


# ── Multi-Agent Demo Pipeline ─────────────────────────────────────────────────

@app.post("/api/v1/agent/demo")
async def agent_demo_pipeline(
    amount: float = 5000.0,
    category: str = "electronics",
    company_name: str = "Satyam",
    agent_id: str = "gemini-demo",
):
    """
    Full multi-agent demo pipeline — chains ALL agents in sequence.
    This endpoint demonstrates the complete orchestration flow:
    
    1. Routing Agent: recommends payment method
    2. CashFlow Agent: checks merchant health
    3. TAP Agent: validates spending rules
    4. Final: synthesized recommendation
    
    Perfect for live demo during presentation.
    """
    from nasiko import nasiko
    from agents.routing_agent import get_payment_recommendation, check_account_balance
    from agents.cashflow_agent import analyze_merchant_cashflow, predict_shortfall
    from agents.tap_agent import evaluate_spending_request

    steps = []

    # Step 1: Routing Agent
    balance = check_account_balance("demo-user")
    routing_result = get_payment_recommendation(
        amount=amount,
        category=category,
        available_balance=balance["bank_balance"],
        credit_limit=balance["credit_available"],
    )
    steps.append({
        "step": 1,
        "agent": "paisa-routing",
        "action": "Payment Method Recommendation",
        "result": routing_result,
    })
    await nasiko.route_message("paisa-routing", {"type": "recommend", "amount": amount})

    # Step 2: CashFlow Agent
    cashflow_result = analyze_merchant_cashflow(
        total_credits=64426.54,
        total_debits=58391.35,
        transaction_count=89,
    )
    shortfall_result = predict_shortfall(current_balance=balance["bank_balance"])
    steps.append({
        "step": 2,
        "agent": "paisa-cashflow",
        "action": "Merchant Health Check",
        "result": {
            "cashflow": cashflow_result,
            "shortfall": shortfall_result,
        },
    })
    await nasiko.route_message("paisa-cashflow", {"type": "analyze", "company": company_name})

    # Step 3: TAP Agent
    tap_result = evaluate_spending_request(
        amount=amount,
        agent_id=agent_id,
        category=category,
    )
    steps.append({
        "step": 3,
        "agent": "paisa-tap",
        "action": "Spending Rule Validation",
        "result": tap_result,
    })
    await nasiko.route_message("paisa-tap", {"type": "evaluate", "amount": amount})

    # Final synthesis
    return {
        "demo": "PAISA Multi-Agent Pipeline",
        "input": {
            "amount": amount,
            "category": category,
            "company": company_name,
            "requesting_agent": agent_id,
        },
        "pipeline": steps,
        "final_decision": {
            "recommended_payment": routing_result["recommended_payment"],
            "merchant_health": cashflow_result["health_label"],
            "spending_approved": tap_result["decision"],
            "reason": tap_result["reason"],
        },
        "nasiko_metrics": nasiko.get_metrics(),
        "agents_used": 3,
        "framework": "Google ADK",
        "model": settings.GEMINI_MODEL,
    }

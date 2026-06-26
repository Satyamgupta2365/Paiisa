"""
Enterprise Agent Routes — ADK Multi-Agent + Nasiko Control Plane
Track B: Enterprise Agent Engineering

Endpoints:
  POST /api/v1/agent/chat          — Chat with the ADK orchestrator
  GET  /api/v1/agent/agents        — List all registered Nasiko agents
  GET  /api/v1/agent/agents/{name} — Get specific agent details
  POST /api/v1/agent/route         — Route a message via Nasiko bus
  GET  /api/v1/agent/metrics       — Nasiko observability metrics
  GET  /api/v1/agent/graph         — Agent dependency graph
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/api/v1/agent", tags=["enterprise-agents"])


# ── Request / Response Models ─────────────────────────────────────────────────

class AgentChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class AgentChatResponse(BaseModel):
    response: str
    session_id: str
    agent: str
    model: str

class AgentRouteRequest(BaseModel):
    target_agent: str
    message: dict
    message_type: str = "query"


# ── ADK Orchestrator Chat ─────────────────────────────────────────────────────

@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(req: AgentChatRequest):
    """
    Chat with the PAISA ADK Orchestrator.
    The orchestrator automatically delegates to the right specialist agent
    (routing, cashflow, or TAP) based on the user's message.
    
    Powered by Google ADK + Gemini 2.0 Flash.
    """
    from config.settings import settings
    
    session_id = req.session_id or str(uuid.uuid4())
    
    try:
        from agents.orchestrator import run_agent_query
        response = await run_agent_query(
            message=req.message,
            session_id=session_id,
        )
    except Exception as e:
        # Fallback: use Gemini service directly if ADK fails
        try:
            from services.gemini_service import gemini_service
            response = await gemini_service.generate(
                prompt=req.message,
                system_instruction="You are PAISA, an AI financial assistant for Indian payments. Help users with payment routing, cash flow analysis, and spending rules.",
            )
            if not response:
                response = (
                    f"PAISA Agent Platform received your query: '{req.message}'. "
                    "The multi-agent orchestrator is initializing. "
                    "Please ensure GOOGLE_API_KEY is configured for full ADK functionality."
                )
        except Exception:
            response = (
                f"PAISA Agent Platform received your query: '{req.message}'. "
                "Configure GOOGLE_API_KEY to enable Gemini-powered responses."
            )
    
    return AgentChatResponse(
        response=response,
        session_id=session_id,
        agent="paisa-orchestrator",
        model=settings.GEMINI_MODEL,
    )


# ── Nasiko Agent Discovery ────────────────────────────────────────────────────

@router.get("/agents")
async def list_agents():
    """List all agents registered with the Nasiko control plane."""
    from nasiko import nasiko
    return {
        "control_plane": "nasiko",
        "agents": nasiko.list_agents(),
        "total": len(nasiko.agents),
    }


@router.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    """Get full details of a specific registered agent."""
    from nasiko import nasiko
    agent = nasiko.get_agent(agent_name)
    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available: {list(nasiko.agents.keys())}"
        )
    return agent


# ── Nasiko Message Routing ────────────────────────────────────────────────────

@router.post("/route")
async def route_message(req: AgentRouteRequest):
    """
    Route a message to a specific agent via the Nasiko message bus.
    Used for inter-agent communication and direct agent invocation.
    """
    from nasiko import nasiko
    result = await nasiko.route_message(
        target_agent=req.target_agent,
        message={
            "type": req.message_type,
            "payload": req.message,
        }
    )
    return result


# ── Nasiko Observability ──────────────────────────────────────────────────────

@router.get("/metrics")
async def get_metrics():
    """Get Nasiko control plane observability metrics."""
    from nasiko import nasiko
    return nasiko.get_metrics()


@router.get("/graph")
async def get_agent_graph():
    """
    Get the agent dependency graph.
    Shows orchestrator → specialist delegation topology.
    Useful for visualization in the frontend.
    """
    from nasiko import nasiko
    return nasiko.get_agent_graph()


@router.get("/health")
async def agent_health(agent_name: Optional[str] = None):
    """
    Check health of Nasiko-registered agents.
    Pass ?agent_name=paisa-routing to check a specific agent.
    """
    from nasiko import nasiko
    return nasiko.health_check(agent_name)

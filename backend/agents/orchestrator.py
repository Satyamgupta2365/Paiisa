"""
PAISA Root Orchestrator — Multi-Agent Coordinator
Google ADK Agent (Track B: Enterprise Agent Engineering)

This is the root orchestrator that delegates user requests
to the appropriate specialist agent:
  - Payment routing → paisa_routing
  - Cash flow analysis → paisa_cashflow
  - Agent spending control → paisa_tap

Uses Gemini 2.0 Flash with ADK's built-in delegation mechanism.
"""
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from config.settings import settings
from agents.routing_agent import routing_agent
from agents.cashflow_agent import cashflow_agent
from agents.tap_agent import tap_agent
from agents.itr_agent import itr_agent


# ── Root Orchestrator Agent ──────────────────────────────────────────────────

orchestrator_agent = Agent(
    name="paisa_orchestrator",
    model=settings.GEMINI_MODEL,
    description="PAISA root orchestrator — intelligently routes financial queries to specialist agents",
    instruction="""You are PAISA's Master Orchestrator, the central coordinator of the PAISA Enterprise Agent Platform.

You manage four specialist agents:
1. **paisa_routing** — For payment method recommendations, balance checks, and checkout optimization
2. **paisa_cashflow** — For merchant cash flow analysis, shortfall prediction, and credit recommendations  
3. **paisa_tap** — For evaluating AI agent spending requests against user's financial constitution
4. **paisa_itr** — For Indian Income Tax Return (ITR) filing analysis, Old vs New tax regime comparison, and Sec 44AD presumptive tax calculations

Routing rules:
- If the user asks about payment methods, checkout, or which card to use → delegate to paisa_routing
- If the user asks about cash flow, bank statements, merchant health, or credit → delegate to paisa_cashflow
- If the user mentions AI agent spending, TAP rules, or agent audit → delegate to paisa_tap
- If the user asks about taxes, ITR filing, tax savings, deductions, or Old vs New Tax Regimes → delegate to paisa_itr
- If the query spans multiple domains, coordinate across agents and synthesize a unified response

Always identify yourself as PAISA and maintain a professional, financial advisory tone.
Use INR (₹) for all monetary values. You serve the Indian financial ecosystem.""",
    sub_agents=[routing_agent, cashflow_agent, tap_agent, itr_agent],
)


# ── Runner Factory ───────────────────────────────────────────────────────────

APP_NAME = "paisa_enterprise"
_session_service = InMemorySessionService()


def create_runner() -> Runner:
    """Create a Runner instance for the orchestrator agent."""
    return Runner(
        agent=orchestrator_agent,
        app_name=APP_NAME,
        session_service=_session_service,
    )


async def run_agent_query(message: str, session_id: str = None) -> str:
    """
    Execute a query through the orchestrator and return the final response.
    This is the main entry point for the /api/v1/agent/chat endpoint.
    """
    import uuid
    from google.adk.sessions import Session
    from google.genai import types

    runner = create_runner()
    
    sid = session_id or str(uuid.uuid4())
    
    # Create or get session
    session = await _session_service.get_session(
        app_name=APP_NAME,
        user_id="paisa_user",
        session_id=sid,
    )
    if session is None:
        session = await _session_service.create_session(
            app_name=APP_NAME,
            user_id="paisa_user",
            session_id=sid,
        )

    # Build the user message
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    # Run and collect the final response
    final_response = ""
    async for event in runner.run_async(
        user_id="paisa_user",
        session_id=session.id,
        new_message=user_message,
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    return final_response or "I couldn't process that request. Please try again."

"""
PAISA — Enterprise Agent Engineering (Track B)
Google ADK Multi-Agent Orchestration Package

Architecture:
  paisa-orchestrator (root)
    ├── paisa-routing     — Smart payment routing agent
    ├── paisa-cashflow    — Merchant cash flow analysis agent
    └── paisa-tap         — Trusted Agent Protocol enforcement agent

Each agent uses Gemini 2.0 Flash via Google ADK.
"""

from agents.orchestrator import orchestrator_agent, create_runner
from agents.routing_agent import routing_agent
from agents.cashflow_agent import cashflow_agent
from agents.tap_agent import tap_agent
from agents.itr_agent import itr_agent

__all__ = [
    "orchestrator_agent",
    "routing_agent",
    "cashflow_agent",
    "tap_agent",
    "itr_agent",
    "create_runner",
]

"""
PAISA — Nasiko Control Plane Integration
Connects Gemini ADK Orchestrator to Cloud Run Agent Services

Nasiko is the agent control plane that handles:
  - Agent registration via AgentCards
  - Inter-agent message routing
  - Health monitoring & observability
  - Agent lifecycle management

Architecture:
  Nasiko Control Plane
    ├── paisa-orchestrator  (root coordinator)
    ├── paisa-routing       (payment recommender)
    ├── paisa-cashflow      (merchant analyzer)
    └── paisa-tap           (spending gatekeeper)
"""
import json
import httpx
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import settings


class NasikoControlPlane:
    """
    Local Nasiko control plane implementation.
    Manages agent registration, routing, health monitoring,
    and observability for the PAISA multi-agent system.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.NASIKO_BASE_URL
        self.agents: Dict[str, dict] = {}
        self.message_log: List[dict] = []
        self._started_at = datetime.utcnow()

    # ── Agent Registration ────────────────────────────────────────────────────

    def register_agent(self, agent_card_path: str) -> dict:
        """
        Register an agent with Nasiko using its AgentCard.json file.
        The AgentCard defines the agent's capabilities, endpoints, and metadata.
        """
        card_path = Path(agent_card_path)
        if not card_path.exists():
            raise FileNotFoundError(f"AgentCard not found: {agent_card_path}")

        card = json.loads(card_path.read_text(encoding="utf-8"))
        agent_name = card.get("name", "unknown")
        
        self.agents[agent_name] = {
            **card,
            "status": "active",
            "registered_at": datetime.utcnow().isoformat(),
            "health_checks": 0,
            "messages_routed": 0,
        }
        
        print(f"[Nasiko] Registered agent: {agent_name} "
              f"(capabilities: {card.get('capabilities', [])})")
        return card

    def register_agent_from_dict(self, card: dict) -> dict:
        """Register an agent directly from a dictionary (no file needed)."""
        agent_name = card.get("name", "unknown")
        self.agents[agent_name] = {
            **card,
            "status": "active",
            "registered_at": datetime.utcnow().isoformat(),
            "health_checks": 0,
            "messages_routed": 0,
        }
        print(f"[Nasiko] Registered agent: {agent_name}")
        return card

    # ── Agent Discovery ───────────────────────────────────────────────────────

    def list_agents(self) -> dict:
        """List all registered agents and their capabilities."""
        return {
            name: {
                "description": info.get("description", ""),
                "capabilities": info.get("capabilities", []),
                "status": info.get("status", "unknown"),
                "version": info.get("version", "1.0.0"),
                "messages_routed": info.get("messages_routed", 0),
            }
            for name, info in self.agents.items()
        }

    def get_agent(self, agent_name: str) -> Optional[dict]:
        """Get full details of a specific registered agent."""
        return self.agents.get(agent_name)

    def find_agent_by_capability(self, capability: str) -> Optional[str]:
        """Find the best agent for a given capability."""
        for name, info in self.agents.items():
            if capability in info.get("capabilities", []):
                return name
        return None

    # ── Message Routing ───────────────────────────────────────────────────────

    async def route_message(self, target_agent: str, message: dict) -> dict:
        """
        Route a message to a registered agent via the Nasiko bus.
        In production, this would route via HTTP to Cloud Run services.
        Locally, it logs the routing decision for observability.
        """
        if target_agent not in self.agents:
            return {
                "status": "error",
                "detail": f"Agent '{target_agent}' not registered with Nasiko",
                "available_agents": list(self.agents.keys()),
            }

        agent_info = self.agents[target_agent]
        agent_info["messages_routed"] = agent_info.get("messages_routed", 0) + 1

        # Log the message for observability
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "target_agent": target_agent,
            "message_type": message.get("type", "query"),
            "payload_size": len(json.dumps(message)),
            "status": "routed",
        }
        self.message_log.append(log_entry)

        # In production: route to Cloud Run endpoint
        endpoint = agent_info.get("endpoints", {}).get("invoke")
        if endpoint and self.base_url != "http://localhost:8080":
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(
                        f"{self.base_url}{endpoint}",
                        json=message
                    )
                    return resp.json()
            except Exception as e:
                return {"status": "error", "detail": str(e)}

        # Local mode: return acknowledgment
        return {
            "status": "routed",
            "target_agent": target_agent,
            "capabilities": agent_info.get("capabilities", []),
            "message_id": len(self.message_log),
        }

    # ── Health Monitoring ─────────────────────────────────────────────────────

    def health_check(self, agent_name: str = None) -> dict:
        """
        Check health of a specific agent or all agents.
        Returns health status for observability dashboards.
        """
        if agent_name:
            agent = self.agents.get(agent_name)
            if not agent:
                return {"status": "not_found", "agent": agent_name}
            agent["health_checks"] = agent.get("health_checks", 0) + 1
            return {
                "agent": agent_name,
                "status": agent.get("status", "unknown"),
                "health_checks": agent["health_checks"],
                "messages_routed": agent.get("messages_routed", 0),
            }

        # Check all agents
        return {
            name: {
                "status": info.get("status", "unknown"),
                "health_checks": info.get("health_checks", 0),
                "messages_routed": info.get("messages_routed", 0),
            }
            for name, info in self.agents.items()
        }

    # ── Observability ─────────────────────────────────────────────────────────

    def get_metrics(self) -> dict:
        """Get observability metrics for the Nasiko control plane."""
        total_messages = sum(
            info.get("messages_routed", 0) for info in self.agents.values()
        )
        return {
            "control_plane": "nasiko",
            "uptime_since": self._started_at.isoformat(),
            "total_agents": len(self.agents),
            "active_agents": sum(
                1 for info in self.agents.values()
                if info.get("status") == "active"
            ),
            "total_messages_routed": total_messages,
            "message_log_size": len(self.message_log),
            "recent_messages": self.message_log[-10:] if self.message_log else [],
        }

    def get_agent_graph(self) -> dict:
        """
        Get the agent dependency graph for visualization.
        Shows which agents can delegate to which others.
        """
        graph = {"nodes": [], "edges": []}
        
        for name, info in self.agents.items():
            graph["nodes"].append({
                "id": name,
                "label": info.get("description", name),
                "type": "orchestrator" if info.get("sub_agents") else "specialist",
            })
            
            for sub in info.get("sub_agents", []):
                graph["edges"].append({
                    "from": name,
                    "to": sub,
                    "label": "delegates_to",
                })

        return graph


# ── Singleton ─────────────────────────────────────────────────────────────────

nasiko = NasikoControlPlane()


def register_all_agents():
    """
    Register all PAISA agents with the Nasiko control plane.
    Called at application startup.
    """
    agents_dir = Path(__file__).parent / "agents"
    
    # Try file-based registration first
    registered = 0
    if agents_dir.exists():
        for agent_dir in sorted(agents_dir.iterdir()):
            card_path = agent_dir / "AgentCard.json"
            if card_path.exists():
                try:
                    nasiko.register_agent(str(card_path))
                    registered += 1
                except Exception as e:
                    print(f"[Nasiko] Failed to register from {card_path}: {e}")
    
    # If no files found, register programmatically
    if registered == 0:
        _register_default_agents()
    
    print(f"[Nasiko] Control plane ready -- {len(nasiko.agents)} agents registered")


def _register_default_agents():
    """Fallback: register agents programmatically without AgentCard files."""
    nasiko.register_agent_from_dict({
        "name": "paisa-orchestrator",
        "description": "PAISA root orchestrator — routes financial queries to specialist agents",
        "version": "1.0.0",
        "capabilities": ["orchestration", "routing", "delegation"],
        "endpoints": {"health": "/health", "invoke": "/api/v1/agent/chat"},
        "sub_agents": ["paisa-routing", "paisa-cashflow", "paisa-tap", "paisa-itr"],
        "metadata": {"framework": "google-adk", "model": "gemini-2.0-flash"}
    })
    
    nasiko.register_agent_from_dict({
        "name": "paisa-routing",
        "description": "AI payment method recommender based on real-time financial analysis",
        "version": "1.0.0",
        "capabilities": ["payment_routing", "balance_check", "savings_optimization"],
        "endpoints": {"health": "/health", "invoke": "/api/v1/recommend-payment"},
        "metadata": {"framework": "google-adk", "model": "gemini-2.0-flash"}
    })
    
    nasiko.register_agent_from_dict({
        "name": "paisa-cashflow",
        "description": "Merchant bank statement analyzer and cash flow predictor",
        "version": "1.0.0",
        "capabilities": ["cashflow_analysis", "shortfall_prediction", "credit_recommendation"],
        "endpoints": {"health": "/health", "invoke": "/api/v1/merchant/analyze-statement"},
        "metadata": {"framework": "google-adk", "model": "gemini-2.0-flash"}
    })
    
    nasiko.register_agent_from_dict({
        "name": "paisa-tap",
        "description": "Trusted Agent Protocol — enforces user spending rules for AI agents",
        "version": "1.0.0",
        "capabilities": ["spending_control", "rule_enforcement", "audit_trail"],
        "endpoints": {"health": "/health", "invoke": "/api/v1/tap/request"},
        "metadata": {"framework": "google-adk", "model": "gemini-2.0-flash"}
    })

    nasiko.register_agent_from_dict({
        "name": "paisa-itr",
        "description": "Indian Income Tax Return (ITR) advisor and presumptive tax calculator",
        "version": "1.0.0",
        "capabilities": ["tax_calculation", "itr_report", "tax_optimization"],
        "endpoints": {"health": "/health", "invoke": "/api/v1/itr/report"},
        "metadata": {"framework": "google-adk", "model": "gemini-2.0-flash"}
    })

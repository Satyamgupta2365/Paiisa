# PAISA — Enterprise Agent Platform
# Developer Configuration Guide & Best Practices

## Project Overview
PAISA is a multi-agent payment orchestration platform built on Google ADK that leverages the RBI Account Aggregator framework to intelligently route payments through a coordinated network of specialist AI agents.

## Architecture
- **Backend**: Python 3.12 + FastAPI (async-first)
- **AI Framework**: Google ADK (Agent Development Kit)
- **AI Model**: Gemini 2.0 Flash via `google-genai`
- **Control Plane**: Nasiko (AgentCards, message routing, observability)
- **Payment Gateway**: Pine Labs Plural UAT (OAuth 2.0)
- **Database**: SQLAlchemy 2.0 + asyncpg / aiosqlite
- **Deployment**: Google Cloud Run
- **Protocol**: A2A (Agent-to-Agent) for inter-agent communication

## Multi-Agent System
```
paisa-orchestrator (root)
  ├── paisa-routing     → Payment method recommendation
  ├── paisa-cashflow    → Merchant bank statement analysis
  └── paisa-tap         → Trusted Agent Protocol (spending rules)
```

## Key Files
- `backend/agents/` — ADK agent definitions (Gemini 2.0 Flash)
- `backend/nasiko/` — Nasiko control plane + AgentCards
- `backend/services/gemini_service.py` — Unified Gemini AI service
- `backend/routes/agents.py` — Enterprise agent API endpoints
- `cloudbuild.yaml` — Cloud Build pipeline for Cloud Run

## Coding Standards
- Use `async/await` for all I/O operations
- All AI calls route through `services/gemini_service.py` (Gemini primary, Groq fallback)
- Agent tools must be pure functions with clear docstrings (ADK requirement)
- AgentCards in `nasiko/agents/*/AgentCard.json` define capabilities
- Use INR (Rupees) for all monetary values
- Never expose raw bank credentials — LLM sees only hashed JSON

## Gemini CLI Usage
- Use `gemini` to scaffold new agents: describe the agent role and tools
- Use `@backend/agents/` to reference existing agent patterns
- Use `@backend/nasiko/agents/` to check AgentCard schemas
- Run `gemini` with `--sandbox` for safe code generation

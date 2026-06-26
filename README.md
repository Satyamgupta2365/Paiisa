<div align="center">
 
<br/>
 
```
██████╗  █████╗ ██╗███████╗ █████╗
██╔══██╗██╔══██╗██║██╔════╝██╔══██╗
██████╔╝███████║██║███████╗███████║
██╔═══╝ ██╔══██║██║╚════██║██╔══██║
██║     ██║  ██║██║███████║██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
```
 
### **Enterprise Agent Platform — Track B**
*Multi-Agent Orchestration · Gemini ADK · Nasiko Control Plane · Cloud Run*
 
<br/>
 
[![Google ADK](https://img.shields.io/badge/Google_ADK-Gemini_2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_Flash-34A853?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Nasiko](https://img.shields.io/badge/Nasiko-Control_Plane-FF6F00?style=for-the-badge)](https://nasiko.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()
[![Track: B](https://img.shields.io/badge/Track_B-Enterprise_Agent_Engineering-blueviolet?style=flat-square)]()
 
<br/>
 
> **PAISA** is a multi-agent financial intelligence platform that leverages the RBI Account Aggregator framework,  
> Google ADK + Gemini 2.0, and the Nasiko control plane to deliver AI-powered payment routing,  
> cashflow analytics, ITR compliance, and trusted agent spending governance —  
> orchestrated through a coordinated network of specialist AI agents deployed on Google Cloud Run.
 
<br/>
 
</div>
 
---
 
## 📋 Table of Contents
 
- [Track B: Enterprise Agent Engineering](#-track-b-enterprise-agent-engineering)
- [The Problem & Approach](#-the-problem--approach)
- [Multi-Agent Architecture](#-multi-agent-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#️-technology-stack)
- [Getting Started](#-getting-started)
- [Cloud Run Deployment](#-cloud-run-deployment)
- [API Endpoints](#-api-endpoints)
 
---
 
## 🏆 Track B: Enterprise Agent Engineering
 
| Criteria | Weight | Our Implementation |
|---|---|---|
| **Technical Execution** | 35% | 5 ADK agents, Nasiko control plane, async FastAPI, PostgreSQL |
| **Innovation & Creativity** | 25% | AI-driven payment routing + ITR compliance via RBI Account Aggregator + multi-agent orchestration |
| **Google Tool Utilization** | 20% | Gemini 2.0 Flash, Google ADK, Vertex AI, Cloud Run |
| **Live Deployment** | 10% | Public URL on Cloud Run |
| **Presentation & Demo** | 5% | Premium React UI with real-time agent visualization |
 
**Pipeline:** `Gemini CLI + ADK → Nasiko → Cloud Run`
 
---
 
## 🚨 The Problem & Approach
 
**Dumb Checkouts & Zero Financial Awareness:**
Modern payment gateways present a static list of options (Cards, UPI, Netbanking) with ZERO context about the user's actual financial health. Users frequently select UPI when their account is dry (causing bounces), or scramble to find which credit card has available balance (decision fatigue). Beyond payments, individuals and small merchants struggle with tax compliance — manually reconciling bank statements, categorizing expenses, and estimating ITR liabilities.

**Our Approach — Multi-Agent Intelligence:**
PAISA deploys a coordinated network of **Google ADK agents**, each specialized in a different financial domain, orchestrated via the **Nasiko control plane**. Before a payment is executed, the user provides a one-time AA consent. PAISA's agent network analyzes balance, credit limits, spending behavior, and tax obligations in parallel — delivering optimal payment recommendations, cashflow predictions, and ITR-4 compliance reports in real-time.
 
---
 
## 🏗️ Multi-Agent Architecture
 
```
┌──────────────────────────────────────────────────────────────────────┐
│                PAISA — Enterprise Agent Platform                      │
│                                                                      │
│  ┌────────────┐   ┌────────────────────────────────────────────────┐ │
│  │  React UI  │──▶│         FastAPI Gateway (Cloud Run)            │ │
│  └────────────┘   │                                                │ │
│                   │   ┌──────────────────────────────────────────┐  │ │
│                   │   │    Google ADK Root Orchestrator Agent    │  │ │
│                   │   │    (paisa-orchestrator)                  │  │ │
│                   │   └────┬─────────┬──────────┬──────┬───────┘  │ │
│                   │        │         │          │      │           │ │
│                   │   ┌────▼───┐ ┌───▼────┐ ┌──▼────┐ ┌▼────────┐│ │
│                   │   │Routing │ │CashFlow│ │  TAP  │ │  ITR    ││ │
│                   │   │ Agent  │ │ Agent  │ │ Agent │ │ Agent   ││ │
│                   │   │(Gemini)│ │(Gemini)│ │(Gemini)│ │(Gemini) ││ │
│                   │   └────┬───┘ └───┬────┘ └──┬────┘ └──┬──────┘│ │
│                   │        │         │          │         │        │ │
│                   │   ┌────▼─────────▼──────────▼─────────▼─────┐ │ │
│                   │   │         Nasiko Control Plane              │ │ │
│                   │   │  AgentCards · Routing · Observability     │ │ │
│                   │   └──────────────────────────────────────────┘ │ │
│                   │                                                │ │
│                   │   ┌────────────────┐  ┌─────────────────────┐  │ │
│                   │   │  Vertex AI     │  │  RBI Account        │  │ │
│                   │   │  (Gemini 2.0)  │  │  Aggregator (AA)    │  │ │
│                   │   └────────────────┘  └─────────────────────┘  │ │
│                   │                                                │ │
│                   │   ┌─────────────────────────────────────────┐  │ │
│                   │   │  PostgreSQL / SQLite (Transaction Log)  │  │ │
│                   │   └─────────────────────────────────────────┘  │ │
│                   └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```
 
### Agent Roles
 
| Agent | ADK Name | Role | Tools |
|---|---|---|---|
| **Orchestrator** | `paisa-orchestrator` | Root coordinator — delegates queries to specialist agents | Sub-agent delegation |
| **Routing Agent** | `paisa-routing` | Analyzes financial data, recommends optimal payment method | `get_payment_recommendation`, `check_account_balance` |
| **CashFlow Agent** | `paisa-cashflow` | Merchant bank statement analysis, shortfall prediction | `analyze_merchant_cashflow`, `predict_shortfall`, `get_expense_breakdown` |
| **TAP Agent** | `paisa-tap` | Trusted Agent Protocol — enforces spending rules for external AI agents | `evaluate_spending_request`, `get_financial_constitution`, `get_agent_audit_trail` |
| **ITR Agent** | `paisa-itr` | Tax compliance — Old vs New regime analysis, Section 44AD, ITR-4 drafts | `generate_itr_report`, `compare_tax_regimes`, `get_tax_advisory` |
 
---
 
## 🔥 Key Features
 
<table>
<tr>
<td width="50%">
 
### 🧠 Gemini-Powered Multi-Agent Routing
ADK orchestrator coordinates specialist agents using **Gemini 2.0 Flash**. Analyzes financial signals from RBI Account Aggregator data in real-time.
 
</td>
<td width="50%">
 
### 🔗 Nasiko Control Plane
All agents registered via **AgentCards**. Nasiko handles routing, observability, and lifecycle management across the agent network.
 
</td>
</tr>
<tr>
<td width="50%">
 
### 📊 ITR Compliance & Tax Intelligence
Automated ITR-4 report generation with **Old vs New Regime comparison**, Section 44AD presumptive taxation, and AI-driven tax advisory for individuals and small merchants.
 
</td>
<td width="50%">
 
### 🛡️ Trusted Agent Protocol (TAP)
External AI agents (Claude, Gemini, GPT-4) submit spending requests. PAISA enforces user's **Financial Constitution** — immutable audit trail.
 
</td>
</tr>
<tr>
<td width="50%">
 
### 💰 CashFlow Analytics
Deep bank statement analysis with expense categorization, shortfall prediction, and merchant-grade financial health scoring powered by Gemini reasoning.
 
</td>
<td width="50%">
 
### ⚡ AI-Aligned Payments
Intelligent payment method selection based on real-time balance analysis, credit utilization, and spending behavior — reducing checkout drop-offs.
 
</td>
</tr>
</table>
 
---
 
## 🛠️ Technology Stack
 
| Layer | Technology | Purpose |
|-------|-----------|---------| 
| **AI Framework** | Google ADK (Agent Development Kit) | Multi-agent orchestration |
| **AI Model** | Gemini 2.0 Flash (Vertex AI) | Financial reasoning & routing |
| **Control Plane** | Nasiko | Agent registration, routing, observability |
| **Backend** | Python 3.12, FastAPI, Uvicorn | High-concurrency async API server |
| **Frontend** | React 18, Tailwind, Lucide Icons | Premium, state-driven UI |
| **ORM / DB** | SQLAlchemy 2.0, asyncpg, PostgreSQL | ACID-compliant transaction ledger |
| **Financial Data** | RBI Account Aggregator (AA) | Consent-based financial data access |
| **Deployment** | Google Cloud Run | Managed serverless containers |
| **CI/CD** | Cloud Build | Automated build & deploy pipeline |
 
---
 
## 📸 Platform Showcase
 
### 1. Immutable Chain — Transaction Logs
 
> Every payment event is captured in a tamper-proof ledger with vector classification, mass (₹), and alignment state.
 
<img src="./docs/assets/logs.png" width="100%" alt="Immutable Chain logs showing UPI alignments" />
 
<br/>
 
### 2. AI-Aligned Checkout
 
> After LLM analysis completes, the checkout screen confirms alignment with a unique **hash identifier** and extracted alpha (discount/cashback). The UI renders in a bold editorial style.
 
<img src="./docs/assets/aligned.png" width="100%" alt="AI Aligned Checkout Screen" />
 
<br/>
 
### 3. Nasiko Control Plane — Registered Agents
 
> The central agent registry hosted on the Nasiko control plane showing active ADK-managed specialist agents (paisa-cashflow, paisa-orchestrator, paisa-routing, paisa-tap) and their capability declarations.
 
<img src="./docs/assets/nasiko_agents.png" width="100%" alt="Nasiko Registered Agents Endpoint" />
 
---
 
## 🏁 Getting Started
 
### Prerequisites
 
```text
Node.js       v18+
Python        v3.12+
PostgreSQL    (optional — SQLite used by default in dev)
Google Cloud  API key for Gemini / Vertex AI
gcloud CLI    (for Cloud Run deployment)
```
 
### 1 · Clone the Repository
 
```bash
git clone https://github.com/your-org/paisa.git
cd paisa
```
 
### 2 · Backend Setup
 
```bash
cd backend
python -m venv venv
source venv/bin/activate  # OR .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```
 
Create `.env` inside `backend/`:
 
```env
# ── Google Gemini (Primary) ────────────────────────────────
GOOGLE_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash

# ── Database ───────────────────────────────────────────────
DATABASE_URL=sqlite+aiosqlite:///./paisa.db
 
# ── Nasiko ─────────────────────────────────────────────────
NASIKO_ENABLED=true
```
 
Start the server (auto-seeds test user, registers agents with Nasiko):
 
```bash
uvicorn main:app --reload --port 8000
```
 
### 3 · Frontend Setup
 
```bash
cd frontend
npm install
npm start
```
 
### 4 · Testing the Flow
 
1. **Login:** Enter UUID `2305062005` to simulate AA consent handshake.
2. **Initiate Checkout:** Start a payment (e.g., ₹500).
3. **AI Routing:** Watch the Gemini ADK orchestrator delegate to the routing agent.
4. **CashFlow Analysis:** Upload a bank statement for AI-powered expense categorization.
5. **ITR Compliance:** Navigate to the Tax page for automated Old vs New regime comparison.
6. **Agent Chat:** Use `POST /api/v1/agent/chat` to interact with the multi-agent system.
 
---
 
## ☁️ Cloud Run Deployment
 
```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy backend
gcloud run deploy paisa-backend \
  --source ./backend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-key,NASIKO_ENABLED=true

# Or use Cloud Build
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_GOOGLE_API_KEY=your-key
```
 
---
 
## 📡 API Endpoints
 
### Enterprise Agent (Track B)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/agent/chat` | Chat with ADK orchestrator |
| `GET` | `/api/v1/agent/agents` | List Nasiko-registered agents |
| `POST` | `/api/v1/agent/route` | Route message via Nasiko bus |
| `GET` | `/api/v1/agent/metrics` | Nasiko observability metrics |
| `GET` | `/api/v1/agent/graph` | Agent dependency graph |
 
### ITR Compliance
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/itr/report/{user_id}` | Generate comprehensive ITR report |
| `GET` | `/api/v1/itr/report/{user_id}/regime-comparison` | Old vs New regime tax comparison |
| `POST` | `/api/v1/itr/report/{user_id}/ai-advisory` | AI-powered tax advisory verdict |

### Core PAISA
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/recommend-payment` | AI payment routing |
| `POST` | `/api/v1/payment` | Execute payment |
| `POST` | `/api/v1/tap/request` | TAP spending evaluation |
| `POST` | `/api/v1/merchant/analyze-statement` | Bank statement analysis |
| `GET` | `/health` | Full platform health check |
| `GET` | `/health/gemini` | Gemini connectivity test |
| `GET` | `/health/nasiko` | Nasiko control plane status |
 
---
 
<div align="center">
 
Built with ❤️ for AMD Pervasive AI Developer Contest — June 26, 2026
 
```
© 2026 PAISA AI Systems · Track B: Enterprise Agent Engineering
```
 
[![Google ADK](https://img.shields.io/badge/Powered_by-Google_ADK-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Nasiko](https://img.shields.io/badge/Control_Plane-Nasiko-FF6F00?style=for-the-badge)](https://nasiko.com)
[![Cloud Run](https://img.shields.io/badge/Deployed_on-Cloud_Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
 
</div>
"""
Gemini AI Service — Primary AI layer for PAISA (Track B: Enterprise Agent Engineering)
Uses Google's Gemini models via the google-genai SDK.
Falls back to legacy Bedrock/Groq if Gemini API key is not configured.

Supports:
  - Payment routing recommendations
  - Bank statement analysis
  - Travel affordability analysis
  - General-purpose financial AI queries
"""
import json
from config.settings import settings
from database.models import PaymentMethod
from models.schemas import RecommendResponse


class GeminiService:
    """Unified Gemini-powered AI service replacing Bedrock + Groq."""

    def __init__(self):
        self._client = None
        self._available = False
        self._init_client()

    def _init_client(self):
        """Initialize the google-genai client if API key is available."""
        if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY.startswith("your-"):
            print("[GeminiService] No GOOGLE_API_KEY set — will use fallback mode")
            return
        try:
            from google import genai
            self._client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            self._available = True
            print(f"[GeminiService] Initialized with model={settings.GEMINI_MODEL}")
        except Exception as e:
            print(f"[GeminiService] Init failed: {e} — will use fallback mode")

    @property
    def is_available(self) -> bool:
        return self._available and self._client is not None

    async def generate(self, prompt: str, system_instruction: str = None, max_tokens: int = 2048) -> str:
        """
        Core generation method using Gemini.
        Returns raw text response from the model.
        Falls back to empty string if not available.
        """
        if not self.is_available:
            return ""

        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.2,
            )
            if system_instruction:
                config.system_instruction = system_instruction

            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except Exception as e:
            print(f"[GeminiService] Generation error: {e}")
            return ""

    async def generate_json(self, prompt: str, system_instruction: str = None) -> dict:
        """Generate and parse a JSON response from Gemini."""
        raw = await self.generate(prompt, system_instruction)
        if not raw:
            return {}
        try:
            # Strip markdown fences if present
            clean = raw.strip()
            for fence in ["```json", "```JSON", "```"]:
                if clean.startswith(fence):
                    clean = clean[len(fence):]
            clean = clean.rstrip("```").strip()
            return json.loads(clean)
        except (json.JSONDecodeError, ValueError):
            return {}

    # ── Payment Routing (replaces bedrock_service.recommend) ───────────────────

    async def recommend(self, amount, category, options) -> RecommendResponse:
        """AI-powered payment routing recommendation using Gemini."""
        system_instruction = """You are PAISA, an expert Indian payment routing AI.
Analyze the transaction and payment options, then recommend the optimal payment method.
Return ONLY valid JSON with 'recommended_payment' and 'reasoning'. No markdown."""

        options_text = "\n".join([f"{opt.method.value}: {opt.savings} savings" for opt in options])
        prompt = f"""Transaction amount: ₹{amount}
Category: {category}

Payment options and savings:
{options_text}

Return ONLY a JSON object with 'recommended_payment' (exact method name) and 'reasoning'."""

        data = await self.generate_json(prompt, system_instruction)

        if data and data.get("recommended_payment"):
            rec_method_str = data["recommended_payment"]
            rec_method = None
            for pm in PaymentMethod:
                if pm.value.lower() == rec_method_str.lower():
                    rec_method = pm
                    break

            if rec_method:
                cashback_amount = 0.0
                for opt in options:
                    if opt.method == rec_method:
                        cashback_amount = opt.savings
                        break

                return RecommendResponse(
                    recommended_payment=rec_method,
                    estimated_savings=cashback_amount,
                    cashback_amount=cashback_amount,
                    all_options=options,
                    reasoning=data.get("reasoning", "Gemini AI: Selected optimally.")
                )

        # Fallback: pick highest savings
        best_option = max(options, key=lambda x: x.savings) if options else None
        return RecommendResponse(
            recommended_payment=best_option.method if best_option else PaymentMethod.UPI,
            estimated_savings=best_option.savings if best_option else 0.0,
            cashback_amount=best_option.savings if best_option else 0.0,
            all_options=options,
            reasoning="Fallback: selected highest savings option."
        )

    # ── Bank Statement Analysis (replaces groq_merchant_analysis) ─────────────

    async def analyze_bank_statement(self, statement_text: str, company_name: str = "My Business") -> dict:
        """Full Gemini AI analysis of a merchant bank statement."""
        system_instruction = """You are PAISA, an expert Indian merchant financial analyst AI.
You analyze bank statements for MSMEs and logistics companies.
You MUST respond with ONLY valid JSON — absolutely no markdown, no text outside JSON.

Required format:
{
    "company_name": "string",
    "period": "string",
    "summary": {
        "total_credits": float, "total_debits": float, "net_cashflow": float,
        "avg_monthly_balance": float, "transaction_count": int
    },
    "income_breakdown": [{"category": "string", "amount": float, "percentage": float}],
    "expense_breakdown": [{"category": "string", "amount": float, "percentage": float}],
    "monthly_trend": [{"month": "string", "credits": float, "debits": float, "net": float}],
    "health_score": int,
    "health_label": "string",
    "working_capital": {
        "current": float, "required": float, "gap": float,
        "credit_recommended": float, "emi_estimate": float, "tenure_months": int
    },
    "ai_insights": ["string"],
    "credit_verdict": "string",
    "credit_verdict_reason": "string"
}"""

        prompt = f"""Company: {company_name}

Bank Statement Data:
{statement_text[:8000]}

Analyze the above bank statement and return complete structured JSON as specified."""

        result = await self.generate_json(prompt, system_instruction)
        if result and isinstance(result, dict) and "summary" in result:
            result["company_name"] = result.get("company_name", company_name)
            return result

        # Fallback to mock data
        from services.groq_merchant_analysis import _mock_analysis
        return _mock_analysis(company_name)

    # ── Travel Tips (replaces groq_travel_service tips) ────────────────────────

    async def get_travel_tips(self, destination: str, issues: list) -> list:
        """Generate personalized travel financial tips using Gemini."""
        issue_text = "\n".join([
            f"- {i.get('label', '')}: {i.get('current_value', '')}"
            for i in issues if i.get("status") == "ISSUE"
        ])
        if not issue_text:
            return ["All systems clear — enjoy your trip!", "Keep PAISA installed abroad for emergency payments."]

        system_instruction = "You are PAISA. Generate 3 concise, actionable financial tips for an Indian traveller. Reply with ONLY a JSON array of 3 strings. No markdown."
        prompt = f"Destination: {destination}\nIssues found:\n{issue_text}\n\nGive 3 personalized pre-departure financial tips."

        raw = await self.generate(prompt, system_instruction)
        if raw:
            try:
                clean = raw.strip()
                for fence in ["```json", "```JSON", "```"]:
                    if clean.startswith(fence):
                        clean = clean[len(fence):]
                clean = clean.rstrip("```").strip()
                tips = json.loads(clean)
                if isinstance(tips, list):
                    return tips
            except Exception:
                pass

        return [
            f"Enable international transactions on your primary card before departing for {destination}.",
            "Load at least ₹50,000 equivalent in forex 2 weeks before travel.",
            "Set up PAISA emergency virtual card — activates in under 60 seconds if your card fails."
        ]

    # ── Salary Affordability (replaces groq_travel_service affordability) ──────

    async def analyze_salary_affordability(self, salary_text: str, destination: str, trip_cost: float) -> dict:
        """Gemini-powered salary affordability analysis."""
        system_instruction = """You are PAISA, an expert Indian personal finance AI.
Analyze the salary slip data and give a structured affordability assessment.
You MUST respond with ONLY valid JSON — no markdown, no explanation outside JSON.

Required JSON format:
{
  "net_salary": 60000,
  "monthly_expenses_detected": 32000,
  "monthly_surplus": 28000,
  "trip_cost": 80000,
  "months_to_save": 6,
  "monthly_saving_required": 13334,
  "affordability": "YES" | "STRETCH" | "NO",
  "ai_tips": ["string"],
  "emi_option": {
    "available": true,
    "monthly_emi": 7500,
    "tenure_months": 6,
    "provider": "HDFC Bank / Pine Labs Affordability"
  }
}"""

        prompt = f"""Salary slip data:
{salary_text}

Trip details:
- Destination: {destination}
- Estimated total trip cost: ₹{trip_cost:,.0f}

Analyze affordability and suggest a realistic savings + EMI plan."""

        result = await self.generate_json(prompt, system_instruction)
        if result and "net_salary" in result:
            return result

        from services.groq_travel_service import _mock_affordability
        return _mock_affordability(destination, trip_cost)

    # ── Trip Budget (replaces groq_travel_service budget) ─────────────────────

    async def plan_trip_budget(self, destination: str, duration_days: int, trip_budget: float) -> dict:
        """Gemini-powered trip budget planning."""
        system_instruction = """You are PAISA, expert Indian travel financial planner.
Generate a realistic itemized trip budget for an Indian traveller.
Respond with ONLY valid JSON — no markdown.

Required format:
{
  "destination": "string",
  "duration_days": int,
  "total_budget": int,
  "breakdown": [{"category": "string", "amount": int, "tip": "string"}],
  "currency_note": "string",
  "paisa_tip": "string"
}"""

        prompt = f"""Plan a detailed trip budget:
- Destination: {destination}
- Duration: {duration_days} days
- Total budget available: ₹{trip_budget:,.0f}
- Traveller profile: Indian, middle-income"""

        result = await self.generate_json(prompt, system_instruction)
        if result and "breakdown" in result:
            return result

        from services.groq_travel_service import _mock_budget
        return _mock_budget(destination, duration_days, trip_budget)

    # ── Health Check ──────────────────────────────────────────────────────────

    async def test_connection(self) -> dict:
        """Quick connectivity test for Gemini."""
        if not self.is_available:
            return {"status": "not_configured", "detail": "GOOGLE_API_KEY not set"}
        try:
            text = await self.generate("Say PAISA_GEMINI_OK in exactly those words.")
            return {
                "status": "connected",
                "response": text,
                "model": settings.GEMINI_MODEL,
                "provider": "Google Gemini"
            }
        except Exception as e:
            return {"status": "error", "detail": str(e)}


# Singleton instance
gemini_service = GeminiService()

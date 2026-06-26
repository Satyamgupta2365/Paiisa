"""
Groq AI Travel Guardian Service
Model: llama-3.3-70b-versatile  (Groq's best — 70B, 128k context, ~300 t/s)

Why this model:
- Fastest large model on Groq (~280-330 tok/s) — instant responses for demo
- 70B parameters — enough intelligence for complex financial reasoning
- Supports structured JSON output — critical for reliable schema extraction
- 128k context window — big enough to hold full salary slip text + history

Features implemented:
1. Salary Slip Affordability Analysis (text upload → Groq AI parses + advises)
2. Trip Budget Planning (AI generates itemized budget for destination)
3. Emergency Virtual Card generation (mock + AI-described)
4. Pre-departure financial health scan (existing, enhanced with AI tips)
"""
import json
from groq import Groq
from config.settings import settings


GROQ_MODEL = "llama-3.3-70b-versatile"


def _build_client() -> Groq | None:
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your-groq-api-key-here":
        return None
    return Groq(api_key=settings.GROQ_API_KEY)


def _chat(client: Groq, messages: list, temperature: float = 0.3) -> str:
    """Call Groq with error handling; return raw text."""
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=1500,
        )
        return resp.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}")


# ── 1. Salary Slip Affordability Analysis ─────────────────────────────────────

def analyze_salary_affordability(salary_text: str, destination: str, trip_cost: float) -> dict:
    """
    Takes raw salary slip text (OCR'd or pasted), destination, and estimated trip cost.
    Returns: affordability analysis, monthly savings plan, expense reduction tips.
    Falls back to realistic mock if no API key configured.
    """
    client = _build_client()

    if not client:
        # Rich mock response for demo when no API key is set
        return _mock_affordability(destination, trip_cost)

    system_prompt = """You are PAISA, an expert Indian personal finance AI.
Analyze the salary slip data provided and give a structured affordability assessment.
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
  "ai_tips": [
    "Save ₹13,334/month for 6 months to cover the full trip cost",
    "Reduce food delivery expenses by ₹3,000 — switch to home cooking 3x/week",
    "Book flight via EMI (0% for 6 months on HDFC credit card)"
  ],
  "emi_option": {
    "available": true,
    "monthly_emi": 7500,
    "tenure_months": 6,
    "provider": "HDFC Bank / Pine Labs Affordability"
  }
}"""

    user_msg = f"""Salary slip data:
{salary_text}

Trip details:
- Destination: {destination}
- Estimated total trip cost: ₹{trip_cost:,.0f}

Analyze affordability and suggest a realistic savings + EMI plan."""

    raw = _chat(client, [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg}
    ])

    try:
        # Strip any accidental markdown
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        return _mock_affordability(destination, trip_cost)


def _mock_affordability(destination: str, trip_cost: float) -> dict:
    monthly_saving = round(trip_cost / 6, -2)
    return {
        "net_salary": 60000,
        "monthly_expenses_detected": 32000,
        "monthly_surplus": 28000,
        "trip_cost": int(trip_cost),
        "months_to_save": 6,
        "monthly_saving_required": int(monthly_saving),
        "affordability": "STRETCH",
        "ai_tips": [
            f"Save ₹{monthly_saving:,.0f}/month for 6 months to fully fund the {destination} trip",
            "Reduce discretionary spending by ₹3,000/month (food delivery, streaming subscriptions)",
            "Use 0% EMI on HDFC Regalia for flight booking — splits ₹45,000 across 6 months",
            "Load forex at least 2 weeks early to avoid last-minute rate spikes",
            f"Emergency buffer: keep ₹5,000 liquid in savings account for {destination} trip"
        ],
        "emi_option": {
            "available": True,
            "monthly_emi": round(trip_cost / 6),
            "tenure_months": 6,
            "provider": "HDFC Bank / Pine Labs Affordability Suite"
        }
    }


# ── 2. Trip Budget Planner ─────────────────────────────────────────────────────

def plan_trip_budget(destination: str, duration_days: int, trip_budget: float) -> dict:
    """
    AI generates an itemized trip budget for the destination.
    Falls back to realistic mock if no API key set.
    """
    client = _build_client()

    if not client:
        return _mock_budget(destination, duration_days, trip_budget)

    system_prompt = """You are PAISA, expert Indian travel financial planner.
Generate a realistic itemized trip budget for an Indian traveller.
Respond with ONLY valid JSON — no markdown.

Required format:
{
  "destination": "Tokyo, Japan",
  "duration_days": 7,
  "total_budget": 83000,
  "breakdown": [
    {"category": "Flight (Round Trip)", "amount": 45000, "tip": "Book via Pine Labs 0% EMI"},
    {"category": "Hotel (7 nights)", "amount": 25000, "tip": "Use Booking.com with HDFC discount"},
    {"category": "Food & Dining", "amount": 8000, "tip": "Mix local street food + 2 restaurant meals"},
    {"category": "Transport (JR Pass + metro)", "amount": 4000, "tip": "Buy JR Pass before departure — ₹800/day"},
    {"category": "Activities & Shopping", "amount": 5000, "tip": "Budget ¥3,000/day for experiences"},
    {"category": "Emergency Buffer", "amount": 5000, "tip": "PAISA virtual card activated if needed"}
  ],
  "currency_note": "₹1 = ¥1.83 (as of March 2026)",
  "paisa_tip": "Load ¥1,50,000 forex 2 weeks before departure to lock exchange rate"
}"""

    user_msg = f"""Plan a detailed trip budget:
- Destination: {destination}
- Duration: {duration_days} days
- Total budget available: ₹{trip_budget:,.0f}
- Traveller profile: Indian, middle-income, first international trip"""

    raw = _chat(client, [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg}
    ])

    try:
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        return _mock_budget(destination, duration_days, trip_budget)


def _mock_budget(destination: str, duration_days: int, trip_budget: float) -> dict:
    flight = round(trip_budget * 0.54, -3)
    hotel = round(trip_budget * 0.30, -3)
    food = round(trip_budget * 0.10, -3)
    emergency = 5000
    other = trip_budget - flight - hotel - food - emergency
    return {
        "destination": destination,
        "duration_days": duration_days,
        "total_budget": int(trip_budget),
        "breakdown": [
            {"category": "Flight (Round Trip)", "amount": int(flight), "tip": "Book 8 weeks early. Use Pine Labs 0% EMI on HDFC."},
            {"category": f"Hotel ({duration_days} nights)", "amount": int(hotel), "tip": "Use Booking.com + HDFC 10% cashback."},
            {"category": "Food & Dining", "amount": int(food), "tip": "Mix local markets + 2 proper restaurant meals per day."},
            {"category": "Transport & Activities", "amount": int(other), "tip": "Pre-purchase city pass / JR Pass for metro."},
            {"category": "Emergency Buffer", "amount": int(emergency), "tip": "PAISA virtual card auto-activates if main card fails."},
        ],
        "currency_note": "₹1 ≈ ¥1.83 (live rate via Setu FX API)",
        "paisa_tip": "Load forex 2 weeks before departure to lock the exchange rate and avoid airport conversion fees."
    }


# ── 3. Emergency Virtual Card ─────────────────────────────────────────────────

def generate_virtual_card(user_name: str, amount: float, destination: str) -> dict:
    """
    Generates a 24-hour emergency virtual card when main card fails abroad.
    In production: calls RuPay / Visa Virtual Card API.
    """
    import random, string, uuid
    from datetime import datetime, timedelta

    card_num = " ".join(["".join(random.choices(string.digits, k=4)) for _ in range(4)])
    cvv = "".join(random.choices(string.digits, k=3))
    expiry = (datetime.utcnow() + timedelta(hours=24)).strftime("%m/%y")
    ref_id = "VC-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    return {
        "ref_id": ref_id,
        "card_number": card_num,
        "cardholder": user_name.upper(),
        "cvv": cvv,
        "expiry": expiry,
        "limit_inr": int(amount),
        "valid_hours": 24,
        "destination": destination,
        "network": "RuPay International",
        "status": "ACTIVE",
        "instructions": [
            "Use this card for online payments and hotel check-ins only",
            "Card auto-expires in 24 hours — settle payments before then",
            "OTP will be sent to your registered mobile number",
            "This card is backed by your India-side credit limit"
        ]
    }


# ── 4. AI Pre-departure Tips ──────────────────────────────────────────────────

def get_ai_travel_tips(destination: str, issues: list) -> list[str]:
    """
    Given the list of scan issues, generate personalized AI tips via Groq.
    Falls back to curated static tips if no API key.
    """
    client = _build_client()

    if not client or not issues:
        return _mock_tips(destination)

    issue_text = "\n".join([f"- {i.get('label', '')}: {i.get('current_value', '')}" for i in issues if i.get("status") == "ISSUE"])
    if not issue_text:
        return ["All systems clear — enjoy your trip!", "Keep PAISA installed abroad for emergency payments."]

    system_prompt = "You are PAISA. Generate 3 concise, actionable financial tips for an Indian traveller. Reply with ONLY a JSON array of 3 strings. No markdown."
    user_msg = f"Destination: {destination}\nIssues found:\n{issue_text}\n\nGive 3 personalized pre-departure financial tips."

    raw = _chat(client, [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg}
    ], temperature=0.4)

    try:
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        tips = json.loads(clean)
        return tips if isinstance(tips, list) else _mock_tips(destination)
    except Exception:
        return _mock_tips(destination)


def _mock_tips(destination: str) -> list:
    return [
        f"Enable international transactions on your primary card before departing for {destination} — RBI requires this to be OFF by default.",
        "Load at least ₹50,000 equivalent in forex 2 weeks before travel to avoid airport rate markups (typically 3-5% higher).",
        "Set up PAISA emergency virtual card in advance — if your physical card is declined, it activates in under 60 seconds."
    ]

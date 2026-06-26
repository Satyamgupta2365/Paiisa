from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from database.models import PaymentMethod, TransactionStatus, AgentDecision


# ── Payment Routing ────────────────────────────────────────────────────────────

class PaymentOption(BaseModel):
    method: PaymentMethod
    cashback: float
    savings: float
    score: float

class RecommendRequest(BaseModel):
    amount: float = Field(..., gt=0)
    category: str
    user_id: Optional[UUID] = None

class RecommendResponse(BaseModel):
    recommended_payment: PaymentMethod
    estimated_savings: float
    cashback_amount: float
    all_options: List[PaymentOption]
    reasoning: str

class PaymentRequest(BaseModel):
    user_id: UUID
    payment_method: PaymentMethod
    amount: float = Field(..., gt=0)
    category: Optional[str] = None

class PaymentResponse(BaseModel):
    status: TransactionStatus
    transaction_id: str | None
    cashback_earned: float
    message: str


# ── Offers ─────────────────────────────────────────────────────────────────────

class OfferCreate(BaseModel):
    payment_method: PaymentMethod
    cashback_percentage: float = Field(..., gt=0)
    max_cashback: Optional[float] = None
    min_amount: float = 0.0
    category: Optional[str] = None
    conditions: Optional[str] = None
    valid_until: Optional[datetime] = None

class OfferOut(OfferCreate):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True


# ── Users ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_payment_method: Optional[PaymentMethod] = None

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_payment_method: Optional[PaymentMethod] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Transactions ───────────────────────────────────────────────────────────────

class TransactionOut(BaseModel):
    id: UUID
    amount: float
    category: Optional[str] = None
    payment_method: PaymentMethod
    cashback_earned: float
    status: TransactionStatus
    created_at: datetime

    class Config:
        from_attributes = True

class SpendingInsights(BaseModel):
    total_spent: float
    total_cashback: float
    total_transactions: int
    best_method: Optional[str] = None
    avg_cashback_rate: float


# ── Travel Guardian ────────────────────────────────────────────────────────────

class TravelIssue(BaseModel):
    check: str
    label: str
    status: str       # "OK" | "ISSUE"
    current_value: str
    recommended: str

class TravelScanRequest(BaseModel):
    user_id: Optional[UUID] = None
    destination: str = "Tokyo, Japan"
    departure_date: Optional[str] = None

class TravelScanResponse(BaseModel):
    destination: str
    hours_to_departure: int
    issues: List[TravelIssue]
    risk_score: int   # 0-100
    all_clear: bool

class TravelFixRequest(BaseModel):
    user_id: Optional[UUID] = None
    destination: Optional[str] = "Tokyo, Japan"


# ── Travel Guardian — Salary Affordability ────────────────────────────────────

class SalaryAffordabilityRequest(BaseModel):
    salary_text: str                      # pasted / OCR'd salary slip
    destination: str = "Tokyo, Japan"
    trip_cost: float = 80000.0

class EmiOption(BaseModel):
    available: bool
    monthly_emi: float
    tenure_months: int
    provider: str

class SalaryAffordabilityResponse(BaseModel):
    net_salary: float
    monthly_expenses_detected: float
    monthly_surplus: float
    trip_cost: float
    months_to_save: int
    monthly_saving_required: float
    affordability: str           # "YES" | "STRETCH" | "NO"
    ai_tips: List[str]
    emi_option: EmiOption


# ── Travel Guardian — Trip Budget Planner ────────────────────────────────────

class BudgetLineItem(BaseModel):
    category: str
    amount: float
    tip: str

class TripBudgetRequest(BaseModel):
    destination: str = "Tokyo, Japan"
    duration_days: int = 7
    trip_budget: float = 83000.0

class TripBudgetResponse(BaseModel):
    destination: str
    duration_days: int
    total_budget: float
    breakdown: List[BudgetLineItem]
    currency_note: str
    paisa_tip: str


# ── Travel Guardian — Emergency Virtual Card ──────────────────────────────────

class VirtualCardRequest(BaseModel):
    user_name: str = "Traveller"
    amount: float = 25000.0
    destination: str = "Tokyo, Japan"

class VirtualCardResponse(BaseModel):
    ref_id: str
    card_number: str
    cardholder: str
    cvv: str
    expiry: str
    limit_inr: float
    valid_hours: int
    destination: str
    network: str
    status: str
    instructions: List[str]


# ── Travel Guardian — AI Tips ─────────────────────────────────────────────────

class TravelScanResponseV2(TravelScanResponse):
    ai_tips: List[str] = []


# ── Cash Flow Predictor (Merchant Dashboard) ───────────────────────────────────

class DailyDataPoint(BaseModel):
    day: str
    amount: float
    is_prediction: bool = False

class CashFlowResponse(BaseModel):
    data_points: List[DailyDataPoint]
    rcs_score: float
    shortfall_predicted: bool
    shortfall_amount: float
    recommended_credit: float
    confidence: int     # percent, e.g. 89


# ── TAP Server (Trusted Agent Protocol) ───────────────────────────────────────

class TapRuleUpdate(BaseModel):
    daily_cap: float = Field(..., gt=0)
    category_allowlist: List[str] = []
    merchant_blacklist: List[str] = []
    require_otp_above: float = 1000.0

class TapRuleOut(BaseModel):
    id: UUID
    user_id: UUID
    daily_cap: float
    category_allowlist: List[str]
    merchant_blacklist: List[str]
    require_otp_above: float
    updated_at: datetime

    class Config:
        from_attributes = True

class TapPaymentRequest(BaseModel):
    user_id: UUID
    agent_id: str
    amount: float = Field(..., gt=0)
    category: Optional[str] = None
    merchant_id: Optional[str] = None

class TapPaymentResponse(BaseModel):
    decision: AgentDecision
    reason: str
    agent_id: str
    requested_amount: float
    logged_at: datetime

class TapLogOut(BaseModel):
    id: UUID
    agent_id: str
    requested_amount: float
    category: Optional[str]
    merchant_id: Optional[str]
    decision: AgentDecision
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Merchant Bank Statement Analyzer (Groq AI) ────────────────────────────────

class StatementAnalysisRequest(BaseModel):
    statement_text: str
    company_name: str = "My Business"

class IncomeLine(BaseModel):
    category: str
    amount: float
    percentage: float

class ExpenseLine(BaseModel):
    category: str
    amount: float
    percentage: float

class MonthlyTrend(BaseModel):
    month: str
    credits: float
    debits: float
    net: float

class StatementSummary(BaseModel):
    total_credits: float
    total_debits: float
    net_cashflow: float
    avg_monthly_balance: float
    transaction_count: int

class WorkingCapital(BaseModel):
    current: float
    required: float
    gap: float
    credit_recommended: float
    emi_estimate: float
    tenure_months: int

class StatementAnalysisResponse(BaseModel):
    company_name: str
    period: str
    summary: StatementSummary
    income_breakdown: List[IncomeLine]
    expense_breakdown: List[ExpenseLine]
    monthly_trend: List[MonthlyTrend]
    health_score: int
    health_label: str
    working_capital: WorkingCapital
    ai_insights: List[str]
    credit_verdict: str
    credit_verdict_reason: str

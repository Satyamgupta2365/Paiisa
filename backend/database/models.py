from sqlalchemy import String, Float, DateTime, Boolean, Text, ForeignKey, Enum as SAEnum, Uuid as SA_Uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
import enum
import uuid
import json
from datetime import datetime
from .db import Base

class PaymentMethod(str, enum.Enum):
    UPI = "UPI"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    WALLET = "Wallet"
    NET_BANKING = "Net Banking"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

class AgentDecision(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    preferred_payment_method: Mapped[PaymentMethod | None] = mapped_column(SAEnum(PaymentMethod, name="paymentmethod"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="user")
    agent_rule   = relationship("AgentRule", back_populates="user", uselist=False)
    agent_logs   = relationship("AgentDecisionLog", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), ForeignKey("users.id"), index=True)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(SAEnum(PaymentMethod, name="paymentmethod"))
    cashback_earned: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[TransactionStatus] = mapped_column(SAEnum(TransactionStatus, name="transactionstatus"), default=TransactionStatus.PENDING)
    pine_labs_txn_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

class Offer(Base):
    __tablename__ = "offers"
    
    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_method: Mapped[PaymentMethod] = mapped_column(SAEnum(PaymentMethod, name="paymentmethod"))
    cashback_percentage: Mapped[float] = mapped_column(Float)
    max_cashback: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_amount: Mapped[float] = mapped_column(Float, default=0.0)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    conditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    valid_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def applies_to(self, amount: float, category: str) -> bool:
        if not self.is_active:
            return False
        if amount < self.min_amount:
            return False
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return False
        if self.category and self.category.lower() != category.lower():
            return False
        return True

    def calculate_cashback(self, amount: float) -> float:
        cashback = amount * (self.cashback_percentage / 100.0)
        if self.max_cashback is not None:
            cashback = min(cashback, self.max_cashback)
        return cashback


# ── PAISA New Models ───────────────────────────────────────────────────────────

class AgentRule(Base):
    """Financial constitution: what AI agents can and cannot spend on behalf of this user."""
    __tablename__ = "agent_rules"

    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    daily_cap: Mapped[float] = mapped_column(Float, default=5000.0)
    category_allowlist: Mapped[str] = mapped_column(Text, default='["food","transport","utilities"]')
    merchant_blacklist: Mapped[str] = mapped_column(Text, default='[]')
    require_otp_above: Mapped[float] = mapped_column(Float, default=1000.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="agent_rule")

    def get_allowlist(self) -> list:
        try:
            return json.loads(self.category_allowlist or "[]")
        except Exception:
            return []

    def get_blacklist(self) -> list:
        try:
            return json.loads(self.merchant_blacklist or "[]")
        except Exception:
            return []


class AgentDecisionLog(Base):
    """Immutable audit trail of every AI agent spending request."""
    __tablename__ = "agent_decision_logs"

    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), ForeignKey("users.id"), index=True)
    agent_id: Mapped[str] = mapped_column(String(100))
    requested_amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    merchant_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    decision: Mapped[AgentDecision] = mapped_column(SAEnum(AgentDecision, name="agentdecision"))
    reason: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="agent_logs")


class StatementHistory(Base):
    """Saves every bank statement analysis the user runs."""
    __tablename__ = "statement_history"

    id: Mapped[uuid.UUID] = mapped_column(SA_Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(200))
    original_filename: Mapped[str | None] = mapped_column(String(300), nullable=True)
    file_format: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # saved file path on disk (relative to backend/uploads/)
    saved_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # full AI analysis result stored as JSON string
    analysis_json: Mapped[str] = mapped_column(Text)
    health_score: Mapped[int] = mapped_column(default=0)
    net_cashflow: Mapped[float] = mapped_column(Float, default=0.0)
    credit_verdict: Mapped[str] = mapped_column(String(30), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

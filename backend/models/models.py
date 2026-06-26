"""
PAISA — ORM Models (Users, Transactions, Offers, AgentRules, AgentDecisionLog)
"""

import uuid
import json
from datetime import datetime

from sqlalchemy import (
    Column, String, Float, DateTime, Boolean,
    ForeignKey, Text, Enum as SAEnum, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.db import Base
import enum


# ── Enums ─────────────────────────────────────────────────────────────────────

class PaymentMethod(str, enum.Enum):
    UPI         = "UPI"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD  = "Debit Card"
    WALLET      = "Wallet"
    NET_BANKING = "Net Banking"


class TransactionStatus(str, enum.Enum):
    PENDING   = "pending"
    SUCCESS   = "success"
    FAILED    = "failed"
    REFUNDED  = "refunded"


class AgentDecision(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# ── Models ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id                       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name                     = Column(String(120), nullable=False)
    email                    = Column(String(255), unique=True, nullable=False, index=True)
    phone                    = Column(String(20), nullable=True)
    preferred_payment_method = Column(SAEnum(PaymentMethod), nullable=True)
    created_at               = Column(DateTime, default=datetime.utcnow)

    transactions  = relationship("Transaction", back_populates="user", lazy="selectin")
    agent_rule    = relationship("AgentRule", back_populates="user", uselist=False, lazy="selectin")
    agent_logs    = relationship("AgentDecisionLog", back_populates="user", lazy="selectin")


class Transaction(Base):
    __tablename__ = "transactions"

    id                    = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id               = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount                = Column(Float, nullable=False)
    category              = Column(String(80), nullable=True)
    payment_method        = Column(SAEnum(PaymentMethod), nullable=False)
    cashback_earned       = Column(Float, default=0.0)
    status                = Column(SAEnum(TransactionStatus), default=TransactionStatus.PENDING)
    pine_labs_txn_id      = Column(String(100), nullable=True)
    ai_recommendation     = Column(Text, nullable=True)
    created_at            = Column(DateTime, default=datetime.utcnow)
    updated_at            = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="transactions")


class Offer(Base):
    __tablename__ = "offers"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_method      = Column(SAEnum(PaymentMethod), nullable=False)
    cashback_percentage = Column(Float, nullable=False)
    max_cashback        = Column(Float, nullable=True)
    min_amount          = Column(Float, default=0.0)
    category            = Column(String(80), nullable=True)
    conditions          = Column(Text, nullable=True)
    valid_until         = Column(DateTime, nullable=True)
    is_active           = Column(Boolean, default=True)

    def applies_to(self, amount: float, category: str | None) -> bool:
        if not self.is_active:
            return False
        if amount < self.min_amount:
            return False
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return False
        if self.category and category and self.category.lower() != category.lower():
            return False
        return True

    def calculate_cashback(self, amount: float) -> float:
        cashback = round(amount * self.cashback_percentage / 100, 2)
        if self.max_cashback:
            cashback = min(cashback, self.max_cashback)
        return cashback


class AgentRule(Base):
    """Stores a user's financial constitution for external AI agents (TAP Server)."""
    __tablename__ = "agent_rules"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id             = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    daily_cap           = Column(Float, default=5000.0)       # Max AI can spend per day (₹)
    category_allowlist  = Column(Text, default="[]")          # JSON list of allowed categories
    merchant_blacklist  = Column(Text, default="[]")          # JSON list of blocked merchants
    require_otp_above   = Column(Float, default=1000.0)       # Biometric check threshold
    created_at          = Column(DateTime, default=datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="agent_rule")

    def get_allowlist(self):
        try:
            return json.loads(self.category_allowlist or "[]")
        except Exception:
            return []

    def get_blacklist(self):
        try:
            return json.loads(self.merchant_blacklist or "[]")
        except Exception:
            return []


class AgentDecisionLog(Base):
    """Immutable audit trail of every AI agent spending request."""
    __tablename__ = "agent_decision_logs"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    agent_id        = Column(String(100), nullable=False)     # e.g. "claude-v3", "gemini-1.5"
    requested_amount= Column(Float, nullable=False)
    category        = Column(String(80), nullable=True)
    merchant_id     = Column(String(100), nullable=True)
    decision        = Column(SAEnum(AgentDecision), nullable=False)
    reason          = Column(String(200), nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="agent_logs")

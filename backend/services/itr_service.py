"""
PAISA ITR Service — Tax Aggregation & Computation Engine
Aggregates data from: Transactions, StatementHistory, AgentDecisionLogs
Computes: Old Regime / New Regime / Sec 44AD Presumptive Tax
"""
import json
from sqlalchemy import select, func
from database.models import Transaction, StatementHistory, AgentDecisionLog, TransactionStatus, AgentDecision
from datetime import datetime


class ItrService:

    # ── Tax Slab Calculators ──────────────────────────────────────────────────

    def calculate_new_regime_tax(self, taxable_income: float) -> float:
        """
        FY 2025-26 / AY 2026-27 New Tax Regime slabs:
          0 – 4,00,000      → 0%
          4,00,001 – 8,00,000 → 5%
          8,00,001 – 12,00,000 → 10%
          12,00,001 – 16,00,000 → 15%
          16,00,001 – 20,00,000 → 20%
          > 20,00,000       → 30%
        Sec 87A: Full rebate if taxable income ≤ ₹12,00,000
        """
        if taxable_income <= 0:
            return 0.0
        if taxable_income <= 400_000:
            return 0.0

        tax = 0.0
        if taxable_income > 400_000:
            tax += min(taxable_income - 400_000, 400_000) * 0.05
        if taxable_income > 800_000:
            tax += min(taxable_income - 800_000, 400_000) * 0.10
        if taxable_income > 1_200_000:
            tax += min(taxable_income - 1_200_000, 400_000) * 0.15
        if taxable_income > 1_600_000:
            tax += min(taxable_income - 1_600_000, 400_000) * 0.20
        if taxable_income > 2_000_000:
            tax += (taxable_income - 2_000_000) * 0.30

        # Sec 87A full rebate for income ≤ ₹12 Lakh
        if taxable_income <= 1_200_000:
            return 0.0

        return round(tax, 2)

    def calculate_old_regime_tax(self, taxable_income: float) -> float:
        """
        Old Tax Regime slabs:
          0 – 2,50,000    → 0%
          2,50,001 – 5,00,000 → 5%
          5,00,001 – 10,00,000 → 20%
          > 10,00,000     → 30%
        Sec 87A: Full rebate if taxable income ≤ ₹5,00,000
        """
        if taxable_income <= 0:
            return 0.0
        if taxable_income <= 250_000:
            return 0.0

        tax = 0.0
        if taxable_income > 250_000:
            tax += min(taxable_income - 250_000, 250_000) * 0.05
        if taxable_income > 500_000:
            tax += min(taxable_income - 500_000, 500_000) * 0.20
        if taxable_income > 1_000_000:
            tax += (taxable_income - 1_000_000) * 0.30

        # Sec 87A rebate
        if taxable_income <= 500_000:
            return 0.0

        return round(tax, 2)

    # ── Comparative Tax Calculator ────────────────────────────────────────────

    def calculate_itr(
        self,
        gross_revenue: float,
        business_expenses: float,
        other_income: float = 0.0,
        deductions_80c: float = 150_000.0,
        deductions_80d: float = 25_000.0,
        apply_presumptive_44ad: bool = False
    ) -> dict:
        """
        Comparative ITR computation: Old Regime vs New Regime
        Also calculates Sec 44AD presumptive tax (6% of digital turnover).
        """
        # 1. Net profit under normal books (Sec 28)
        normal_profit = max(0.0, gross_revenue - business_expenses)

        # 2. Presumptive profit under Sec 44AD (6% digital turnover)
        presumptive_profit = gross_revenue * 0.06 if apply_presumptive_44ad else normal_profit
        declared_business_income = presumptive_profit if apply_presumptive_44ad else normal_profit

        # 3. Gross Total Income
        gti = declared_business_income + other_income

        # ── NEW REGIME ───────────────────────────────────────────────────────
        new_regime_deductions = 0.0  # Chapter VI-A deductions disallowed
        new_taxable_income = max(0.0, gti - new_regime_deductions)
        new_raw_tax = self.calculate_new_regime_tax(new_taxable_income)
        new_cess = round(new_raw_tax * 0.04, 2)
        new_total_tax = round(new_raw_tax + new_cess, 2)

        # ── OLD REGIME ───────────────────────────────────────────────────────
        old_regime_deductions = min(deductions_80c, 150_000.0) + min(deductions_80d, 25_000.0)
        old_taxable_income = max(0.0, gti - old_regime_deductions)
        old_raw_tax = self.calculate_old_regime_tax(old_taxable_income)
        old_cess = round(old_raw_tax * 0.04, 2)
        old_total_tax = round(old_raw_tax + old_cess, 2)

        # ── RECOMMENDATION ───────────────────────────────────────────────────
        optimal_regime = "New" if new_total_tax <= old_total_tax else "Old"
        tax_saved = round(abs(old_total_tax - new_total_tax), 2)
        best_tax = new_total_tax if optimal_regime == "New" else old_total_tax

        if apply_presumptive_44ad:
            sec44_note = (
                "Section 44AD presumptive taxation at 6% digital rate is applied. "
                "You declare ₹{:,.0f} as net taxable income — no audit books required.".format(presumptive_profit)
            )
        else:
            sec44_note = "Normal accounting (Sec 28) is applied. Full audited books must be maintained."

        return {
            "business_income_type": "Presumptive (Sec 44AD — 6% Digital)" if apply_presumptive_44ad else "Normal Accounting (Sec 28)",
            "gross_revenue": round(gross_revenue, 2),
            "business_expenses": round(business_expenses, 2),
            "normal_profit": round(normal_profit, 2),
            "presumptive_profit_44ad": round(presumptive_profit, 2),
            "declared_business_income": round(declared_business_income, 2),
            "other_income": round(other_income, 2),
            "gross_total_income": round(gti, 2),
            "new_regime": {
                "label": "New Tax Regime (FY 2025-26)",
                "deductions_applied": 0.0,
                "taxable_income": round(new_taxable_income, 2),
                "raw_tax": round(new_raw_tax, 2),
                "cess": round(new_cess, 2),
                "total_tax": round(new_total_tax, 2),
                "is_optimal": optimal_regime == "New",
            },
            "old_regime": {
                "label": "Old Tax Regime (with deductions)",
                "deductions_applied": round(old_regime_deductions, 2),
                "taxable_income": round(old_taxable_income, 2),
                "raw_tax": round(old_raw_tax, 2),
                "cess": round(old_cess, 2),
                "total_tax": round(old_total_tax, 2),
                "is_optimal": optimal_regime == "Old",
            },
            "recommendation": {
                "optimal_regime": optimal_regime,
                "tax_liability": round(best_tax, 2),
                "tax_saved": round(tax_saved, 2),
                "effective_tax_rate": round((best_tax / gti * 100) if gti > 0 else 0.0, 2),
                "sec44ad_note": sec44_note,
                "guidance": (
                    f"Choose the {optimal_regime.upper()} TAX REGIME. "
                    f"You save ₹{tax_saved:,.2f} vs the alternative regime. "
                    + sec44_note
                ),
            },
        }

    # ── Data Aggregator ───────────────────────────────────────────────────────

    async def aggregate_tax_data(self, user_id: str, db) -> dict:
        """
        Pull live data from the PAISA platform for ITR aggregation:
        1. StatementHistory — latest bank statement (credits/debits)
        2. Transactions — user's Pine Labs digital transaction volume
        3. AgentDecisionLog — approved AI agent spending (tech expense deductions)
        """
        # ── Sensible defaults (Satyam demo data) ────────────────────────────
        gross_revenue = 64_426.54
        business_expenses = 58_391.35
        agent_expenses = 0.0
        data_source = "demo_defaults"
        statement_company = "Demo Business"
        statement_period = "FY 2025-26"
        transaction_count = 0
        tap_log_count = 0

        # ── 1. Latest bank statement analysis ───────────────────────────────
        try:
            stmt_q = await db.execute(
                select(StatementHistory)
                .order_by(StatementHistory.created_at.desc())
                .limit(1)
            )
            stmt = stmt_q.scalar_one_or_none()
            if stmt:
                analysis = json.loads(stmt.analysis_json or "{}")
                summary = analysis.get("summary", {})
                if summary.get("total_credits", 0) > 0:
                    gross_revenue = float(summary.get("total_credits", gross_revenue))
                    business_expenses = float(summary.get("total_debits", business_expenses))
                    data_source = "statement_history"
                    statement_company = stmt.company_name
        except Exception as e:
            print(f"[ITR] Statement query warning: {e}")

        # ── 2. User digital transaction volume ──────────────────────────────
        try:
            tx_q = await db.execute(
                select(func.sum(Transaction.amount), func.count(Transaction.id))
                .where(Transaction.status == TransactionStatus.SUCCESS)
            )
            tx_row = tx_q.one_or_none()
            if tx_row and tx_row[0]:
                tx_total = float(tx_row[0])
                transaction_count = int(tx_row[1] or 0)
                # Pine Labs digital turnover supplements/overrides bank data
                if tx_total > 0:
                    gross_revenue = max(gross_revenue, tx_total)
                    if data_source == "demo_defaults":
                        data_source = "pine_labs_transactions"
        except Exception as e:
            print(f"[ITR] Transaction query warning: {e}")

        # ── 3. TAP approved AI agent expenditures ───────────────────────────
        try:
            tap_q = await db.execute(
                select(func.sum(AgentDecisionLog.requested_amount), func.count(AgentDecisionLog.id))
                .where(AgentDecisionLog.decision == AgentDecision.APPROVED)
            )
            tap_row = tap_q.one_or_none()
            if tap_row and tap_row[0]:
                agent_expenses = float(tap_row[0])
                tap_log_count = int(tap_row[1] or 0)
        except Exception as e:
            print(f"[ITR] TAP logs query warning: {e}")

        total_expenses = business_expenses + agent_expenses
        net_profit = max(0.0, gross_revenue - total_expenses)
        profit_margin = round((net_profit / gross_revenue * 100) if gross_revenue > 0 else 0.0, 2)

        return {
            "gross_revenue": round(gross_revenue, 2),
            "operating_expenses": round(business_expenses, 2),
            "ai_agent_expenses": round(agent_expenses, 2),
            "total_expenses": round(total_expenses, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin_pct": profit_margin,
            "digital_turnover_pct": 100.0,
            "transaction_count": transaction_count,
            "tap_log_count": tap_log_count,
            "data_source": data_source,
            "statement_company": statement_company,
            "assessment_year": "2026-27",
            "financial_year": "2025-26",
        }


itr_service = ItrService()

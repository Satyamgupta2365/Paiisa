import json
from sqlalchemy import select
from database.models import Transaction, StatementHistory, AgentDecisionLog
from datetime import datetime

class ItrService:
    def calculate_new_regime_tax(self, taxable_income: float) -> float:
        """
        Calculate income tax under the New Tax Regime (FY 2025-26 / 2026-27)
        Slabs:
          - Up to ₹4,00,000: Nil
          - ₹4,00,001 to ₹8,00,000: 5%
          - ₹8,00,001 to ₹12,00,000: 10%
          - ₹12,00,001 to ₹16,00,000: 15%
          - ₹16,00,001 to ₹20,00,000: 20%
          - Above ₹20,00,000: 30%
        Rebate: S.87A provides 100% tax rebate if taxable income <= ₹12,00,000.
        """
        if taxable_income <= 0:
            return 0.0
        
        # Calculate raw tax based on slabs
        tax = 0.0
        
        # Slab 1: Up to 4L
        if taxable_income <= 400000:
            return 0.0
        
        # Slab 2: 4L to 8L (5%)
        if taxable_income > 400000:
            tax += min(taxable_income - 400000, 400000) * 0.05
            
        # Slab 3: 8L to 12L (10%)
        if taxable_income > 800000:
            tax += min(taxable_income - 800000, 400000) * 0.10
            
        # Slab 4: 12L to 16L (15%)
        if taxable_income > 1200000:
            tax += min(taxable_income - 1200000, 400000) * 0.15
            
        # Slab 5: 16L to 20L (20%)
        if taxable_income > 1600000:
            tax += min(taxable_income - 1600000, 400000) * 0.20
            
        # Slab 6: Above 20L (30%)
        if taxable_income > 2000000:
            tax += (taxable_income - 2000000) * 0.30
            
        # Rebate under Section 87A (effective up to ₹12,00,000 taxable income)
        if taxable_income <= 1200000:
            return 0.0
            
        return round(tax, 2)

    def calculate_old_regime_tax(self, taxable_income: float) -> float:
        """
        Calculate income tax under the Old Tax Regime
        Slabs:
          - Up to ₹2,50,000: Nil
          - ₹2,50,001 to ₹5,00,000: 5%
          - ₹5,00,001 to ₹10,00,000: 20%
          - Above ₹10,00,000: 30%
        Rebate: S.87A provides 100% tax rebate if taxable income <= ₹5,00,000.
        """
        if taxable_income <= 0:
            return 0.0
            
        tax = 0.0
        
        # Slab 1: Up to 2.5L
        if taxable_income <= 250000:
            return 0.0
            
        # Slab 2: 2.5L to 5L (5%)
        if taxable_income > 250000:
            tax += min(taxable_income - 250000, 250000) * 0.05
            
        # Slab 3: 5L to 10L (20%)
        if taxable_income > 500000:
            tax += min(taxable_income - 500000, 500000) * 0.20
            
        # Slab 4: Above 10L (30%)
        if taxable_income > 1000000:
            tax += (taxable_income - 1000000) * 0.30
            
        # Rebate under Section 87A (effective up to ₹5,00,000 taxable income)
        if taxable_income <= 500000:
            return 0.0
            
        return round(tax, 2)

    def calculate_itr(
        self,
        gross_revenue: float,
        business_expenses: float,
        other_income: float = 0.0,
        deductions_80c: float = 150000.0,
        deductions_80d: float = 25000.0,
        apply_presumptive_44ad: bool = False
    ) -> dict:
        """
        Performs comparative tax calculation under Old & New regimes,
        including normal accounting vs Presumptive S.44AD (6% digital profit).
        """
        # 1. Net Profit under Normal Accounting
        normal_profit = max(0.0, gross_revenue - business_expenses)
        
        # 2. Net Profit under Presumptive Section 44AD (6% of gross digital turnover)
        presumptive_profit = gross_revenue * 0.06 if apply_presumptive_44ad else normal_profit
        
        declared_business_income = presumptive_profit if apply_presumptive_44ad else normal_profit
        
        # Total Income before deductions
        gti = declared_business_income + other_income
        
        # --- NEW REGIME CALCULATION ---
        # Deductions are generally NOT allowed in New Regime, except Standard Deduction (if salaried, which is ₹75k)
        new_regime_deductions = 0.0
        new_taxable_income = max(0.0, gti - new_regime_deductions)
        new_raw_tax = self.calculate_new_regime_tax(new_taxable_income)
        new_cess = round(new_raw_tax * 0.04, 2)
        new_total_tax = new_raw_tax + new_cess
        
        # --- OLD REGIME CALCULATION ---
        # Deductions are allowed in Old Regime (80C, 80D, etc.)
        old_regime_deductions = min(deductions_80c, 150000.0) + min(deductions_80d, 25000.0)
        old_taxable_income = max(0.0, gti - old_regime_deductions)
        old_raw_tax = self.calculate_old_regime_tax(old_taxable_income)
        old_cess = round(old_raw_tax * 0.04, 2)
        old_total_tax = old_raw_tax + old_cess
        
        # Recommend the lower tax option
        optimal_regime = "New" if new_total_tax <= old_total_tax else "Old"
        tax_saved = abs(old_total_tax - new_total_tax)
        
        return {
            "business_income_type": "Presumptive (Sec 44AD)" if apply_presumptive_44ad else "Normal Accounting (Sec 28)",
            "normal_profit": round(normal_profit, 2),
            "declared_business_income": round(declared_business_income, 2),
            "other_income": round(other_income, 2),
            "gross_total_income": round(gti, 2),
            "new_regime": {
                "taxable_income": round(new_taxable_income, 2),
                "raw_tax": round(new_raw_tax, 2),
                "cess": round(new_cess, 2),
                "total_tax": round(new_total_tax, 2),
            },
            "old_regime": {
                "deductions_applied": round(old_regime_deductions, 2),
                "taxable_income": round(old_taxable_income, 2),
                "raw_tax": round(old_raw_tax, 2),
                "cess": round(old_cess, 2),
                "total_tax": round(old_total_tax, 2),
            },
            "recommendation": {
                "optimal_regime": optimal_regime,
                "tax_liability": round(new_total_tax if optimal_regime == "New" else old_total_tax, 2),
                "tax_saved": round(tax_saved, 2),
                "guidance": (
                    f"Choose the {optimal_regime.upper()} TAX REGIME. It saves you ₹{tax_saved:,.2f} in tax. "
                    + ("By utilizing Section 44AD presumptive taxation at 6% for digital payments, you also do not need to maintain detailed balance sheets or audits." if apply_presumptive_44ad else "Normal audit filing is recommended.")
                )
            }
        }

    async def aggregate_tax_data(self, user_id: str, db) -> dict:
        """
        Queries other parts of the system to gather tax-related numbers:
        1. Queries statement history for latest uploads (income/expenses).
        2. Queries transactions for Pine Labs POS volumes.
        3. Queries TAP logs for agent spending to deduct as tech/operating expenses.
        """
        # Default mock values in case database is empty
        gross_revenue = 64426.54  # Default Credits from satyam statement
        business_expenses = 58391.35  # Default Debits from satyam statement
        agent_expenses = 0.0
        
        # 1. Read latest statement analysis
        try:
            stmt_result = await db.execute(
                select(StatementHistory).order_by(StatementHistory.created_at.desc()).limit(1)
            )
            stmt = stmt_result.scalar_one_or_none()
            if stmt:
                analysis = json.loads(stmt.analysis_json)
                summary = analysis.get("summary", {})
                gross_revenue = summary.get("total_credits", gross_revenue)
                business_expenses = summary.get("total_debits", business_expenses)
        except Exception as e:
            print(f"Error querying statement history for ITR: {e}")

        # 2. Read success transactions (add to digital revenue)
        try:
            tx_result = await db.execute(
                select(Transaction).where(Transaction.status == "success")
            )
            txs = tx_result.scalars().all()
            if txs:
                # Add digital payments to gross revenue
                tx_sum = sum(t.amount for t in txs)
                # If transactions exist, we use them to build/augment gross revenue
                gross_revenue = max(gross_revenue, tx_sum)
        except Exception as e:
            print(f"Error querying transactions for ITR: {e}")

        # 3. Read TAP logs (approved expenditures by AI agents)
        try:
            tap_result = await db.execute(
                select(AgentDecisionLog).where(AgentDecisionLog.decision == "APPROVED")
            )
            logs = tap_result.scalars().all()
            agent_expenses = sum(log.requested_amount for log in logs)
        except Exception as e:
            print(f"Error querying TAP logs for ITR: {e}")

        # Agent expenditures are tax-deductible software/service expenses
        total_expenses = business_expenses + agent_expenses

        return {
            "gross_revenue": round(gross_revenue, 2),
            "operating_expenses": round(business_expenses, 2),
            "ai_agent_expenses": round(agent_expenses, 2),
            "total_expenses": round(total_expenses, 2),
            "digital_turnover_pct": 100.0  # our platform tracks digital transactions
        }

itr_service = ItrService()

"""
Travel Guardian Service
Simulates a 48-hour pre-departure scan of a traveller's financial instruments.
In production this would call card issuer APIs via RBI AA Framework (Setu SDK).
For simulation and local development, uses rich mock data that demonstrates the full scenario.
"""
from models.schemas import TravelIssue, TravelScanResponse


class TravelGuardianService:

    def scan(self, destination: str = "Tokyo, Japan", user_id=None) -> TravelScanResponse:
        """Run the 48-hour pre-departure financial health check."""
        issues = [
            TravelIssue(
                check="card_international_status",
                label="HDFC Regalia — International Transactions",
                status="ISSUE",
                current_value="DISABLED",
                recommended="Must be enabled for international card swipes. RBI mandate: off by default."
            ),
            TravelIssue(
                check="forex_balance",
                label="Forex Balance (JPY / USD)",
                status="ISSUE",
                current_value="₹0 loaded",
                recommended="Load minimum ₹50,000 equivalent for 7-day trip to Tokyo."
            ),
            TravelIssue(
                check="credit_limit",
                label="Credit Limit vs. Estimated Trip Spend",
                status="OK",
                current_value="₹3,20,000 available",
                recommended="Sufficient for estimated ₹1,10,000 trip expenditure."
            ),
            TravelIssue(
                check="travel_insurance",
                label="International Travel Insurance",
                status="ISSUE",
                current_value="No active policy",
                recommended="Required for medical emergencies and flight cancellations abroad."
            ),
        ]

        open_issues = [i for i in issues if i.status == "ISSUE"]
        risk_score = min(100, len(open_issues) * 30)

        return TravelScanResponse(
            destination=destination,
            hours_to_departure=48,
            issues=issues,
            risk_score=risk_score,
            all_clear=(len(open_issues) == 0)
        )

    def get_resolved(self, destination: str = "Tokyo, Japan") -> TravelScanResponse:
        """Return the same scan with all issues resolved (post-fix state)."""
        issues = [
            TravelIssue(
                check="card_international_status",
                label="HDFC Regalia — International Transactions",
                status="OK",
                current_value="ENABLED",
                recommended="Active for this trip."
            ),
            TravelIssue(
                check="forex_balance",
                label="Forex Balance (JPY / USD)",
                status="OK",
                current_value="¥150,000 loaded (≈ ₹82,000)",
                recommended="Sufficient for 7-day itinerary."
            ),
            TravelIssue(
                check="credit_limit",
                label="Credit Limit vs. Estimated Trip Spend",
                status="OK",
                current_value="₹3,20,000 available",
                recommended="Sufficient."
            ),
            TravelIssue(
                check="travel_insurance",
                label="International Travel Insurance",
                status="OK",
                current_value="Policy XYZ-9934 active (7 days)",
                recommended="Coverage: ₹50L medical + ₹5L trip cancellation."
            ),
        ]
        return TravelScanResponse(
            destination=destination,
            hours_to_departure=47,
            issues=issues,
            risk_score=0,
            all_clear=True
        )


travel_service = TravelGuardianService()

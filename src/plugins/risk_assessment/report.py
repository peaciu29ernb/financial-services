"""Risk assessment report generation module.

Provides functionality to format and export risk assessment results
into structured reports suitable for financial advisors and clients.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json

from .calculator import RiskProfile, RiskLevel, calculate_risk_score


@dataclass
class RiskReport:
    """Structured risk assessment report."""

    profile: RiskProfile
    score: float
    risk_level: RiskLevel
    generated_at: datetime = field(default_factory=datetime.utcnow)
    flags: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize the report to a dictionary."""
        return {
            "generated_at": self.generated_at.isoformat() + "Z",
            "risk_level": self.risk_level.value,
            "score": round(self.score, 4),
            "profile": {
                "investment_horizon_years": self.profile.investment_horizon_years,
                "volatility_tolerance": self.profile.volatility_tolerance,
                "liquidity_ratio": self.profile.liquidity_ratio,
                "debt_to_equity": self.profile.debt_to_equity,
                "asset_concentration": self.profile.asset_concentration,
            },
            "flags": self.flags,
            "recommendations": self.recommendations,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize the report to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_text(self) -> str:
        """Format the report as a human-readable text summary."""
        lines = [
            "=" * 52,
            "        RISK ASSESSMENT REPORT",
            "=" * 52,
            f"Generated : {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')} UTC",
            f"Risk Level: {self.risk_level.value.upper()}",
            f"Score     : {self.score:.4f}",
            "",
            "--- Portfolio Profile ---",
            f"  Investment Horizon : {self.profile.investment_horizon_years} years",
            f"  Volatility Tolerance: {self.profile.volatility_tolerance:.2f}",
            f"  Liquidity Ratio    : {self.profile.liquidity_ratio:.2f}",
            f"  Debt-to-Equity     : {self.profile.debt_to_equity:.2f}",
            f"  Asset Concentration: {self.profile.asset_concentration:.2f}",
        ]

        if self.flags:
            lines.append("")
            lines.append("--- Risk Flags ---")
            for flag in self.flags:
                lines.append(f"  ⚠  {flag}")

        if self.recommendations:
            lines.append("")
            lines.append("--- Recommendations ---")
            for rec in self.recommendations:
                lines.append(f"  •  {rec}")

        lines.append("=" * 52)
        return "\n".join(lines)


_RECOMMENDATIONS: dict[RiskLevel, list[str]] = {
    RiskLevel.LOW: [
        "Portfolio is well-positioned for stable, long-term growth.",
        "Consider periodic rebalancing to maintain target allocation.",
    ],
    RiskLevel.MEDIUM: [
        "Review asset concentration to improve diversification.",
        "Monitor liquidity ratios quarterly.",
    ],
    RiskLevel.HIGH: [
        "Reduce debt-to-equity ratio to below 1.5 where possible.",
        "Increase liquid asset holdings to cover at least 6 months of obligations.",
        "Consult a financial advisor before making large position changes.",
    ],
    RiskLevel.CRITICAL: [
        "Immediate review with a senior risk officer is strongly advised.",
        "Halt new leveraged positions until risk score falls below HIGH threshold.",
        "Evaluate emergency liquidity facilities and credit lines.",
    ],
}


def generate_report(
    profile: RiskProfile,
    flags: Optional[list[str]] = None,
) -> RiskReport:
    """Generate a complete risk report for the given profile.

    Args:
        profile: The client or portfolio risk profile to assess.
        flags: Optional list of pre-computed risk flags. If None,
               flags are derived automatically from the profile.

    Returns:
        A populated RiskReport instance ready for export.
    """
    score, level, computed_flags = calculate_risk_score(profile)

    resolved_flags = flags if flags is not None else computed_flags
    recommendations = _RECOMMENDATIONS.get(level, [])

    return RiskReport(
        profile=profile,
        score=score,
        risk_level=level,
        flags=resolved_flags,
        recommendations=recommendations,
    )

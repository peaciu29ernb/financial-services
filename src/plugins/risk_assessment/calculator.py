"""Risk assessment calculator for financial services plugin."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskProfile:
    score: float
    level: RiskLevel
    factors: list[str]
    recommendation: str


def calculate_risk_score(
    portfolio_volatility: float,
    debt_to_equity: float,
    liquidity_ratio: float,
    market_exposure: float,
    credit_score: Optional[int] = None,
) -> RiskProfile:
    """Calculate a composite risk score based on financial indicators.

    Args:
        portfolio_volatility: Annualized volatility (0.0 - 1.0)
        debt_to_equity: Debt-to-equity ratio
        liquidity_ratio: Current ratio (current assets / current liabilities)
        market_exposure: Percentage of assets in volatile markets (0.0 - 1.0)
        credit_score: Optional FICO-style credit score (300 - 850)

    Returns:
        RiskProfile with computed score, level, contributing factors, and recommendation.
    """
    factors = []
    score = 0.0

    # Volatility contribution (weight: 30%)
    vol_component = min(portfolio_volatility, 1.0) * 30
    score += vol_component
    if portfolio_volatility > 0.4:
        factors.append(f"High portfolio volatility ({portfolio_volatility:.1%})")

    # Debt-to-equity contribution (weight: 25%)
    de_normalized = min(debt_to_equity / 5.0, 1.0)
    score += de_normalized * 25
    if debt_to_equity > 2.0:
        factors.append(f"Elevated debt-to-equity ratio ({debt_to_equity:.2f})")

    # Liquidity contribution (weight: 25%, inverse — lower is riskier)
    liq_risk = max(0.0, 1.0 - (liquidity_ratio / 3.0))
    score += liq_risk * 25
    if liquidity_ratio < 1.0:
        factors.append(f"Poor liquidity ratio ({liquidity_ratio:.2f})")

    # Market exposure contribution (weight: 20%)
    score += min(market_exposure, 1.0) * 20
    if market_exposure > 0.6:
        factors.append(f"High market exposure ({market_exposure:.1%})")

    # Credit score adjustment (optional, up to ±10 points)
    if credit_score is not None:
        credit_adjustment = ((850 - credit_score) / 550) * 10
        score += credit_adjustment
        if credit_score < 620:
            factors.append(f"Low credit score ({credit_score})")

    score = round(min(max(score, 0.0), 100.0), 2)

    if score < 25:
        level = RiskLevel.LOW
        recommendation = "Portfolio appears well-balanced. Maintain current strategy."
    elif score < 50:
        level = RiskLevel.MEDIUM
        recommendation = "Consider rebalancing to reduce identified risk factors."
    elif score < 75:
        level = RiskLevel.HIGH
        recommendation = "Significant risk detected. Immediate review recommended."
    else:
        level = RiskLevel.CRITICAL
        recommendation = "Critical risk level. Escalate to senior risk officer immediately."

    return RiskProfile(score=score, level=level, factors=factors, recommendation=recommendation)

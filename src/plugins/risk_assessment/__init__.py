"""
Risk Assessment Plugin for Claude Financial Services.

This plugin provides tools for evaluating financial risk profiles,
calculating risk scores, and flagging high-risk indicators such as
poor liquidity or high volatility.

Usage:
    from src.plugins.risk_assessment import calculate_risk_score, RiskProfile, RiskLevel

    profile = RiskProfile(
        asset_value=500000.0,
        volatility_index=0.25,
        liquidity_ratio=1.8,
        debt_to_equity=0.6,
        market_exposure=0.4,
    )
    result = calculate_risk_score(profile)
    print(result.level, result.score)
"""

from .calculator import (
    RiskLevel,
    RiskProfile,
    calculate_risk_score,
)

__all__ = [
    "RiskLevel",
    "RiskProfile",
    "calculate_risk_score",
]

__version__ = "0.1.0"
__author__ = "Anthropic Financial Services Team"

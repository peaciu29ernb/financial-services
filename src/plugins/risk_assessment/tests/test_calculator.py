"""Unit tests for the risk assessment calculator."""

import pytest
from src.plugins.risk_assessment.calculator import (
    RiskLevel,
    RiskProfile,
    calculate_risk_score,
)


class TestCalculateRiskScore:
    def test_low_risk_profile(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.05,
            debt_to_equity=0.3,
            liquidity_ratio=3.0,
            market_exposure=0.1,
            credit_score=800,
        )
        assert isinstance(profile, RiskProfile)
        assert profile.level == RiskLevel.LOW
        assert profile.score < 25
        assert len(profile.factors) == 0

    def test_critical_risk_profile(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.9,
            debt_to_equity=4.5,
            liquidity_ratio=0.5,
            market_exposure=0.95,
            credit_score=310,
        )
        assert profile.level == RiskLevel.CRITICAL
        assert profile.score >= 75
        assert len(profile.factors) > 0

    def test_high_volatility_flagged(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.55,
            debt_to_equity=1.0,
            liquidity_ratio=2.0,
            market_exposure=0.3,
        )
        assert any("volatility" in f.lower() for f in profile.factors)

    def test_poor_liquidity_flagged(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.1,
            debt_to_equity=0.5,
            liquidity_ratio=0.8,
            market_exposure=0.2,
        )
        assert any("liquidity" in f.lower() for f in profile.factors)

    def test_score_clamped_between_0_and_100(self):
        profile = calculate_risk_score(
            portfolio_volatility=10.0,
            debt_to_equity=100.0,
            liquidity_ratio=0.0,
            market_exposure=10.0,
            credit_score=300,
        )
        assert 0.0 <= profile.score <= 100.0

    def test_without_credit_score(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.2,
            debt_to_equity=1.0,
            liquidity_ratio=1.5,
            market_exposure=0.3,
        )
        assert profile.score is not None
        assert profile.level in list(RiskLevel)

    def test_medium_risk_recommendation_contains_rebalancing(self):
        profile = calculate_risk_score(
            portfolio_volatility=0.3,
            debt_to_equity=1.8,
            liquidity_ratio=1.2,
            market_exposure=0.45,
        )
        if profile.level == RiskLevel.MEDIUM:
            assert "rebalancing" in profile.recommendation.lower()

    # NOTE: Added boundary credit scores (299, 851) to catch off-by-one edge
    # cases at the min/max limits of the valid credit score range.
    @pytest.mark.parametrize("credit_score", [299, 300, 500, 620, 750, 850, 851])
    def test_various_credit_scores_produce_valid_profiles(self, credit_score):
        profile = calculate_risk_score(
            portfolio_volatility=0.2,
            debt_to_equity=1.0,
            liquidity_ratio=1.5,
            market_exposure=0.3,
            credit_score=credit_score,
        )
        assert isinstance(profile, RiskProfile)
        assert profile.level in list(RiskLevel)
        # Score should always be a valid number regardless of credit score input
        assert 0.0 <= profile.score <= 100.0

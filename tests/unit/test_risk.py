"""Unit tests for risk engine."""

import pytest
from afi.core.risk import (
    RiskProfile,
    RiskEngine,
    RiskLevel,
    TimeHorizon,
    PortfolioRiskMetrics,
    PositionRiskMetrics,
)


class TestRiskProfile:
    """Tests for risk profile."""

    def test_maximum_risk_budget(self):
        """Test maximum risk budget calculation."""
        profile = RiskProfile(
            capital=500.0,
            risk_tolerance=0.10,
            time_horizon_days=7,
        )
        assert profile.maximum_risk_budget == pytest.approx(50.0)

    def test_investable_capital(self):
        """Test investable capital after emergency fund."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            emergency_fund=3000.0,
        )
        assert profile.investable_capital == pytest.approx(7000.0)

    def test_monthly_surplus(self):
        """Test monthly surplus calculation."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            income_monthly=5000.0,
            expenses_monthly=2000.0,
        )
        assert profile.monthly_surplus == pytest.approx(3000.0)

    def test_is_liquid(self):
        """Test liquidity check."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            emergency_fund=12000.0,
            expenses_monthly=2000.0,
        )
        assert profile.is_liquid is True


class TestRiskEngine:
    """Tests for risk engine."""

    def test_validate_risk_profile_valid(self):
        """Test valid risk profile validation."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            emergency_fund=12000.0,
            income_monthly=5000.0,
            expenses_monthly=2000.0,
        )
        engine = RiskEngine()
        is_valid, warnings = engine.validate_risk_profile(profile)

        assert is_valid is True
        assert len(warnings) == 0

    def test_validate_risk_profile_zero_capital(self):
        """Test validation with zero capital."""
        profile = RiskProfile(
            capital=0.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
        )
        engine = RiskEngine()
        is_valid, warnings = engine.validate_risk_profile(profile)

        assert is_valid is False

    def test_calculate_maximum_position_size(self):
        """Test maximum position size calculation."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            emergency_fund=2000.0,
        )
        engine = RiskEngine()
        size = engine.calculate_maximum_position_size(
            profile, position_risk_amount=500.0
        )

        assert size == pytest.approx(500.0)

    def test_check_position_concentration(self):
        """Test position concentration check."""
        engine = RiskEngine()
        is_allowed, reason = engine.check_position_concentration(
            portfolio_value=10000.0, new_position_value=1500.0, max_single_position=0.20
        )

        assert is_allowed is True

    def test_check_position_concentration_violation(self):
        """Test concentration limit violation."""
        engine = RiskEngine()
        is_allowed, reason = engine.check_position_concentration(
            portfolio_value=10000.0, new_position_value=3000.0, max_single_position=0.20
        )

        assert is_allowed is False

    def test_calculate_scenario_analysis(self):
        """Test scenario analysis."""
        engine = RiskEngine()
        scenarios = engine.calculate_scenario_analysis(
            entry_price=10.0, current_price=10.5, volatility=0.20
        )

        assert "bull" in scenarios
        assert "base" in scenarios
        assert "bear" in scenarios
        assert scenarios["bull"]["probability"] == 0.25
        assert scenarios["base"]["probability"] == 0.50
        assert scenarios["bear"]["probability"] == 0.25

    def test_stress_test_portfolio(self):
        """Test portfolio stress testing."""
        position = PositionRiskMetrics(
            position_size=1000.0,
            entry_price=10.0,
            current_price=10.5,
            volatility=0.20,
        )
        metrics = PortfolioRiskMetrics(
            total_value=10000.0,
            positions={"HRHO": position},
            cash=9000.0,
        )
        engine = RiskEngine()
        stress = engine.stress_test_portfolio(metrics, market_shock=-0.20)

        assert "shock_scenario" in stress
        assert "total_loss" in stress
        assert stress["total_loss"] > 0

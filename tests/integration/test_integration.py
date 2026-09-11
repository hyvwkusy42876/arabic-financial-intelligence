"""Integration tests."""

import pytest
from datetime import datetime, timedelta
from afi.core.portfolio import Portfolio
from afi.core.risk import RiskProfile, RiskEngine
from afi.engines.backtesting import BacktestEngine


class TestPortfolioRiskIntegration:
    """Test integration between portfolio and risk management."""

    def test_portfolio_with_risk_checks(self):
        """Test portfolio operations with risk validation."""
        profile = RiskProfile(
            capital=10000.0,
            risk_tolerance=0.05,
            time_horizon_days=365,
            emergency_fund=2000.0,
        )
        engine = RiskEngine()
        is_valid, warnings = engine.validate_risk_profile(profile)

        assert is_valid is True

        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=profile.investable_capital,
        )
        portfolio.add_position("HRHO", quantity=100.0, entry_price=8.25)

        assert portfolio.total_position_value > 0

    def test_position_sizing_for_risk(self):
        """Test position sizing based on risk profile."""
        profile = RiskProfile(
            capital=500.0,
            risk_tolerance=0.10,
            time_horizon_days=7,
        )
        engine = RiskEngine()
        max_risk_budget = profile.maximum_risk_budget  # 50 EGP
        max_size = engine.calculate_maximum_position_size(profile, max_risk_budget)

        assert max_size <= profile.investable_capital

"""Unit tests for financial calculations."""

import pytest
from afi.core.calculator import (
    PortfolioCalculator,
    RiskCalculator,
    FeeCalculator,
    DecimalCalculator,
    PositionMetrics,
)


class TestPortfolioCalculator:
    """Tests for portfolio-level calculations."""

    def test_calculate_allocation(self):
        """Test allocation calculation."""
        positions = {"HRHO": 5000.0, "EFID": 3000.0, "EMCO": 2000.0}
        allocation = PortfolioCalculator.calculate_allocation(positions)

        assert allocation["HRHO"] == pytest.approx(50.0)
        assert allocation["EFID"] == pytest.approx(30.0)
        assert allocation["EMCO"] == pytest.approx(20.0)

    def test_calculate_portfolio_return(self):
        """Test portfolio return calculation."""
        current = 11000.0
        initial = 10000.0
        ret = PortfolioCalculator.calculate_portfolio_return(current, initial)

        assert ret == pytest.approx(10.0)

    def test_calculate_cagr(self):
        """Test CAGR calculation."""
        cagr = PortfolioCalculator.calculate_cagr(
            starting_value=10000.0, ending_value=15000.0, years=2.0
        )

        assert cagr == pytest.approx(22.47, rel=0.01)

    def test_calculate_volatility(self):
        """Test volatility calculation."""
        returns = [0.01, -0.02, 0.015, 0.025, -0.01]
        vol = PortfolioCalculator.calculate_volatility(returns)

        assert vol > 0  # Should be positive

    def test_calculate_max_drawdown(self):
        """Test max drawdown calculation."""
        values = [10000, 11000, 9500, 10500, 9000, 12000]
        dd = PortfolioCalculator.calculate_max_drawdown(values)

        assert dd == pytest.approx(18.18, rel=0.01)


class TestRiskCalculator:
    """Tests for risk calculations."""

    def test_calculate_position_size(self):
        """Test position sizing."""
        size = RiskCalculator.calculate_position_size(
            capital=10000.0,
            risk_per_trade=500.0,
            entry_price=10.0,
            stop_loss=9.0,
        )

        assert size == pytest.approx(500.0)

    def test_calculate_value_at_risk(self):
        """Test VaR calculation."""
        var = RiskCalculator.calculate_value_at_risk(
            position_value=10000.0, volatility=20.0, confidence_level=0.95
        )

        assert var > 0


class TestFeeCalculator:
    """Tests for fee calculations."""

    def test_calculate_commission(self):
        """Test commission calculation."""
        comm = FeeCalculator.calculate_commission(
            trade_value=10000.0, commission_rate=0.001
        )

        assert comm == pytest.approx(10.0)

    def test_calculate_total_cost(self):
        """Test total cost with fees."""
        total, effective = FeeCalculator.calculate_total_cost(
            quantity=100.0, price=10.0, commission_rate=0.001, slippage_rate=0.001
        )

        assert total == pytest.approx(1002.0)
        assert effective == pytest.approx(10.02)


class TestPositionMetrics:
    """Tests for position metrics."""

    def test_current_value(self):
        """Test current value calculation."""
        metrics = PositionMetrics(
            quantity=100.0, entry_price=10.0, current_price=12.0
        )
        assert metrics.current_value == 1200.0

    def test_unrealized_pl(self):
        """Test unrealized P&L calculation."""
        metrics = PositionMetrics(
            quantity=100.0, entry_price=10.0, current_price=12.0, commission_paid=10.0
        )
        assert metrics.unrealized_pl == pytest.approx(190.0)

    def test_unrealized_pl_pct(self):
        """Test unrealized P&L percentage."""
        metrics = PositionMetrics(
            quantity=100.0, entry_price=10.0, current_price=12.0, commission_paid=10.0
        )
        assert metrics.unrealized_pl_pct == pytest.approx(18.81, rel=0.01)

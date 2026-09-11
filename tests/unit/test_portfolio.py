"""Unit tests for portfolio management."""

import pytest
from datetime import datetime
from afi.core.portfolio import Portfolio, Position, Transaction


class TestPortfolio:
    """Tests for portfolio functionality."""

    def test_total_value(self):
        """Test total portfolio value."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=5000.0,
        )
        portfolio.add_position("HRHO", quantity=100.0, entry_price=8.25)
        portfolio.positions["HRHO"].current_price = 9.0

        assert portfolio.total_position_value == pytest.approx(900.0)
        assert portfolio.total_value == pytest.approx(5900.0)

    def test_allocation(self):
        """Test portfolio allocation."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=5000.0,
        )
        portfolio.add_position("HRHO", quantity=100.0, entry_price=8.25)
        portfolio.add_position("EFID", quantity=100.0, entry_price=0.86)
        portfolio.positions["HRHO"].current_price = 8.25
        portfolio.positions["EFID"].current_price = 0.86

        allocation = portfolio.allocation
        total_pct = sum(allocation.values())
        assert total_pct == pytest.approx(100.0, rel=0.1)

    def test_add_position(self):
        """Test adding position."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=10000.0,
        )
        portfolio.add_position("HRHO", quantity=100.0, entry_price=8.25)

        assert "HRHO" in portfolio.positions
        assert portfolio.positions["HRHO"].quantity == 100.0

    def test_remove_position(self):
        """Test removing position."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=10000.0,
        )
        portfolio.add_position("HRHO", quantity=100.0, entry_price=8.25)
        portfolio.remove_position("HRHO")

        assert "HRHO" not in portfolio.positions

    def test_add_cash(self):
        """Test adding cash."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=5000.0,
        )
        portfolio.add_cash(2000.0)

        assert portfolio.cash == pytest.approx(7000.0)

    def test_withdraw_cash_success(self):
        """Test withdrawing cash."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=5000.0,
        )
        success = portfolio.withdraw_cash(2000.0)

        assert success is True
        assert portfolio.cash == pytest.approx(3000.0)

    def test_withdraw_cash_insufficient(self):
        """Test withdrawal with insufficient cash."""
        portfolio = Portfolio(
            portfolio_id="test-1",
            name="Test",
            cash=1000.0,
        )
        success = portfolio.withdraw_cash(2000.0)

        assert success is False
        assert portfolio.cash == pytest.approx(1000.0)


class TestPosition:
    """Tests for position functionality."""

    def test_entry_value(self):
        """Test entry value calculation."""
        position = Position(
            ticker="HRHO",
            quantity=100.0,
            average_entry_price=8.25,
            current_price=8.25,
            total_fees_paid=10.0,
        )
        assert position.entry_value == pytest.approx(835.0)

    def test_unrealized_pl(self):
        """Test unrealized P&L."""
        position = Position(
            ticker="HRHO",
            quantity=100.0,
            average_entry_price=8.25,
            current_price=9.0,
            total_fees_paid=0.0,
        )
        assert position.unrealized_pl == pytest.approx(75.0)

    def test_unrealized_pl_pct(self):
        """Test unrealized P&L percentage."""
        position = Position(
            ticker="HRHO",
            quantity=100.0,
            average_entry_price=8.25,
            current_price=9.0,
            total_fees_paid=0.0,
        )
        assert position.unrealized_pl_pct == pytest.approx(9.09, rel=0.01)

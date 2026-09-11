"""Test configuration and fixtures."""

import pytest
from datetime import datetime, timedelta
from afi.core.calculator import PortfolioCalculator, RiskCalculator, PositionMetrics
from afi.core.risk import RiskProfile, RiskEngine, PortfolioRiskMetrics, PositionRiskMetrics
from afi.core.portfolio import Portfolio, Position, Transaction
from afi.providers.mock import MockMarketDataProvider, MockNewsProvider, MockLLMProvider


@pytest.fixture
def mock_market_provider():
    """Provide mock market data provider."""
    return MockMarketDataProvider()


@pytest.fixture
def mock_news_provider():
    """Provide mock news provider."""
    return MockNewsProvider()


@pytest.fixture
def mock_llm_provider():
    """Provide mock LLM provider."""
    return MockLLMProvider()


@pytest.fixture
def risk_profile():
    """Provide test risk profile."""
    return RiskProfile(
        capital=500.0,
        risk_tolerance=0.10,
        time_horizon_days=7,
        emergency_fund=3000.0,
        income_monthly=5000.0,
        expenses_monthly=2000.0,
        investment_experience="beginner",
    )


@pytest.fixture
def test_portfolio():
    """Provide test portfolio."""
    portfolio = Portfolio(
        portfolio_id="test-portfolio-1",
        name="Test Portfolio",
        cash=10000.0,
        base_currency="EGP",
    )
    return portfolio


@pytest.fixture
def position_metrics():
    """Provide test position metrics."""
    return PositionMetrics(
        quantity=100.0,
        entry_price=10.0,
        current_price=12.0,
        commission_paid=10.0,
    )


@pytest.fixture
def risk_engine():
    """Provide risk engine."""
    return RiskEngine()

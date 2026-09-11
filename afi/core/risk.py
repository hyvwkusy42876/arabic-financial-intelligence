"""Deterministic risk engine.

All risk calculations are performed by deterministic software.
The LLM interprets and explains results but never overrides calculations.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class RiskLevel(Enum):
    """Risk tolerance levels."""

    VERY_LOW = 0.01  # 1%
    LOW = 0.03  # 3%
    MODERATE = 0.05  # 5%
    HIGH = 0.10  # 10%
    VERY_HIGH = 0.15  # 15%


class TimeHorizon(Enum):
    """Investment time horizons."""

    VERY_SHORT = 1  # Days
    SHORT = 30  # Days
    MEDIUM = 90  # Days
    LONG = 365  # Days
    VERY_LONG = 1825  # 5 years


@dataclass
class RiskProfile:
    """User financial risk profile."""

    capital: float
    risk_tolerance: float  # As decimal (0.05 = 5%)
    time_horizon_days: int
    emergency_fund: float = 0.0
    income_monthly: float = 0.0
    expenses_monthly: float = 0.0
    investment_experience: str = "beginner"  # beginner, intermediate, advanced
    risk_aversion: str = "moderate"  # conservative, moderate, aggressive

    @property
    def maximum_risk_budget(self) -> float:
        """Maximum amount that can be risked.

        Returns:
            Maximum amount at risk in capital units
        """
        return self.capital * self.risk_tolerance

    @property
    def investable_capital(self) -> float:
        """Capital available for investment after emergency fund.

        Returns:
            Investable amount
        """
        return max(0, self.capital - self.emergency_fund)

    @property
    def monthly_surplus(self) -> float:
        """Monthly surplus after expenses.

        Returns:
            Monthly amount available for investing
        """
        return max(0, self.income_monthly - self.expenses_monthly)

    @property
    def is_liquid(self) -> bool:
        """Check if investor has sufficient emergency fund.

        Returns:
            True if emergency fund >= 6 months expenses
        """
        required_emergency = self.expenses_monthly * 6
        return self.emergency_fund >= required_emergency


@dataclass
class PositionRiskMetrics:
    """Risk metrics for a single position."""

    position_size: float  # Amount invested
    entry_price: float
    current_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    volatility: float = 0.0  # Annualized, as decimal
    correlation: float = 0.0  # With portfolio

    @property
    def unrealized_loss_at_stop(self) -> float:
        """Unrealized loss if stop is hit.

        Returns:
            Loss amount
        """
        if self.stop_loss is None:
            return 0.0
        return self.position_size * (1 - (self.stop_loss / self.entry_price))

    @property
    def risk_reward_ratio(self) -> float:
        """Risk/reward ratio (if both stop and target set).

        Returns:
            Ratio (higher is better)
        """
        if self.stop_loss is None or self.take_profit is None:
            return 0.0

        risk = self.entry_price - self.stop_loss
        reward = self.take_profit - self.entry_price

        if risk <= 0:
            return 0.0

        return reward / risk

    @property
    def max_loss_percentage(self) -> float:
        """Maximum loss if stop is hit (as percentage).

        Returns:
            Percentage loss
        """
        if self.stop_loss is None:
            return 0.0
        return ((self.entry_price - self.stop_loss) / self.entry_price) * 100


@dataclass
class PortfolioRiskMetrics:
    """Risk metrics for entire portfolio."""

    total_value: float
    positions: dict[str, PositionRiskMetrics] = field(default_factory=dict)
    cash: float = 0.0
    max_single_position: float = 0.2  # 20%
    max_sector_exposure: float = 0.3  # 30%
    max_portfolio_risk: float = 0.05  # 5% of portfolio at risk

    @property
    def total_at_risk(self) -> float:
        """Total amount at risk across all positions.

        Returns:
            Total amount at risk
        """
        return sum(p.unrealized_loss_at_stop for p in self.positions.values())

    @property
    def portfolio_risk_percentage(self) -> float:
        """Total risk as percentage of portfolio.

        Returns:
            Percentage of portfolio at risk
        """
        if self.total_value <= 0:
            return 0.0
        return (self.total_at_risk / self.total_value) * 100

    @property
    def is_within_risk_limits(self) -> bool:
        """Check if portfolio is within acceptable risk limits.

        Returns:
            True if compliant
        """
        if self.portfolio_risk_percentage > self.max_portfolio_risk * 100:
            return False

        for position in self.positions.values():
            exposure = position.position_size / self.total_value if self.total_value > 0 else 0
            if exposure > self.max_single_position:
                return False

        return True

    @property
    def concentration_risk(self) -> float:
        """Measure of portfolio concentration (Herfindahl index).

        Returns:
            Concentration ratio (0-1, higher = more concentrated)
        """
        if self.total_value <= 0:
            return 0.0

        exposures = [
            (p.position_size / self.total_value) for p in self.positions.values()
        ]
        return sum(e**2 for e in exposures)


class RiskEngine:
    """Core deterministic risk engine.

    All calculations are deterministic and never influenced by LLM.
    The LLM can interpret results but not override them.
    """

    def __init__(self):
        """Initialize risk engine."""
        self.scenarios = []  # Historical scenarios for backtesting

    def validate_risk_profile(self, profile: RiskProfile) -> tuple[bool, list[str]]:
        """Validate a user's risk profile.

        Args:
            profile: User's risk profile

        Returns:
            (is_valid, list_of_warnings)
        """
        warnings = []

        if profile.capital <= 0:
            return False, ["رأس المال يجب أن يكون أكبر من صفر"]

        if profile.emergency_fund < profile.expenses_monthly * 3:
            warnings.append(
                "صندوق الطوارئ أقل من 3 أشهر من نفقاتك"
            )

        if profile.investment_experience == "beginner" and profile.risk_tolerance > 0.10:
            warnings.append(
                "المبتدئون لا يجب أن يأخذوا مخاطر عالية"
            )

        return True, warnings

    def calculate_maximum_position_size(
        self, profile: RiskProfile, position_risk_amount: float
    ) -> float:
        """Calculate maximum position size based on risk budget.

        Args:
            profile: User risk profile
            position_risk_amount: Amount willing to risk on this position

        Returns:
            Maximum capital to allocate to position
        """
        if position_risk_amount <= 0:
            return 0.0

        # Cannot risk more than 20% of portfolio in single position
        max_single = profile.investable_capital * 0.20
        position_size = min(position_risk_amount, max_single)

        # Cannot risk more than available capital
        position_size = min(position_size, profile.investable_capital)

        return position_size

    def check_position_concentration(
        self,
        portfolio_value: float,
        new_position_value: float,
        max_single_position: float = 0.20,
    ) -> tuple[bool, str]:
        """Check if new position violates concentration limits.

        Args:
            portfolio_value: Current portfolio value
            new_position_value: Value of new position
            max_single_position: Maximum allowed single position (0.20 = 20%)

        Returns:
            (is_allowed, reason)
        """
        if portfolio_value <= 0:
            return True, "محفظة فارغة"

        exposure = new_position_value / portfolio_value

        if exposure > max_single_position:
            return (
                False,
                f"الموضع سيشكل {exposure*100:.1f}% من المحفظة، الحد الأقصى {max_single_position*100:.0f}%",
            )

        return True, "OK"

    def calculate_scenario_analysis(
        self, entry_price: float, current_price: float, volatility: float
    ) -> dict:
        """Generate bull/base/bear scenarios.

        Args:
            entry_price: Entry price
            current_price: Current price
            volatility: Annualized volatility (as decimal)

        Returns:
            Scenario dictionary with prices and probabilities
        """
        # Use volatility and historical patterns for scenarios
        volatility_move = volatility * 0.5  # Half volatility for one-week scenarios

        return {
            "bull": {
                "price": current_price * (1 + volatility_move),
                "probability": 0.25,
                "description": "السيناريو الإيجابي",
            },
            "base": {
                "price": current_price,
                "probability": 0.50,
                "description": "السيناريو الأساسي",
            },
            "bear": {
                "price": current_price * (1 - volatility_move),
                "probability": 0.25,
                "description": "السيناريو السلبي",
            },
        }

    def calculate_expected_value(
        self, scenarios: dict, position_size: float
    ) -> float:
        """Calculate expected value across scenarios.

        Args:
            scenarios: Scenario dictionary with prices and probabilities
            position_size: Size of position

        Returns:
            Expected value
        """
        ev = 0.0
        for scenario in scenarios.values():
            ev += scenario["price"] * scenario["probability"] * position_size
        return ev

    def stress_test_portfolio(
        self,
        portfolio_metrics: PortfolioRiskMetrics,
        market_shock: float = -0.20,  # -20% market move
    ) -> dict:
        """Stress test portfolio against market shock.

        Args:
            portfolio_metrics: Portfolio risk metrics
            market_shock: Market movement (as decimal, -0.20 = -20%)

        Returns:
            Stress test results
        """
        total_loss = 0.0
        position_impacts = {}

        for ticker, position in portfolio_metrics.positions.items():
            # Shock impacts positions based on their beta-like correlation
            impact_factor = 1 + (market_shock * (1 + position.correlation))
            new_price = position.current_price * impact_factor
            position_loss = position.position_size * (1 - impact_factor)
            total_loss += position_loss
            position_impacts[ticker] = {
                "current_value": position.position_size,
                "stress_value": position.position_size * impact_factor,
                "loss": position_loss,
                "loss_pct": (position_loss / position.position_size * 100)
                if position.position_size > 0
                else 0,
            }

        return {
            "shock_scenario": f"{market_shock*100:.0f}% Market Move",
            "total_loss": total_loss,
            "portfolio_impact_pct": (
                (total_loss / portfolio_metrics.total_value * 100)
                if portfolio_metrics.total_value > 0
                else 0
            ),
            "position_impacts": position_impacts,
        }

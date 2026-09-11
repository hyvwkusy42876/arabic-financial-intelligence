"""Core financial calculations.

Deterministic P&L, fees, position sizing, and value calculations.
"""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal, ROUND_HALF_UP
import math


@dataclass
class PositionMetrics:
    """Metrics for a single position."""

    quantity: float
    entry_price: float
    current_price: float
    commission_paid: float = 0.0

    @property
    def current_value(self) -> float:
        """Current total value of position."""
        return self.quantity * self.current_price

    @property
    def entry_value(self) -> float:
        """Total entry value (including commission)."""
        return (self.quantity * self.entry_price) + self.commission_paid

    @property
    def unrealized_pl(self) -> float:
        """Unrealized profit/loss."""
        return self.current_value - self.entry_value

    @property
    def unrealized_pl_pct(self) -> float:
        """Unrealized P&L as percentage."""
        if self.entry_value <= 0:
            return 0.0
        return (self.unrealized_pl / self.entry_value) * 100

    @property
    def average_price(self) -> float:
        """Average price per share including commission."""
        if self.quantity <= 0:
            return 0.0
        return self.entry_value / self.quantity


class PortfolioCalculator:
    """Portfolio-level calculations."""

    @staticmethod
    def calculate_allocation(position_values: dict[str, float]) -> dict[str, float]:
        """Calculate allocation percentages.

        Args:
            position_values: {ticker: current_value}

        Returns:
            {ticker: allocation_percentage}
        """
        total_value = sum(position_values.values())
        if total_value <= 0:
            return {k: 0.0 for k in position_values}
        return {k: (v / total_value) * 100 for k, v in position_values.items()}

    @staticmethod
    def calculate_portfolio_return(
        current_value: float,
        initial_value: float,
        cash_additions: float = 0.0,
        cash_withdrawals: float = 0.0,
    ) -> float:
        """Calculate total portfolio return.

        Args:
            current_value: Current portfolio value
            initial_value: Initial portfolio value
            cash_additions: Total cash added
            cash_withdrawals: Total cash withdrawn

        Returns:
            Total return as percentage
        """
        adjusted_initial = initial_value + cash_additions - cash_withdrawals
        if adjusted_initial <= 0:
            return 0.0
        return ((current_value - adjusted_initial) / adjusted_initial) * 100

    @staticmethod
    def calculate_cagr(
        starting_value: float, ending_value: float, years: float
    ) -> float:
        """Calculate Compound Annual Growth Rate.

        Args:
            starting_value: Portfolio value at start
            ending_value: Portfolio value at end
            years: Time period in years

        Returns:
            CAGR as percentage
        """
        if starting_value <= 0 or years <= 0 or ending_value <= 0:
            return 0.0
        return ((ending_value / starting_value) ** (1 / years) - 1) * 100

    @staticmethod
    def calculate_volatility(returns: list[float]) -> float:
        """Calculate annualized volatility.

        Args:
            returns: List of period returns (as decimals)

        Returns:
            Annualized volatility as percentage
        """
        if len(returns) < 2:
            return 0.0

        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)

        # Annualize (assuming daily returns, 252 trading days)
        return std_dev * math.sqrt(252) * 100

    @staticmethod
    def calculate_sharpe_ratio(
        returns: list[float], risk_free_rate: float = 0.02
    ) -> float:
        """Calculate Sharpe ratio.

        Args:
            returns: List of period returns (as decimals)
            risk_free_rate: Annual risk-free rate

        Returns:
            Sharpe ratio
        """
        if len(returns) < 2:
            return 0.0

        mean_return = sum(returns) / len(returns) * 252  # Annualize
        volatility = PortfolioCalculator.calculate_volatility(returns)

        if volatility <= 0:
            return 0.0

        return (mean_return - risk_free_rate) / (volatility / 100)

    @staticmethod
    def calculate_max_drawdown(values: list[float]) -> float:
        """Calculate maximum drawdown.

        Args:
            values: List of portfolio values over time

        Returns:
            Maximum drawdown as percentage
        """
        if len(values) < 2:
            return 0.0

        peak = values[0]
        max_dd = 0.0

        for value in values[1:]:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak > 0 else 0
            max_dd = max(max_dd, drawdown)

        return max_dd * 100


class RiskCalculator:
    """Risk calculations for positions and portfolios."""

    @staticmethod
    def calculate_position_risk(
        capital: float, position_size: float, stop_loss: Optional[float] = None
    ) -> float:
        """Calculate risk amount for a position.

        Args:
            capital: Total capital available
            position_size: Size of position in capital
            stop_loss: Stop loss price (if applicable)

        Returns:
            Amount at risk in capital units
        """
        if stop_loss is not None:
            return position_size * (1 - stop_loss)
        return capital * 0.02  # Default: 2% risk per trade

    @staticmethod
    def calculate_position_size(
        capital: float, risk_per_trade: float, entry_price: float, stop_loss: float
    ) -> float:
        """Calculate position size based on risk management.

        Ensures risk is controlled to a specific amount.

        Args:
            capital: Total capital available
            risk_per_trade: Maximum amount to risk (in capital units)
            entry_price: Entry price of asset
            stop_loss: Stop loss price

        Returns:
            Shares/units to buy
        """
        if capital <= 0 or stop_loss >= entry_price:
            return 0.0

        price_risk = entry_price - stop_loss
        if price_risk <= 0:
            return 0.0

        position_size = risk_per_trade / price_risk
        max_position_value = capital * 0.20  # Max 20% in one position

        if position_size * entry_price > max_position_value:
            position_size = max_position_value / entry_price

        return position_size

    @staticmethod
    def calculate_portfolio_risk(
        positions: dict[str, PositionMetrics], portfolio_value: float
    ) -> dict[str, float]:
        """Calculate portfolio-level risk metrics.

        Args:
            positions: {ticker: PositionMetrics}
            portfolio_value: Total portfolio value

        Returns:
            Risk metrics dictionary
        """
        if portfolio_value <= 0:
            return {"concentration_ratio": 0.0, "max_single_exposure": 0.0}

        exposures = [
            (v.current_value / portfolio_value) for v in positions.values()
        ]
        max_exposure = max(exposures) if exposures else 0.0
        concentration = sum(e**2 for e in exposures)  # Herfindahl index

        return {"concentration_ratio": concentration, "max_single_exposure": max_exposure}

    @staticmethod
    def calculate_value_at_risk(
        position_value: float, volatility: float, confidence_level: float = 0.95
    ) -> float:
        """Calculate Value at Risk (VaR).

        Uses normal distribution approximation.

        Args:
            position_value: Position value
            volatility: Annualized volatility (as percentage)
            confidence_level: Confidence level (0.95 = 95%)

        Returns:
            VaR amount (potential loss)
        """
        # Approximate z-score for confidence levels
        z_scores = {0.90: 1.28, 0.95: 1.645, 0.99: 2.33}
        z_score = z_scores.get(confidence_level, 1.645)

        daily_volatility = (volatility / 100) / math.sqrt(252)
        var = position_value * daily_volatility * z_score

        return var


class FeeCalculator:
    """Trading fee calculations."""

    @staticmethod
    def calculate_commission(trade_value: float, commission_rate: float) -> float:
        """Calculate trading commission.

        Args:
            trade_value: Total trade value
            commission_rate: Commission as decimal (0.001 = 0.1%)

        Returns:
            Commission amount
        """
        return trade_value * commission_rate

    @staticmethod
    def calculate_total_cost(
        quantity: float,
        price: float,
        commission_rate: float = 0.001,
        slippage_rate: float = 0.001,
    ) -> tuple[float, float]:
        """Calculate total cost including fees.

        Args:
            quantity: Number of shares
            price: Price per share
            commission_rate: Commission rate
            slippage_rate: Slippage rate

        Returns:
            (total_cost, effective_price_per_share)
        """
        base_cost = quantity * price
        commission = FeeCalculator.calculate_commission(base_cost, commission_rate)
        slippage = FeeCalculator.calculate_commission(base_cost, slippage_rate)

        total_cost = base_cost + commission + slippage
        effective_price = total_cost / quantity if quantity > 0 else 0.0

        return total_cost, effective_price


class DecimalCalculator:
    """High-precision decimal calculations for financial data."""

    @staticmethod
    def round_to_decimals(value: float, decimals: int = 2) -> float:
        """Round to specific decimal places.

        Args:
            value: Value to round
            decimals: Number of decimal places

        Returns:
            Rounded value
        """
        quantize_str = "0." + "0" * decimals
        return float(Decimal(str(value)).quantize(Decimal(quantize_str)))

    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers.

        Args:
            numerator: Numerator
            denominator: Denominator
            default: Default value if denominator is 0

        Returns:
            Result of division or default
        """
        if denominator == 0:
            return default
        return numerator / denominator

"""Backtesting engine.

Historical strategy testing with proper bias prevention.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Callable, list
import statistics


@dataclass
class BacktestTrade:
    """A single trade in backtest."""

    entry_date: datetime
    entry_price: float
    exit_date: datetime
    exit_price: float
    quantity: float
    commission: float = 0.0

    @property
    def gross_pl(self) -> float:
        """Gross profit/loss."""
        return (self.exit_price - self.entry_price) * self.quantity

    @property
    def net_pl(self) -> float:
        """Net profit/loss after commission."""
        return self.gross_pl - self.commission

    @property
    def return_pct(self) -> float:
        """Return as percentage."""
        entry_cost = self.entry_price * self.quantity
        if entry_cost <= 0:
            return 0.0
        return (self.net_pl / entry_cost) * 100

    @property
    def duration_days(self) -> int:
        """Trade duration in days."""
        return (self.exit_date - self.entry_date).days


@dataclass
class BacktestResult:
    """Complete backtest results."""

    strategy_name: str
    ticker: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    trades: list[BacktestTrade] = field(default_factory=list)
    initial_prices: list[float] = field(default_factory=list)
    final_prices: list[float] = field(default_factory=list)
    portfolio_values: list[float] = field(default_factory=list)

    @property
    def final_value(self) -> float:
        """Final portfolio value."""
        return self.portfolio_values[-1] if self.portfolio_values else self.initial_capital

    @property
    def total_return(self) -> float:
        """Total return as percentage."""
        if self.initial_capital <= 0:
            return 0.0
        return ((self.final_value - self.initial_capital) / self.initial_capital) * 100

    @property
    def cagr(self) -> float:
        """Compound Annual Growth Rate."""
        years = (self.end_date - self.start_date).days / 365.25
        if years <= 0 or self.initial_capital <= 0:
            return 0.0
        return ((self.final_value / self.initial_capital) ** (1 / years) - 1) * 100

    @property
    def volatility(self) -> float:
        """Annualized volatility."""
        if len(self.portfolio_values) < 2:
            return 0.0

        returns = [
            (self.portfolio_values[i] - self.portfolio_values[i - 1])
            / self.portfolio_values[i - 1]
            for i in range(1, len(self.portfolio_values))
        ]

        if len(returns) < 2:
            return 0.0

        std_dev = statistics.stdev(returns)
        return std_dev * (252**0.5) * 100  # Annualize

    @property
    def max_drawdown(self) -> float:
        """Maximum drawdown from peak."""
        if not self.portfolio_values:
            return 0.0

        peak = self.portfolio_values[0]
        max_dd = 0.0

        for value in self.portfolio_values[1:]:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak > 0 else 0
            max_dd = max(max_dd, drawdown)

        return max_dd * 100

    @property
    def win_rate(self) -> float:
        """Percentage of winning trades."""
        if not self.trades:
            return 0.0
        wins = sum(1 for t in self.trades if t.net_pl > 0)
        return (wins / len(self.trades)) * 100

    @property
    def avg_trade_return(self) -> float:
        """Average return per trade."""
        if not self.trades:
            return 0.0
        return sum(t.return_pct for t in self.trades) / len(self.trades)

    @property
    def sharpe_ratio(self) -> float:
        """Sharpe ratio (risk-adjusted return)."""
        if not self.portfolio_values or len(self.portfolio_values) < 2:
            return 0.0

        returns = [
            (self.portfolio_values[i] - self.portfolio_values[i - 1])
            / self.portfolio_values[i - 1]
            for i in range(1, len(self.portfolio_values))
        ]

        if len(returns) < 2:
            return 0.0

        mean_return = statistics.mean(returns) * 252  # Annualize
        volatility = self.volatility / 100

        if volatility <= 0:
            return 0.0

        risk_free_rate = 0.02  # Assume 2% risk-free rate
        return (mean_return - risk_free_rate) / volatility

    @property
    def profit_factor(self) -> float:
        """Ratio of gross profit to gross loss."""
        if not self.trades:
            return 0.0

        gross_profit = sum(t.gross_pl for t in self.trades if t.gross_pl > 0)
        gross_loss = abs(sum(t.gross_pl for t in self.trades if t.gross_pl < 0))

        if gross_loss <= 0:
            return float("inf") if gross_profit > 0 else 0.0

        return gross_profit / gross_loss


class BacktestEngine:
    """Backtesting engine with bias prevention."""

    def __init__(self, initial_capital: float = 10000.0, commission_rate: float = 0.001):
        """Initialize backtester.

        Args:
            initial_capital: Starting capital
            commission_rate: Commission as decimal (0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate

    def run_backtest(
        self,
        strategy_name: str,
        ticker: str,
        historical_prices: list[dict],
        strategy_func: Callable,
    ) -> BacktestResult:
        """Run backtest on historical data.

        Args:
            strategy_name: Name of strategy
            ticker: Security ticker
            historical_prices: List of OHLCV dicts with 'date', 'close', 'volume'
            strategy_func: Function that generates signals (returns 'buy', 'sell', or 'hold')

        Returns:
            Backtest results
        """
        if not historical_prices:
            return BacktestResult(
                strategy_name=strategy_name,
                ticker=ticker,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow(),
                initial_capital=self.initial_capital,
            )

        result = BacktestResult(
            strategy_name=strategy_name,
            ticker=ticker,
            start_date=historical_prices[0]["date"],
            end_date=historical_prices[-1]["date"],
            initial_capital=self.initial_capital,
        )

        current_value = self.initial_capital
        position = None  # Current position
        result.portfolio_values.append(current_value)

        for i in range(len(historical_prices)):
            signal = strategy_func(historical_prices, i)
            current_price = historical_prices[i]["close"]
            current_date = historical_prices[i]["date"]

            if signal == "buy" and position is None:
                # Open position
                quantity = current_value / current_price
                commission = (current_value * self.commission_rate)
                position = {
                    "entry_date": current_date,
                    "entry_price": current_price,
                    "quantity": quantity,
                    "commission": commission,
                }
                current_value -= commission

            elif signal == "sell" and position is not None:
                # Close position
                exit_value = position["quantity"] * current_price
                commission = exit_value * self.commission_rate
                net_pl = exit_value - commission - (
                    position["quantity"] * position["entry_price"]
                    + position["commission"]
                )

                trade = BacktestTrade(
                    entry_date=position["entry_date"],
                    entry_price=position["entry_price"],
                    exit_date=current_date,
                    exit_price=current_price,
                    quantity=position["quantity"],
                    commission=position["commission"] + commission,
                )
                result.trades.append(trade)

                current_value = exit_value - commission
                position = None

            # Update portfolio value
            if position is not None:
                unrealized = (position["quantity"] * current_price) - (
                    position["quantity"] * position["entry_price"]
                )
                current_value = (
                    self.initial_capital - (
                        position["quantity"] * position["entry_price"]
                        + position["commission"]
                    )
                    + (position["quantity"] * current_price)
                )
            else:
                current_value = max(current_value, 0)

            result.portfolio_values.append(current_value)
            result.final_prices.append(current_price)

        return result

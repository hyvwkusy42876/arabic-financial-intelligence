"""Portfolio management and tracking."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """A buy/sell transaction."""

    transaction_id: str
    timestamp: datetime
    ticker: str
    transaction_type: str  # "buy" or "sell"
    quantity: float
    price: float
    commission: float = 0.0
    notes: str = ""

    @property
    def total_value(self) -> float:
        """Total transaction value including commission."""
        base = self.quantity * self.price
        if self.transaction_type == "buy":
            return base + self.commission
        return base - self.commission


@dataclass
class Position:
    """A current holding in a security."""

    ticker: str
    quantity: float
    average_entry_price: float
    current_price: float
    total_fees_paid: float = 0.0
    acquired_date: Optional[datetime] = None
    dividends_received: float = 0.0
    is_long: bool = True  # True for long positions, False for short

    @property
    def entry_value(self) -> float:
        """Total value at entry including fees."""
        return (self.quantity * self.average_entry_price) + self.total_fees_paid

    @property
    def current_value(self) -> float:
        """Current market value."""
        return self.quantity * self.current_price

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
    def total_return_with_dividends(self) -> float:
        """Total return including dividends received."""
        return self.unrealized_pl + self.dividends_received


@dataclass
class Portfolio:
    """A portfolio of holdings."""

    portfolio_id: str
    name: str
    description: str = ""
    cash: float = 0.0
    positions: dict[str, Position] = field(default_factory=dict)
    transactions: list[Transaction] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    is_paper_trading: bool = True  # False for real trading (v2+)
    base_currency: str = "EGP"

    @property
    def total_value(self) -> float:
        """Total portfolio value (positions + cash)."""
        positions_value = sum(p.current_value for p in self.positions.values())
        return positions_value + self.cash

    @property
    def total_invested(self) -> float:
        """Total amount invested in positions."""
        return sum(p.entry_value for p in self.positions.values())

    @property
    def total_position_value(self) -> float:
        """Current value of all positions."""
        return sum(p.current_value for p in self.positions.values())

    @property
    def unrealized_pl(self) -> float:
        """Total unrealized profit/loss."""
        return sum(p.unrealized_pl for p in self.positions.values())

    @property
    def unrealized_pl_pct(self) -> float:
        """Unrealized P&L as percentage of invested amount."""
        if self.total_invested <= 0:
            return 0.0
        return (self.unrealized_pl / self.total_invested) * 100

    @property
    def allocation(self) -> dict[str, float]:
        """Allocation percentages.

        Returns:
            {ticker: percentage}
        """
        if self.total_value <= 0:
            return {}
        return {
            ticker: (pos.current_value / self.total_value) * 100
            for ticker, pos in self.positions.items()
        }

    @property
    def cash_percentage(self) -> float:
        """Cash as percentage of portfolio."""
        if self.total_value <= 0:
            return 0.0
        return (self.cash / self.total_value) * 100

    def add_position(
        self,
        ticker: str,
        quantity: float,
        entry_price: float,
        fees: float = 0.0,
    ) -> Position:
        """Add or update a position.

        Args:
            ticker: Security ticker
            quantity: Quantity to add
            entry_price: Price per unit
            fees: Transaction fees

        Returns:
            Updated position
        """
        if ticker in self.positions:
            pos = self.positions[ticker]
            # Calculate new average entry price
            total_cost = (pos.quantity * pos.average_entry_price) + (
                quantity * entry_price
            )
            new_quantity = pos.quantity + quantity
            pos.average_entry_price = total_cost / new_quantity if new_quantity > 0 else 0
            pos.quantity = new_quantity
            pos.total_fees_paid += fees
        else:
            pos = Position(
                ticker=ticker,
                quantity=quantity,
                average_entry_price=entry_price,
                current_price=entry_price,
                total_fees_paid=fees,
                acquired_date=datetime.now(),
            )
            self.positions[ticker] = pos

        return pos

    def remove_position(self, ticker: str) -> Optional[Position]:
        """Remove a position (close it out completely).

        Args:
            ticker: Security ticker

        Returns:
            Removed position or None
        """
        return self.positions.pop(ticker, None)

    def update_prices(self, prices: dict[str, float]) -> None:
        """Update current prices for all positions.

        Args:
            prices: {ticker: current_price}
        """
        for ticker, price in prices.items():
            if ticker in self.positions:
                self.positions[ticker].current_price = price

    def add_cash(self, amount: float) -> None:
        """Add cash to portfolio.

        Args:
            amount: Amount to add
        """
        self.cash += amount
        self.updated_date = datetime.now()

    def withdraw_cash(self, amount: float) -> bool:
        """Withdraw cash from portfolio.

        Args:
            amount: Amount to withdraw

        Returns:
            True if successful, False if insufficient cash
        """
        if amount > self.cash:
            return False
        self.cash -= amount
        self.updated_date = datetime.now()
        return True

    def record_transaction(self, transaction: Transaction) -> None:
        """Record a transaction.

        Args:
            transaction: Transaction to record
        """
        self.transactions.append(transaction)
        self.updated_date = datetime.now()

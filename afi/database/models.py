"""Database initialization and models."""

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class UserProfile(Base):
    """User financial profile."""

    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Financial profile
    total_capital = Column(Float, default=0.0)
    emergency_fund = Column(Float, default=0.0)
    monthly_income = Column(Float, default=0.0)
    monthly_expenses = Column(Float, default=0.0)
    risk_tolerance = Column(Float, default=0.05)  # 5% default
    experience_level = Column(String, default="beginner")
    
    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")


class Portfolio(Base):
    """Portfolio tracking."""

    __tablename__ = "portfolios"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_profiles.id"), index=True)
    name = Column(String)
    description = Column(Text)
    base_currency = Column(String, default="EGP")
    initial_value = Column(Float, default=0.0)
    current_cash = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("UserProfile", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")


class Position(Base):
    """Holdings in a security."""

    __tablename__ = "positions"

    id = Column(String, primary_key=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"), index=True)
    ticker = Column(String, index=True)
    exchange = Column(String)  # EGX, NYSE, etc.
    quantity = Column(Float)
    average_entry_price = Column(Float)
    current_price = Column(Float)
    total_fees = Column(Float, default=0.0)
    dividends_received = Column(Float, default=0.0)
    acquired_date = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")


class Transaction(Base):
    """Buy/sell transactions."""

    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"), index=True)
    ticker = Column(String, index=True)
    transaction_type = Column(String)  # buy, sell
    quantity = Column(Float)
    price = Column(Float)
    commission = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")


class PriceHistory(Base):
    """Historical price data."""

    __tablename__ = "price_history"

    id = Column(String, primary_key=True)
    ticker = Column(String, index=True)
    exchange = Column(String)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, index=True)
    source = Column(String)  # Provider name
    currency = Column(String, default="EGP")


class Recommendation(Base):
    """Investment recommendations."""

    __tablename__ = "recommendations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_profiles.id"), index=True)
    ticker = Column(String, index=True)
    recommendation_type = Column(String)  # buy, sell, hold, watch
    thesis = Column(Text)
    entry_price = Column(Float)
    target_price = Column(Float)
    stop_loss = Column(Float)
    confidence = Column(Float)  # 0.0 to 1.0
    expected_return = Column(Float)
    time_horizon_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    executed_at = Column(DateTime)
    result_price = Column(Float)
    actual_return = Column(Float)
    is_evaluated = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("UserProfile", back_populates="recommendations")


class PaperTrade(Base):
    """Paper trading records."""

    __tablename__ = "paper_trades"

    id = Column(String, primary_key=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"), index=True)
    ticker = Column(String, index=True)
    order_type = Column(String)  # market, limit
    action = Column(String)  # buy, sell
    quantity = Column(Float)
    price = Column(Float)
    commission = Column(Float)
    status = Column(String)  # pending, filled, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime)
    realized_pl = Column(Float)


class News(Base):
    """News and research articles."""

    __tablename__ = "news"

    id = Column(String, primary_key=True)
    title = Column(String)
    summary = Column(Text)
    content = Column(Text)
    source = Column(String)  # Provider name
    source_url = Column(String)
    ticker = Column(String, index=True)
    published_at = Column(DateTime, index=True)
    retrieved_at = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String)  # positive, neutral, negative
    relevance_score = Column(Float)  # 0-1
    

class BacktestResult(Base):
    """Backtest results."""

    __tablename__ = "backtest_results"

    id = Column(String, primary_key=True)
    strategy_name = Column(String)
    ticker = Column(String, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    initial_capital = Column(Float)
    final_value = Column(Float)
    total_return = Column(Float)
    cagr = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    win_rate = Column(Float)
    total_trades = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(Text)  # JSON


class AuditLog(Base):
    """Audit logging for financial actions."""

    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    action = Column(String)  # buy, sell, recommendation, etc.
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String)
    success = Column(Boolean, default=True)


def init_database(database_url: str = "sqlite:///./afi_data.db"):
    """Initialize database.
    
    Args:
        database_url: Database connection URL
    """
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(bind=engine)
    return engine


def get_session(database_url: str = "sqlite:///./afi_data.db"):
    """Get database session.
    
    Args:
        database_url: Database connection URL
        
    Returns:
        SQLAlchemy session
    """
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()

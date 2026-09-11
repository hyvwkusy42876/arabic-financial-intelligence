"""Application settings and configuration management."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # AI Provider
    ai_provider: str = "ollama"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "mistral:7b-instruct-v0.2-q4_K_M"
    ollama_timeout: int = 120

    # Market Data
    market_data_provider: str = "mock"
    yahoo_finance_enabled: bool = True

    # News
    news_provider: str = "mock"

    # Application
    debug: bool = False
    log_level: str = "INFO"
    database_url: str = "sqlite:///./afi_data.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:3000"

    # Security
    secret_key: str = "change-me-in-production"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    cors_allow_credentials: bool = True

    # Hardware
    gpu_enabled: bool = True
    gpu_device_id: int = 0
    max_vram_gb: int = 4
    max_ram_gb: int = 12
    max_context_length: int = 2048
    batch_size: int = 1

    # Cache
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300
    cache_market_data_ttl: int = 60
    cache_news_ttl: int = 600

    # Backtesting
    backtest_max_workers: int = 4
    backtest_chunk_size: int = 252

    # Paper Trading
    paper_trading_initial_cash: float = 10000.0
    paper_trading_commission: float = 0.001
    paper_trading_slippage: float = 0.001

    # Risk Engine
    risk_default_max_position: float = 0.2
    risk_default_max_concentration: float = 0.3
    risk_default_portfolio_max_risk: float = 0.05

    # Language
    default_language: str = "ar"
    supported_languages: str = "ar,en"
    default_currency: str = "EGP"
    default_timezone: str = "Africa/Cairo"

    class Config:
        """Pydantic settings configuration."""

        env_file = "config/.env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()

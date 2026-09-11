"""Provider abstraction layer.

Supports multiple market data, news, and LLM providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class DataSource:
    """Metadata about data source."""

    provider: str
    timestamp: datetime
    timezone: str
    retrieval_timestamp: datetime
    quality_status: str  # VALID, STALE, INCOMPLETE, CONFLICTING, UNVERIFIED
    confidence: float  # 0-1
    note: str = ""


class BaseMarketDataProvider(ABC):
    """Base class for market data providers."""

    @abstractmethod
    def get_quote(self, ticker: str, exchange: str = "EGX") -> Optional[dict]:
        """Get current quote for a security.

        Args:
            ticker: Security ticker
            exchange: Exchange name

        Returns:
            Quote dict with price, volume, etc. or None if unavailable
        """
        pass

    @abstractmethod
    def get_historical_prices(
        self, ticker: str, exchange: str, start_date: datetime, end_date: datetime
    ) -> Optional[list[dict]]:
        """Get historical price data.

        Args:
            ticker: Security ticker
            exchange: Exchange name
            start_date: Start date
            end_date: End date

        Returns:
            List of OHLCV dicts or None
        """
        pass

    @abstractmethod
    def get_fundamentals(self, ticker: str, exchange: str = "EGX") -> Optional[dict]:
        """Get fundamental data.

        Args:
            ticker: Security ticker
            exchange: Exchange name

        Returns:
            Fundamentals dict (P/E, dividend, etc.) or None
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check provider health.

        Returns:
            True if provider is available
        """
        pass


class BaseNewsProvider(ABC):
    """Base class for news/research providers."""

    @abstractmethod
    def search_news(
        self, query: str, ticker: Optional[str] = None, limit: int = 10
    ) -> Optional[list[dict]]:
        """Search for news articles.

        Args:
            query: Search query
            ticker: Optional ticker filter
            limit: Maximum results

        Returns:
            List of news dicts or None
        """
        pass

    @abstractmethod
    def get_company_news(self, ticker: str, limit: int = 10) -> Optional[list[dict]]:
        """Get news for a specific company.

        Args:
            ticker: Company ticker
            limit: Maximum results

        Returns:
            List of news dicts or None
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check provider health.

        Returns:
            True if provider is available
        """
        pass


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def chat(
        self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2048
    ) -> Optional[str]:
        """Send chat request to LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum output tokens

        Returns:
            Response text or None
        """
        pass

    @abstractmethod
    def structured_output(
        self, prompt: str, schema: dict, temperature: float = 0.0
    ) -> Optional[dict]:
        """Get structured JSON output from LLM.

        Args:
            prompt: Prompt text
            schema: JSON schema for output
            temperature: Sampling temperature

        Returns:
            Parsed JSON dict or None
        """
        pass

    @abstractmethod
    def stream(
        self, messages: list[dict], temperature: float = 0.7
    ) -> Any:
        """Stream response from LLM.

        Args:
            messages: List of message dicts
            temperature: Sampling temperature

        Yields:
            Response chunks
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check provider health.

        Returns:
            True if provider is available
        """
        pass

    @abstractmethod
    def model_info(self) -> dict:
        """Get model information.

        Returns:
            Info dict with model name, size, etc.
        """
        pass

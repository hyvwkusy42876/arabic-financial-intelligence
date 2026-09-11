"""Mock providers for testing and development."""

from datetime import datetime, timedelta
from typing import Optional
import random

from afi.providers.base import (
    BaseMarketDataProvider,
    BaseNewsProvider,
    BaseLLMProvider,
    DataSource,
)


class MockMarketDataProvider(BaseMarketDataProvider):
    """Mock market data provider for testing."""

    def __init__(self):
        """Initialize mock provider."""
        self.available = True
        # Mock data for Egyptian stocks
        self.mock_prices = {
            "HRHO": 8.25,  # Heliopolis Company
            "EFID": 0.86,  # Egyptian Financial & Industrial
            "EMCO": 15.50,  # Egyptian Kuwaiti Holding
            "JUFO": 3.42,  # Juhayna Food Industries
            "ORHD": 1.18,  # Orasecom Telecom Holding
        }

    def get_quote(self, ticker: str, exchange: str = "EGX") -> Optional[dict]:
        """Get mock quote."""
        if ticker not in self.mock_prices:
            return None

        price = self.mock_prices[ticker]
        variation = random.uniform(-0.05, 0.05)
        return {
            "ticker": ticker,
            "exchange": exchange,
            "price": price * (1 + variation),
            "open": price * 0.99,
            "high": price * 1.02,
            "low": price * 0.98,
            "volume": random.randint(100000, 500000),
            "timestamp": datetime.utcnow(),
            "currency": "EGP",
            "source": DataSource(
                provider="mock",
                timestamp=datetime.utcnow(),
                timezone="Africa/Cairo",
                retrieval_timestamp=datetime.utcnow(),
                quality_status="VALID",
                confidence=1.0,
            ),
        }

    def get_historical_prices(
        self, ticker: str, exchange: str, start_date: datetime, end_date: datetime
    ) -> Optional[list[dict]]:
        """Get mock historical prices."""
        if ticker not in self.mock_prices:
            return None

        prices = []
        current_date = start_date
        base_price = self.mock_prices[ticker]

        while current_date <= end_date:
            variation = random.uniform(-0.02, 0.02)
            close = base_price * (1 + variation)
            prices.append(
                {
                    "date": current_date,
                    "open": close * 0.99,
                    "high": close * 1.01,
                    "low": close * 0.99,
                    "close": close,
                    "volume": random.randint(50000, 200000),
                }
            )
            base_price = close
            current_date += timedelta(days=1)

        return prices

    def get_fundamentals(self, ticker: str, exchange: str = "EGX") -> Optional[dict]:
        """Get mock fundamentals."""
        if ticker not in self.mock_prices:
            return None

        return {
            "ticker": ticker,
            "pe_ratio": random.uniform(8, 20),
            "pb_ratio": random.uniform(0.5, 3),
            "dividend_yield": random.uniform(0, 0.08),
            "earnings_per_share": random.uniform(0.5, 2),
            "book_value_per_share": random.uniform(2, 10),
            "market_cap_millions": random.uniform(100, 5000),
            "revenue_millions": random.uniform(50, 1000),
            "net_income_millions": random.uniform(5, 100),
        }

    def health_check(self) -> bool:
        """Check provider health."""
        return self.available


class MockNewsProvider(BaseNewsProvider):
    """Mock news provider for testing."""

    def __init__(self):
        """Initialize mock provider."""
        self.available = True
        self.mock_headlines = [
            "شركة مصرية تعلن عن زيادة أرباحها بنسبة 15%",
            "البنك المركزي يرفع سعر الفائدة 0.5%",
            "اتفاق جديد لمشروع بنية تحتية بقيمة مليار دولار",
            "الجنيه المصري يستقر أمام الدولار الأمريكي",
            "قطاع السياحة يشهد نموًا قويًا في الربع الأخير",
        ]

    def search_news(
        self, query: str, ticker: Optional[str] = None, limit: int = 10
    ) -> Optional[list[dict]]:
        """Get mock news search results."""
        results = []
        for i in range(min(limit, len(self.mock_headlines))):
            results.append(
                {
                    "title": self.mock_headlines[i],
                    "summary": f"Mock summary for {query}...",
                    "source": "Mock News",
                    "url": f"https://example.com/news/{i}",
                    "published_at": datetime.utcnow() - timedelta(hours=i),
                    "ticker": ticker or "N/A",
                    "sentiment": random.choice(["positive", "neutral", "negative"]),
                }
            )
        return results

    def get_company_news(self, ticker: str, limit: int = 10) -> Optional[list[dict]]:
        """Get mock company news."""
        return self.search_news(f"news about {ticker}", ticker, limit)

    def health_check(self) -> bool:
        """Check provider health."""
        return self.available


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing."""

    def __init__(self):
        """Initialize mock provider."""
        self.available = True

    def chat(
        self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2048
    ) -> Optional[str]:
        """Return mock response."""
        return "هذا رد تجريبي من نموذج وهمي. في بيئة الإنتاج، ستتلقى ردًا حقيقيًا من LLM."

    def structured_output(
        self, prompt: str, schema: dict, temperature: float = 0.0
    ) -> Optional[dict]:
        """Return mock structured response."""
        return {
            "analysis": "Mock analysis",
            "recommendation": "hold",
            "confidence": 0.7,
        }

    def stream(self, messages: list[dict], temperature: float = 0.7):
        """Mock streaming response."""
        yield "Mock "
        yield "streaming "
        yield "response"

    def health_check(self) -> bool:
        """Check provider health."""
        return self.available

    def model_info(self) -> dict:
        """Get mock model info."""
        return {
            "name": "mock-model",
            "type": "mock",
            "parameters": "N/A",
            "context_length": 2048,
        }

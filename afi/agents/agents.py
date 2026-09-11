"""AI agents for financial analysis and decision support."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class AgentResponse:
    """Response from an agent."""

    agent_name: str
    timestamp: datetime
    content: str
    structured_data: Optional[dict] = None
    sources: list[str] = None
    confidence: float = 0.5
    error: Optional[str] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = []


class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, llm_provider: Any, name: str):
        """Initialize agent.

        Args:
            llm_provider: LLM provider instance
            name: Agent name
        """
        self.llm_provider = llm_provider
        self.name = name
        self.conversation_history = []

    @abstractmethod
    async def process(self, query: str, context: dict = None) -> AgentResponse:
        """Process a query and return response.

        Args:
            query: User query
            context: Additional context

        Returns:
            Agent response
        """
        pass

    @abstractmethod
    async def explain(self, data: dict) -> str:
        """Explain complex data in natural language.

        Args:
            data: Data to explain

        Returns:
            Natural language explanation
        """
        pass

    def _build_system_prompt(self, role: str, constraints: list[str]) -> str:
        """Build system prompt for agent.

        Args:
            role: Agent role description
            constraints: List of constraints

        Returns:
            System prompt
        """
        constraints_text = "\n".join([f"- {c}" for c in constraints])
        return f"""
You are {role}.

Constraints:
{constraints_text}

Respond in Arabic when appropriate. Use precise financial terminology.
Always cite sources and indicate confidence levels.
"""


class ResearchAgent(BaseAgent):
    """Research and analysis agent."""

    async def process(self, query: str, context: dict = None) -> AgentResponse:
        """Process research query."""
        try:
            system_prompt = self._build_system_prompt(
                "أخصائي البحث المالي (Financial Research Specialist)",
                [
                    "Provide fact-based research",
                    "Always cite sources",
                    "Clearly separate facts from analysis",
                    "Mark uncertainty explicitly",
                ],
            )

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": query})

            response = self.llm_provider.chat(messages, temperature=0.3, max_tokens=1500)

            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})

            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content=response,
                confidence=0.7,
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content="",
                error=str(e),
                confidence=0.0,
            )

    async def explain(self, data: dict) -> str:
        """Explain research data."""
        prompt = f"اشرح هذه البيانات المالية بشكل واضح وموجز:\n{data}"
        response = self.llm_provider.chat(
            [{"role": "user", "content": prompt}], temperature=0.5, max_tokens=500
        )
        return response


class FundamentalAnalysisAgent(BaseAgent):
    """Fundamental analysis agent."""

    async def process(self, query: str, context: dict = None) -> AgentResponse:
        """Process fundamental analysis query."""
        try:
            system_prompt = self._build_system_prompt(
                "محلل أساسي (Fundamental Analyst)",
                [
                    "Analyze company financials objectively",
                    "Compare to industry peers",
                    "Identify value and growth metrics",
                    "Never guarantee returns",
                ],
            )

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": query})

            response = self.llm_provider.chat(messages, temperature=0.3, max_tokens=1500)

            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})

            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content=response,
                confidence=0.65,
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content="",
                error=str(e),
                confidence=0.0,
            )

    async def explain(self, data: dict) -> str:
        """Explain fundamental metrics."""
        prompt = f"اشرح هذه المقاييس الأساسية:\n{data}"
        response = self.llm_provider.chat(
            [{"role": "user", "content": prompt}], temperature=0.5, max_tokens=500
        )
        return response


class TechnicalAnalysisAgent(BaseAgent):
    """Technical analysis agent."""

    async def process(self, query: str, context: dict = None) -> AgentResponse:
        """Process technical analysis query."""
        try:
            system_prompt = self._build_system_prompt(
                "محلل تقني (Technical Analyst)",
                [
                    "Analyze price action and trends",
                    "Identify support and resistance",
                    "Use indicators appropriately",
                    "Never use technical analysis alone",
                    "Always combine with fundamental analysis",
                ],
            )

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": query})

            response = self.llm_provider.chat(messages, temperature=0.3, max_tokens=1500)

            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})

            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content=response,
                confidence=0.55,
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content="",
                error=str(e),
                confidence=0.0,
            )

    async def explain(self, data: dict) -> str:
        """Explain technical patterns."""
        prompt = f"اشرح هذه الأنماط التقنية:\n{data}"
        response = self.llm_provider.chat(
            [{"role": "user", "content": prompt}], temperature=0.5, max_tokens=500
        )
        return response


class EventAnalysisAgent(BaseAgent):
    """Economic and corporate event analysis agent."""

    async def process(self, query: str, context: dict = None) -> AgentResponse:
        """Process event analysis query."""
        try:
            system_prompt = self._build_system_prompt(
                "محلل الأحداث الاقتصادية (Economic Event Analyst)",
                [
                    "Analyze impact of economic and corporate events",
                    "Identify affected sectors and companies",
                    "Assess whether information is priced in",
                    "Consider historical precedents",
                    "Provide scenario analysis",
                ],
            )

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": query})

            response = self.llm_provider.chat(messages, temperature=0.5, max_tokens=2000)

            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})

            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content=response,
                confidence=0.6,
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                timestamp=datetime.utcnow(),
                content="",
                error=str(e),
                confidence=0.0,
            )

    async def explain(self, data: dict) -> str:
        """Explain event impact."""
        prompt = f"اشرح تأثير هذا الحدث الاقتصادي:\n{data}"
        response = self.llm_provider.chat(
            [{"role": "user", "content": prompt}], temperature=0.5, max_tokens=800
        )
        return response

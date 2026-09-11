# Arabic Financial Intelligence Platform

**Production-grade AI Financial Intelligence and Personal Business Management Platform**

A serious, local-first financial advisor system designed for Arabic-speaking investors. Communicate naturally in Arabic with a deterministic, risk-aware financial intelligence engine.

## Features

### Core Capabilities
- 🗣️ **Arabic-First Interface**: Complete Arabic UI with support for Egyptian dialect, MSA, and financial terminology
- 💰 **Portfolio Management**: Track multiple portfolios with real-time P&L, allocation analysis, and risk metrics
- ⚠️ **Deterministic Risk Engine**: Position sizing, concentration limits, scenario analysis—independent of LLM
- 📊 **Paper Trading**: Full virtual trading environment with realistic fees, slippage, and execution
- 📰 **Event-Driven Analysis**: Economic event identification, affected sectors/companies, impact scoring
- 🔬 **Research & News Integration**: Multi-source aggregation with reliability tiers and conflict detection
- 📈 **Backtesting Engine**: Historical strategy testing with proper bias prevention
- 🎯 **Scenario Analysis**: Bull/base/bear case development with evidence-based probabilities
- 💾 **Local-First Architecture**: Works offline; online features clearly marked
- 🔒 **Security-First**: No real trading in v1, sandboxed AI, prompt-injection resistant

### AI & Markets
- **Multiple AI Backends**: Support for Ollama (local), with abstractions for future cloud providers
- **Market Data Providers**: EGX, international equities, currencies, commodities
- **Recommendation Tracking**: Log, evaluate, and calibrate all recommendations
- **Evaluation System**: Track accuracy, timing, risk quality, and calibration over time

### Hardware-Optimized
- Designed for RTX 3050 Laptop (4GB VRAM) + 16GB RAM
- Quantized model recommendations
- Memory-aware configuration
- Graceful CPU fallback

## Quick Start

### Prerequisites
- Python 3.11+
- SQLite3 (included with Python)
- Optional: [Ollama](https://ollama.ai) for local LLM (recommended: mistral or neural-chat quantized)
- Windows/Linux/macOS

### Installation

```bash
# Clone repository
git clone https://github.com/hyvwkusy42876/arabic-financial-intelligence.git
cd arabic-financial-intelligence

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m afi.database.init

# Create config file
cp config/.env.example config/.env
# Edit config/.env with your settings
```

### Running the Application

```bash
# Start backend server
python -m afi.server.main

# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000` in Arabic.

### Using Local Ollama (Recommended)

```bash
# Install Ollama from https://ollama.ai

# Pull a recommended model
ollama pull mistral:7b-instruct-v0.2-q4_K_M

# Start Ollama server (runs on port 11434 by default)
ollama serve

# In application Settings, select Ollama as AI provider
# Model: mistral:7b-instruct-v0.2-q4_K_M
```

## Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Arabic)                  │
│              React + TypeScript + Tailwind CSS               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway & Orchestrator                  │
│            Handles routing, auth, request validation         │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────┐
        │       Core Financial Engines        │
        ├─────────────────────────────────────┤
        │ • Risk Engine (Deterministic)       │
        │ • Portfolio Manager                 │
        │ • Position Sizing                   │
        │ • P&L Calculator                    │
        │ • Scenario Engine                   │
        │ • Backtesting Engine                │
        │ • Paper Trading Engine              │
        └─────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────┐
        │    AI & Knowledge Components        │
        ├─────────────────────────────────────┤
        │ • Conversation Manager              │
        │ • Intent Router                     │
        │ • Research Agent                    │
        │ • Market Data Agent                 │
        │ • News Agent                        │
        │ • Fundamental Analysis Agent        │
        │ • Technical Analysis Agent          │
        │ • Event Analysis Agent              │
        │ • Recommendation Evaluator          │
        └─────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────┐
        │      Data & Provider Layer          │
        ├─────────────────────────────────────┤
        │ • Market Data Providers             │
        │   - EGX Integration                 │
        │   - International Equities          │
        │   - Currencies, Commodities         │
        │ • News/Research Providers           │
        │ • LLM Providers (Ollama, etc)       │
        │ • Cache Management                  │
        └─────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────┐
        │      Database & Persistence         │
        ├─────────────────────────────────────┤
        │ • SQLite Local Database             │
        │ • Migration System                  │
        │ • Query Optimization                │
        └─────────────────────────────────────┘
```

### Directory Structure

```
arabic-financial-intelligence/
├── afi/                           # Main application package
│   ├── __init__.py
│   ├── core/                      # Core financial logic
│   │   ├── portfolio.py           # Portfolio management
│   │   ├── position.py            # Position tracking
│   │   ├── risk.py                # Risk engine (deterministic)
│   │   ├── scenario.py            # Scenario analysis
│   │   └── calculator.py          # P&L, fees, etc.
│   │
│   ├── database/                  # Data persistence
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── init.py                # Database initialization
│   │   ├── migrations/            # Alembic migrations
│   │   └── queries.py             # Common queries
│   │
│   ├── providers/                 # Data providers (abstraction)
│   │   ├── base.py                # Provider interfaces
│   │   ├── market_data/           # Market data providers
│   │   │   ├── base.py
│   │   │   ├── egx.py             # Egyptian Exchange
│   │   │   ├── yahoo.py           # Yahoo Finance fallback
│   │   │   └── mock.py            # Mock for testing
│   │   ├── news/                  # News/research providers
│   │   │   ├── base.py
│   │   │   ├── aggregator.py      # Multi-source aggregation
│   │   │   └── mock.py
│   │   └── llm/                   # LLM providers
│   │       ├── base.py
│   │       ├── ollama.py          # Local Ollama
│   │       ├── openai.py          # Future: OpenAI
│   │       └── mock.py            # Mock for testing
│   │
│   ├── agents/                    # AI agents/components
│   │   ├── base.py                # Agent base class
│   │   ├── orchestrator.py        # Main orchestrator
│   │   ├── intent_router.py       # Intent classification
│   │   ├── research.py            # Research agent
│   │   ├── market_data.py         # Market data agent
│   │   ├── news.py                # News agent
│   │   ├── fundamental.py         # Fundamental analysis
│   │   ├── technical.py           # Technical analysis
│   │   ├── event.py               # Event analysis
│   │   └── evaluator.py           # Recommendation evaluator
│   │
│   ├── engines/                   # Specialized engines
│   │   ├── backtesting.py         # Backtesting engine
│   │   ├── paper_trading.py       # Paper trading
│   │   ├── technical_analysis.py  # TA calculations
│   │   ├── fundamental_analysis.py# FA calculations
│   │   └── economic.py            # Macro analysis
│   │
│   ├── memory/                    # State & memory management
│   │   ├── user_profile.py        # User financial profile
│   │   ├── conversation.py        # Conversation history
│   │   ├── cache.py               # Data caching
│   │   └── provenance.py          # Source tracking
│   │
│   ├── security/                  # Security layer
│   │   ├── sanitizer.py           # Input sanitization
│   │   ├── permissions.py         # Permission checks
│   │   ├── audit.py               # Audit logging
│   │   └── validator.py           # Data validation
│   │
│   ├── server/                    # API server
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI application
│   │   ├── routes/                # API routes
│   │   │   ├── chat.py
│   │   │   ├── portfolio.py
│   │   │   ├── market.py
│   │   │   ├── paper_trade.py
│   │   │   ├── recommendation.py
│   │   │   ├── backtest.py
│   │   │   ├── settings.py
│   │   │   └── health.py
│   │   └── middleware/            # Middleware
│   │       ├── auth.py
│   │       └── cors.py
│   │
│   ├── utils/                     # Utilities
│   │   ├── arabic.py              # Arabic language handling
│   │   ├── currency.py            # Currency conversion
│   │   ├── logger.py              # Structured logging
│   │   ├── timer.py               # Performance timing
│   │   └── validation.py          # Input validation
│   │
│   └── cli/                       # CLI utilities
│       ├── setup.py               # Setup commands
│       ├── dev.py                 # Development utilities
│       └── test.py                # Test utilities
│
├── frontend/                      # React frontend
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── services/              # API services
│   │   ├── store/                 # Redux/Zustand state
│   │   ├── styles/                # Tailwind config
│   │   ├── i18n/                  # Arabic localization
│   │   ├── types/                 # TypeScript types
│   │   └── App.tsx                # Root component
│   ├── public/                    # Static assets
│   └── package.json
│
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   │   ├── core/
│   │   ├── providers/
│   │   ├── engines/
│   │   └── utils/
│   ├── integration/               # Integration tests
│   ├── security/                  # Security tests
│   ├── financial_logic/           # Financial logic tests
│   ├── fixtures/                  # Test data
│   └── conftest.py                # Pytest configuration
│
├── config/                        # Configuration
│   ├── .env.example               # Environment template
│   ├── settings.py                # Settings loader
│   ├── logging.yaml               # Logging configuration
│   └── models.yaml                # Model recommendations
│
├── scripts/                       # Utility scripts
│   ├── backtest_runner.py
│   ├── data_importer.py
│   ├── health_check.py
│   └── generate_recommendations.py
│
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   ├── DATA_SOURCES.md
│   ├── MODELS.md
│   ├── BACKTESTING.md
│   ├── PAPER_TRADING.md
│   ├── TROUBLESHOOTING.md
│   ├── API.md
│   └── USER_GUIDE.md
│
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata
├── pytest.ini                     # Pytest configuration
├── .gitignore                     # Git ignore rules
├── SETUP.md                       # Setup instructions
└── CONTRIBUTING.md               # Contribution guidelines
```

## Key Design Decisions

### 1. Deterministic Risk Engine
All risk calculations are performed by deterministic software, never by the LLM. The AI interprets and explains results, but cannot override calculations.

### 2. Separation of Concerns
- **Facts**: Market data, historical prices, official disclosures
- **Calculations**: Position sizing, P&L, fees (deterministic)
- **Analysis**: AI interpretation of facts
- **Predictions**: Probability-weighted scenarios (marked with uncertainty)
- **Uncertainty**: Always explicit, never hidden

### 3. Local-First, Online-Enhanced
- Core functionality works offline
- Online features clearly marked
- No mandatory cloud dependencies
- Optional cloud APIs for enhanced research

### 4. Multiple AI Providers
- Built-in: Ollama (local)
- Extensible: OpenAI, Claude, Cohere interfaces prepared
- Easy provider switching in settings
- Fallback to mock provider for testing

### 5. No Real Trading in v1
- Paper trading only
- BrokerAdapter abstraction prepared
- Real broker implementations disabled
- Permission system prevents accidental live orders

### 6. Explainable Recommendations
Every recommendation includes:
- Supporting evidence with sources
- Calculation methodology
- Scenarios (bull/base/bear)
- Risk assessment
- Invalidation conditions
- Confidence calibration

## Configuration

### Environment Variables

Create `config/.env`:

```
# AI Provider
AI_PROVIDER=ollama  # or openai, claude, etc.
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct-v0.2-q4_K_M

# Market Data
MARKET_DATA_PROVIDER=mock  # or egx, yahoo, alpha_vantage
# EGX_API_KEY=your_key_here
# YAHOO_FINANCE_ENABLED=true

# News & Research
NEWS_PROVIDER=mock  # or newsapi, finnhub, etc.
# NEWS_API_KEY=your_key_here

# Application
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./afi_data.db
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=generate-a-random-secret-key-here
CORS_ORIGINS=http://localhost:3000

# Hardware
GPU_ENABLED=true
MAX_VRAM_GB=4
MAX_RAM_GB=12
```

## Supported Markets & Assets

### Exchanges
- **EGX** (Egyptian Exchange): Equities, bonds
- **International**: US, UK, EU equities (via providers)
- **Currencies**: EGP, USD, EUR, GBP
- **Commodities**: Gold, oil, etc.
- **Indices**: EGX30, S&P 500, etc.

### Data Quality Tiers
- **Tier 1**: Official sources (exchange, government, company filings)
- **Tier 2**: Major financial news organizations
- **Tier 3**: Secondary reporting
- **Tier 4**: Social media / unverified (clearly marked)

## Language Support

### Arabic Support
- **Egyptian Dialect** (default for conversational)
- **Modern Standard Arabic** (formal terms)
- **Financial Terminology** in Arabic
- **Arabizi** (mixed script) understanding

### Example Interactions
```
User: "معايا 500 جنيه وعايز أخاطر بـ10% لمدة أسبوع"
Translator: I have 500 EGP and want to risk 10% for one week

System Response:
رأس المال: 500 جنيه
الحد الأقصى للمخاطرة: 50 جنيه
المدة: أسبوع واحد
```

## Financial Logic Guarantees

1. ✅ **No guaranteed returns** - Never claim "السهم هيطلع أكيد"
2. ✅ **No fake data** - Always source-attributed
3. ✅ **Explicit uncertainty** - Calibrated confidence levels
4. ✅ **Risk-aware** - All recommendations include downside scenario
5. ✅ **Transaction costs** - Always accounted for
6. ✅ **Liquidity checks** - Asset tradeability verified
7. ✅ **Evidence-based** - Source provenance tracked
8. ✅ **Conflict detection** - Sources that disagree are flagged
9. ✅ **No silent stale data** - Timestamp always shown
10. ✅ **Fallback planning** - Graceful degradation when data unavailable

## Paper Trading

Full virtual trading environment:
- Virtual cash account
- Market/limit orders
- Realistic fees & slippage
- Position tracking
- P&L calculation
- Transaction history
- Can be converted to real trading recommendations

## Backtesting

Historical strategy testing with:
- No look-ahead bias
- No future-data leakage
- Realistic commissions
- Spread/slippage assumptions
- Delayed execution modeling
- Metrics: total return, CAGR, volatility, max drawdown, Sharpe, Sortino, win rate

## Security Model

### Threat Protection
- ✅ Prompt injection resistant
- ✅ Malicious web content sandboxed
- ✅ No arbitrary code execution from external sources
- ✅ Path traversal prevention
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CSRF protection where relevant
- ✅ Secret key management (env-based, no hardcoding)
- ✅ Audit logging for all financial actions

### Real Trading Safety (Future)
When real broker integration is added:
- Explicit user confirmation required
- Maximum daily loss limits
- Maximum position size limits
- Maximum portfolio exposure limits
- Emergency kill switch
- Duplicate order protection
- Idempotency keys
- Comprehensive audit trail

## Testing

Run the complete test suite:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Security tests
pytest tests/security/

# Financial logic tests
pytest tests/financial_logic/

# With coverage
pytest --cov=afi tests/
```

## System Health Monitoring

Access System Health dashboard:
```
http://localhost:3000/system-health
```

Displays:
- AI backend status
- Database health
- Market data status
- News provider status
- GPU detection & VRAM
- Disk space
- Last successful data update
- System performance metrics

## Development

### Adding a New Market Data Provider

1. Create `afi/providers/market_data/your_provider.py`
2. Extend `BaseMarketDataProvider`
3. Implement required methods
4. Add to provider registry
5. Add tests in `tests/unit/providers/`
6. Document in `docs/DATA_SOURCES.md`

### Adding a New AI Agent

1. Create `afi/agents/your_agent.py`
2. Extend `BaseAgent`
3. Implement `process()` and `explain()`
4. Register in orchestrator
5. Add tests and integration tests
6. Document interface

### Adding Support for New LLM Provider

1. Create `afi/providers/llm/your_provider.py`
2. Extend `BaseLLMProvider`
3. Implement chat, structured output, streaming
4. Add configuration
5. Add to provider registry
6. Test on RTX 3050 4GB VRAM
7. Document in MODELS.md

## Performance Notes

### Optimizations for RTX 3050 4GB VRAM
- Model quantization (Q4_K_M recommended)
- Context window limits (2K-4K typical)
- Batch size = 1 for inference
- Lazy model loading
- GPU memory management
- CPU fallback for text processing

### Recommended Models
- **Mistral 7B Q4_K_M** (5.5GB) - Best all-around
- **Neural-Chat 7B Q4_K_M** (5.5GB) - Good for instruction following
- **Phi-2 Q4_K_M** (1.5GB) - Fastest, adequate performance
- **Llama 2 7B Q4_K_M** (5.5GB) - General purpose

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for:
- Ollama connection issues
- Database initialization problems
- Market data provider errors
- Memory/GPU issues
- Arabic rendering problems
- Performance optimization

## Contributing

See `CONTRIBUTING.md` for:
- Code style (Black, isort)
- Testing requirements (>80% coverage)
- Commit message conventions
- PR review process
- Security review checklist

## License

MIT License - see LICENSE file

## Support & Community

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Documentation: `/docs`

## Disclaimer

This platform is a decision-support and research tool, not a guarantee of financial results. All investments carry risk. Past performance does not guarantee future results. Consult with qualified financial advisors before making investment decisions.

---

**Status**: Version 0.1.0 (Active Development)  
**Last Updated**: 2024  
**Target Hardware**: RTX 3050 Laptop (4GB VRAM) + 16GB RAM

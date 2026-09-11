"""Setup and installation guide in Arabic."""

# إعداد منصة الذكاء المالي العربية

## المتطلبات

- Python 3.11 أو أحدث
- SQLite3 (مضمن مع Python)
- Ollama (اختياري لكن موصى به) - للنموذج اللغوي المحلي
- Windows/Linux/macOS

## الخطوة 1: تثبيت Python

### على Windows:

```bash
# تحميل من https://python.org
# أثناء التثبيت، تأكد من تحديد "Add Python to PATH"
python --version
```

### على Linux/macOS:

```bash
# Ubuntu/Debian
sudo apt-get install python3.11 python3.11-venv

# macOS
brew install python@3.11

python3 --version
```

## الخطوة 2: استنساخ المستودع

```bash
git clone https://github.com/hyvwkusy42876/arabic-financial-intelligence.git
cd arabic-financial-intelligence
```

## الخطوة 3: إنشاء بيئة افتراضية

### على Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### على Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

## الخطوة 4: تثبيت المتطلبات

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## الخطوة 5: تهيئة قاعدة البيانات

```bash
python -m afi.database
```

ستظهر رسالة: `✓ Database initialized successfully`

## الخطوة 6: إنشاء ملف الإعدادات

```bash
cp config/.env.example config/.env
```

قم بتحرير `config/.env` وضع قيمك الخاصة:

```bash
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct-v0.2-q4_K_M
DEBUG=false
LOG_LEVEL=INFO
```

## الخطوة 7: تثبيت Ollama (موصى به)

### على Windows و macOS:

1. اذهب إلى https://ollama.ai
2. حمّل المثبت
3. ثبّت كالمعتاد

### على Linux:

```bash
curl https://ollama.ai/install.sh | sh
```

## الخطوة 8: تحميل نموذج اللغة

افتح terminal/cmd جديد:

```bash
# تشغيل خادم Ollama
ollama serve
```

في terminal آخر:

```bash
# تحميل النموذج الموصى به
ollama pull mistral:7b-instruct-v0.2-q4_K_M
```

أو اختر نموذج آخر حسب ذاكرة الفيديو:

```bash
# إذا كان لديك 4GB VRAM
ollama pull mistral:7b-instruct-v0.2-q4_K_M

# إذا كان لديك 2GB VRAM أو أقل
ollama pull phi:2.2-chat-q4

# أسرع (متطلبات منخفضة)
ollama pull neural-chat:7b-v3-q4
```

## الخطوة 9: تشغيل الخادم

في terminal جديد (مع تفعيل البيئة الافتراضية):

```bash
python -m afi.server.main
```

ستظهر رسالة مثل:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## الخطوة 10: فحص صحة النظام

```bash
curl http://localhost:8000/health
```

ستحصل على:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "ai_provider": "ollama"
}
```

## الخطوة 11: تشغيل الاختبارات

```bash
# جميع الاختبارات
pytest

# اختبارات معينة
pytest tests/unit/
pytest tests/financial_logic/
pytest tests/security/
```

## الاستخدام الأساسي

### التحقق من صحة النظام

```bash
curl http://localhost:8000/api/health/status
```

### إنشاء محفظة

```python
from afi.core.portfolio import Portfolio

portfolio = Portfolio(
    portfolio_id="my-portfolio",
    name="محفظتي",
    cash=10000.0,
    base_currency="EGP"
)

# إضافة موضع
portfolio.add_position(
    ticker="HRHO",
    quantity=100.0,
    entry_price=8.25
)

print(f"إجمالي القيمة: {portfolio.total_value} EGP")
```

### فحص المخاطر

```python
from afi.core.risk import RiskProfile, RiskEngine

profile = RiskProfile(
    capital=500.0,
    risk_tolerance=0.10,  # 10%
    time_horizon_days=7
)

engine = RiskEngine()
is_valid, warnings = engine.validate_risk_profile(profile)

if is_valid:
    max_risk = profile.maximum_risk_budget
    print(f"الحد الأقصى للمخاطرة: {max_risk} EGP")
```

### اختبار الاستراتيجية

```python
from afi.engines.backtesting import BacktestEngine
from datetime import datetime, timedelta

engine = BacktestEngine(initial_capital=10000.0)

def simple_strategy(prices, index):
    # تحريك متوسط بسيط
    if index < 20:
        return "hold"
    
    avg_20 = sum(p["close"] for p in prices[index-20:index]) / 20
    current = prices[index]["close"]
    
    if current > avg_20:
        return "buy"
    else:
        return "sell"

result = engine.run_backtest(
    strategy_name="MA20",
    ticker="HRHO",
    historical_prices=prices,
    strategy_func=simple_strategy
)

print(f"العائد الإجمالي: {result.total_return}%")
print(f"نسبة Sharpe: {result.sharpe_ratio}")
print(f"أقصى انخفاض: {result.max_drawdown}%")
```

## استكشاف الأخطاء

انظر إلى `docs/TROUBLESHOOTING.md` للمزيد من المساعدة.

## المساعدة والدعم

- توثيق المشروع: `/docs`
- قضايا المشروع: GitHub Issues
- النقاشات: GitHub Discussions

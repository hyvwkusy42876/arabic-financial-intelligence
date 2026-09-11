# دليل التحميل والتثبيت

## قائمة المحتويات

### 📂 البنية الأساسية
```
arabic-financial-intelligence/
├── afi/                    # حزمة التطبيق الرئيسية
│   ├── core/              # المحركات المالية
│   ├── database/          # قاعدة البيانات
│   ├── providers/         # مزودو البيانات
│   ├── agents/            # وكلاء الذكاء الاصطناعي
│   ├── engines/           # المحركات المتخصصة
│   ├── utils/             # أدوات المساعدة
│   └── server/            # خادم FastAPI
├── tests/                 # مجموعة الاختبارات
├── docs/                  # التوثيق
├── config/                # ملفات الإعدادات
├── scripts/               # نصوص مساعدة
├── requirements.txt       # المتطلبات
├── README.md              # الملف التعريفي
├── SETUP_AR.md            # إرشادات التثبيت
└── FINAL_REPORT.md        # الملخص النهائي
```

## 📥 خطوات التحميل والتثبيت

### 1️⃣ تحميل الملف

#### الطريقة الأولى: من GitHub مباشرة
```bash
git clone https://github.com/hyvwkusy42876/arabic-financial-intelligence.git
cd arabic-financial-intelligence
```

#### الطريقة الثانية: تحميل الملف المضغوط
```bash
# اذهب إلى https://github.com/hyvwkusy42876/arabic-financial-intelligence
# اضغط على "Code" ثم "Download ZIP"
# استخرج الملف المضغوط
unzip arabic-financial-intelligence-main.zip
cd arabic-financial-intelligence-main
```

### 2️⃣ التثبيت على Windows

#### الخطوة 1: التحقق من Python
```cmd
python --version
REM يجب أن يكون 3.11 أو أحدث
```

#### الخطوة 2: إنشاء بيئة افتراضية
```cmd
python -m venv venv
venv\Scripts\activate
```

#### الخطوة 3: تثبيت المتطلبات
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

#### الخطوة 4: تهيئة قاعدة البيانات
```cmd
python -m afi.database
```

#### الخطوة 5: نسخ الإعدادات
```cmd
copy config\.env.example config\.env
REM عدّل config\.env حسب احتياجاتك
```

#### الخطوة 6: تشغيل الاختبارات
```cmd
pytest
```

#### الخطوة 7: تشغيل الخادم
```cmd
python -m afi.server.main
```

سيظهر:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3️⃣ التثبيت على Linux/macOS

#### الخطوة 1: التحقق من Python
```bash
python3 --version
# يجب أن يكون 3.11 أو أحدث
```

#### الخطوة 2: إنشاء بيئة افتراضية
```bash
python3 -m venv venv
source venv/bin/activate
```

#### الخطوة 3: تثبيت المتطلبات
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### الخطوة 4: تهيئة قاعدة البيانات
```bash
python -m afi.database
```

#### الخطوة 5: نسخ الإعدادات
```bash
cp config/.env.example config/.env
# عدّل config/.env حسب احتياجاتك
```

#### الخطوة 6: تشغيل الاختبارات
```bash
pytest
```

#### الخطوة 7: تشغيل الخادم
```bash
python -m afi.server.main
```

## 🔧 تثبيت Ollama (اختياري لكن موصى به)

### Windows/macOS:
1. اذهب إلى https://ollama.ai
2. حمّل المثبت
3. ثبّت البرنامج
4. افتح Terminal/CMD وشغّل:

```bash
ollama serve
```

### Linux:
```bash
curl https://ollama.ai/install.sh | sh
ollama serve
```

### في Terminal آخر:
```bash
# تحميل النموذج الموصى به
ollama pull mistral:7b-instruct-v0.2-q4_K_M

# أو اختر نموذج أخف
ollama pull phi:2.2-chat-q4
```

## ✅ التحقق من التثبيت

```bash
# 1. فحص صحة النظام
python scripts/health_check.py

# 2. اختبار الاستيراد
python -c "from afi.core.risk import RiskEngine; print('✓ All imports work!')"

# 3. فحص الخادم
curl http://localhost:8000/health
```

## 🧪 تشغيل الاختبارات

```bash
# جميع الاختبارات
pytest

# اختبارات محددة
pytest tests/unit/
pytest tests/financial_logic/
pytest tests/security/

# مع تقرير التغطية
pytest --cov=afi tests/
```

## 📖 الملفات المهمة

| الملف | الوصف |
|------|-------|
| `README.md` | نظرة عامة على المشروع |
| `SETUP_AR.md` | إرشادات التثبيت بالعربية |
| `FINAL_REPORT.md` | الملخص الشامل |
| `docs/TROUBLESHOOTING_AR.md` | حل المشاكل الشائعة |
| `docs/MODELS_AR.md` | دليل نماذج Ollama |
| `requirements.txt` | المتطلبات الكاملة |
| `pyproject.toml` | إعدادات المشروع |
| `config/.env.example` | نموذج الإعدادات |

## 🚀 الاستخدام الأساسي

### إنشاء محفظة
```python
from afi.core.portfolio import Portfolio

portfolio = Portfolio(
    portfolio_id="my-portfolio",
    name="محفظتي",
    cash=10000.0,
    base_currency="EGP"
)

# إضافة مركز
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
max_risk = profile.maximum_risk_budget
print(f"الحد الأقصى للمخاطرة: {max_risk} EGP")
```

### اختبار استراتيجية
```python
from afi.engines.backtesting import BacktestEngine

engine = BacktestEngine(initial_capital=10000.0)

def simple_strategy(prices, index):
    if index < 20:
        return "hold"
    avg_20 = sum(p["close"] for p in prices[index-20:index]) / 20
    return "buy" if prices[index]["close"] > avg_20 else "sell"

result = engine.run_backtest(
    strategy_name="MA20",
    ticker="HRHO",
    historical_prices=prices,
    strategy_func=simple_strategy
)

print(f"العائد الإجمالي: {result.total_return}%")
print(f"نسبة Sharpe: {result.sharpe_ratio}")
```

## 🔗 المراجع السريعة

### المتطلبات الأدنى:
- Python 3.11+
- 2GB RAM
- 500MB مساحة قرص

### المتطلبات المثالية:
- Python 3.11+
- 16GB RAM
- RTX 3050 4GB VRAM
- NVMe SSD
- اتصال إنترنت (اختياري)

## 💬 الحصول على المساعدة

### المشاكل الشائعة:
1. "ModuleNotFoundError" → تأكد من تفعيل البيئة الافتراضية
2. "Database is locked" → احذف afi_data.db وأعد التهيئة
3. "Ollama connection failed" → تأكد من تشغيل ollama serve
4. "Memory error" → استخدم نموذج أخف (phi بدل mistral)

### الدعم:
- 📖 اقرأ `docs/TROUBLESHOOTING_AR.md`
- 🐛 أبلغ عن الأخطاء على GitHub Issues
- 💬 اطرح الأسئلة على GitHub Discussions

## 📝 ملاحظات مهمة

⚠️ **هذا نظام دعم قرار وبحث فقط، وليس ضمان أرباح مالية**

- جميع الاستثمارات تحمل مخاطر
- الأداء السابق لا يضمن النتائج المستقبلية
- استشر خبير مالي مؤهل قبل اتخاذ قرارات استثمارية

## 📄 الترخيص

MIT License - انظر LICENSE للتفاصيل

---

**النسخة**: 0.1.0 (تطوير نشط)  
**آخر تحديث**: سبتمبر 2026  
**الجهاز المستهدف**: RTX 3050 Laptop (4GB VRAM) + 16GB RAM  
**اللغة**: عربي أولاً 🇸🇦

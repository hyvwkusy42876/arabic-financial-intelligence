# استكشاف الأخطاء والمشاكل الشائعة

## مشاكل Ollama

### المشكلة: لا يمكن الاتصال بـ Ollama

**الأعراض:**
```
Error: Failed to connect to Ollama at http://localhost:11434
```

**الحل:**

1. تأكد من تشغيل خادم Ollama:
```bash
ollama serve
```

2. تحقق من أن الخادم يعمل على الميناء الصحيح:
```bash
curl http://localhost:11434/api/tags
```

3. إذا لم ينجح، أعد تثبيت Ollama:
```bash
# Windows
msiexec /i ollama-installer.msi

# macOS
brew reinstall ollama

# Linux
curl https://ollama.ai/install.sh | sh
```

### المشكلة: النموذج لم يتم تنزيله

**الحل:**
```bash
ollama pull mistral:7b-instruct-v0.2-q4_K_M

# أو اختر نموذجًا أخف إذا كان لديك ذاكرة محدودة
ollama pull phi:2.2-chat-q4
```

### المشكلة: استخدام ذاكرة عالي جدًا

**الحل:**

1. استخدم نموذجًا أصغر:
```bash
# بدلاً من Mistral 7B
ollama pull neural-chat:7b-v3-q4  # أخف بـ 1GB
ollama pull phi:2.2-chat-q4       # الأخف (1.5GB)
```

2. حد من حجم السياق في `config/.env`:
```
MAX_CONTEXT_LENGTH=1024
BATCH_SIZE=1
```

## مشاكل قاعدة البيانات

### المشكلة: "database disk image is malformed"

**الحل:**
```bash
# احذف قاعدة البيانات القديمة
rm afi_data.db

# أعد تهيئة قاعدة البيانات
python -m afi.database
```

### المشكلة: الاتصال مرفوض

**الحل:**
```bash
# تحقق من أن البيانات في المسار الصحيح
ls -la afi_data.db  # Linux/macOS
dir afi_data.db     # Windows

# إذا لم توجد، أنشئها
python -m afi.database.init
```

## مشاكل التثبيت

### المشكلة: "ModuleNotFoundError: No module named 'afi'"

**الحل:**

1. تأكد من أنك في المجلد الصحيح:
```bash
cd arabic-financial-intelligence
```

2. تأكد من تفعيل البيئة الافتراضية:
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. أعد تثبيت المتطلبات:
```bash
pip install -e .
```

### المشكلة: "pip: command not found"

**الحل:**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt
```

## مشاكل الأداء

### المشكلة: التطبيق بطيء جدًا

**الحل:**

1. تحقق من استخدام الموارد:
```bash
# Linux/macOS
top

# Windows
tasklist
```

2. قلل حجم السياق:
```
MAX_CONTEXT_LENGTH=1024
```

3. استخدم نموذجًا أسرع:
```bash
ollama pull phi:2.2-chat-q4
```

4. فعّل التخزين المؤقت:
```
CACHE_ENABLED=true
CACHE_TTL_SECONDS=300
```

### المشكلة: استخدام GPU مرتفع

**الحل:**

1. تحقق من إصدار NVIDIA:
```bash
nvidia-smi
```

2. قلل من استخدام VRAM في `config/.env`:
```
GPU_ENABLED=true
MAX_VRAM_GB=2  # بدلاً من 4
```

3. استخدم CPU بدلاً من GPU:
```
GPU_ENABLED=false
```

## مشاكل بيانات السوق

### المشكلة: "No market data available"

**الحل:**

1. تحقق من اتصالك بالإنترنت

2. جرب مزود البيانات الوهمي للاختبار:
```
MARKET_DATA_PROVIDER=mock
```

3. تحقق من صحة رمز السهم:
```python
from afi.providers.mock import MockMarketDataProvider

provider = MockMarketDataProvider()
quote = provider.get_quote("HRHO")  # يجب أن يعمل
```

## مشاكل الاختبارات

### المشكلة: "pytest: command not found"

**الحل:**
```bash
pip install pytest pytest-cov
pytest --version
```

### المشكلة: "FAILED - AssertionError"

**الحل:**
```bash
# شغّل الاختبارات بتفاصيل أكثر
pytest -v --tb=long

# شغّل اختبار واحد
pytest tests/unit/test_calculator.py::TestPortfolioCalculator::test_calculate_allocation -v
```

## مشاكل اللغة العربية

### المشكلة: أحرف عربية مشوهة

**الحل:**

1. تأكد من ترميز UTF-8:
```bash
# Linux/macOS
export PYTHONIOENCODING=utf-8

# Windows PowerShell
$env:PYTHONIOENCODING='utf-8'
```

2. تحقق من إعدادات المحرر:
- استخدم UTF-8 للملفات
- قم بحفظ الملفات بصيغة UTF-8

## الحصول على المساعدة

### أين تجد الدعم:

1. **التوثيق**: `/docs` في المستودع
2. **مشاكل GitHub**: https://github.com/hyvwkusy42876/arabic-financial-intelligence/issues
3. **النقاشات**: https://github.com/hyvwkusy42876/arabic-financial-intelligence/discussions

### معلومات مفيدة عند الإبلاغ عن المشاكل:

```bash
# إصدار Python
python --version

# الملفات المثبتة
pip list

# رسائل الخطأ الكاملة
# (انسخ النص كاملاً من الـ terminal)

# نظام التشغيل
uname -a  # Linux/macOS
ver       # Windows
```

## التحقق من صحة التثبيت

```bash
# 1. تحقق من Python
python --version  # يجب أن يكون 3.11+

# 2. تحقق من قاعدة البيانات
ls afi_data.db  # يجب أن توجد

# 3. تحقق من البيئة الافتراضية
which python  # يجب أن يشير إلى venv

# 4. تشغيل اختبار سريع
python -c "from afi.core.risk import RiskEngine; print('✓ Import successful')"

# 5. تحقق من صحة النظام
curl http://localhost:8000/health  # بعد تشغيل الخادم
```

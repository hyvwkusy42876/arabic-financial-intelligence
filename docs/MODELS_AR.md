# نموذج تعليمات Ollama

## اختيار النموذج المناسب لجهازك

### جهازك: RTX 3050 Laptop (4GB VRAM) + 16GB RAM

#### ✅ الخيار الأول (موصى به): Mistral 7B

```bash
ollama pull mistral:7b-instruct-v0.2-q4_K_M
```

**المميزات:**
- حجم: 5.5GB
- جودة عالية جدًا
- فهم عميق للعربية
- سرعة معقولة
- متطلبات مقبولة

**الأداء المتوقع:**
- وقت الاستجابة: 5-15 ثانية (حسب السؤال)
- VRAM المستخدم: 3-4GB
- RAM المستخدم: 2-3GB

#### ✅ الخيار الثاني: Neural Chat 7B

```bash
ollama pull neural-chat:7b-v3-q4
```

**المميزات:**
- حجم: 4.8GB
- جودة جيدة جدًا
- متخصص في المحادثات
- أسرع قليلاً من Mistral
- استهلاك موارد أقل

**الأداء المتوقع:**
- وقت الاستجابة: 4-12 ثانية
- VRAM المستخدم: 3.5GB
- RAM المستخدم: 2GB

#### ✅ الخيار الثالث (الأخف): Phi 2

```bash
ollama pull phi:2.2-chat-q4
```

**المميزات:**
- حجم: 1.5GB فقط!
- سرعة عالية جدًا
- استهلاك موارد منخفض جدًا
- جودة مقبولة
- مثالي للأجهزة المحدودة

**الأداء المتوقع:**
- وقت الاستجابة: 2-5 ثواني
- VRAM المستخدم: 1-2GB
- RAM المستخدم: 500MB-1GB

#### الخيار الرابع: Llama 2

```bash
ollama pull llama2:7b-chat-q4
```

**المميزات:**
- حجم: 5.5GB
- نموذج قياسي
- جودة جيدة
- معروف وموثوق

## خطوات التثبيت

### 1. تثبيت Ollama

#### على Windows:
```bash
# انتقل إلى https://ollama.ai
# انقر على Download
# قم بتشغيل المثبت
# اتبع تعليمات التثبيت
```

#### على macOS:
```bash
brew install ollama
# أو انتقل إلى https://ollama.ai وحمل المثبت
```

#### على Linux:
```bash
curl https://ollama.ai/install.sh | sh
```

### 2. بدء خادم Ollama

```bash
ollama serve
```

ستظهر رسالة:
```
Listening on 127.0.0.1:11434
```

### 3. تنزيل النموذج

افتح terminal/cmd جديد واختر أحد الخيارات أعلاه:

```bash
# الخيار الموصى به
ollama pull mistral:7b-instruct-v0.2-q4_K_M
```

انتظر حتى ينتهي التنزيل (قد يستغرق 10-30 دقيقة حسب سرعة الإنترنت).

### 4. اختبر النموذج

```bash
ollama run mistral:7b-instruct-v0.2-q4_K_M
```

اكتب شيئًا واضغط Enter:
```
>>> مرحبا، كيف حالك؟
```

إذا حصلت على رد، فالنموذج يعمل بشكل صحيح!

اكتب `exit` للخروج.

## تكوين التطبيق

عدّل `config/.env`:

```bash
# لاستخدام Mistral (موصى به)
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct-v0.2-q4_K_M
OLLAMA_TIMEOUT=120

# أو لاستخدام Phi (الأخف)
# OLLAMA_MODEL=phi:2.2-chat-q4
# OLLAMA_TIMEOUT=60

# أو لاستخدام Neural Chat
# OLLAMA_MODEL=neural-chat:7b-v3-q4
# OLLAMA_TIMEOUT=90
```

## مراقبة الأداء

### على Windows:

افتح Task Manager (Ctrl+Shift+Esc):
- CPU: يجب أن يكون أقل من 80%
- Memory: يجب أن يكون أقل من 80%
- GPU Memory: راقب استخدام VRAM

### على Linux/macOS:

```bash
# مراقبة حية
top

# أو استخدم
htop
```

## معالجة المشاكل

### إذا كان النموذج بطيئًا جدًا:

1. قلل حجم السياق في `config/.env`:
```
MAX_CONTEXT_LENGTH=1024
```

2. استخدم نموذجًا أخف (Phi بدلاً من Mistral)

3. تأكد من عدم تشغيل برامج أخرى على الخلفية

### إذا حصلت على خطأ VRAM:

1. أغلق برامج أخرى تستخدم GPU

2. استخدم نموذجًا أخف:
```bash
ollama pull phi:2.2-chat-q4
```

3. عطّل GPU وشغّل على CPU:
```
GPU_ENABLED=false
```

### إذا لم ينزل النموذج:

```bash
# احذف النموذج
ollama rm mistral:7b-instruct-v0.2-q4_K_M

# حاول مرة أخرى
ollama pull mistral:7b-instruct-v0.2-q4_K_M
```

## المزيد من النماذج

ستجد المزيد على https://ollama.ai/library

### بدائل عربية جيدة:

```bash
# أرابيا (نموذج متخصص)
ollama pull arabicllama2:7b-chat-q4

# Falcon
ollama pull falcon:7b-instruct-q4_K_M
```

## اختبار النموذج مع التطبيق

```bash
# 1. تأكد من تشغيل Ollama
ollama serve

# 2. في terminal جديد، شغّل التطبيق
python -m afi.server.main

# 3. في terminal ثالث، اختبر الاتصال
curl http://localhost:8000/api/health/ai

# يجب أن ترى: {"status": "connected" ...}
```

## نصائح للأداء الأمثل

1. **استخدم NVMe SSD**: يحسّن سرعة تحميل النموذج
2. **أغلق البرامج الأخرى**: خاصة التي تستخدم GPU
3. **استخدم سلك Ethernet**: بدلاً من WiFi للتنزيلات الضخمة
4. **شغّل على وقت قليل استخدام**: تجنب أوقات الذروة
5. **تحديث الدرايفرات**: خاصة NVIDIA drivers للأداء الأفضل

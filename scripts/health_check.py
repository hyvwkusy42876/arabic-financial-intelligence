#!/usr/bin/env python
"""التحقق السريع من صحة النظام."""

import sys
import subprocess
from pathlib import Path

print("\n" + "="*60)
print("فحص صحة منصة الذكاء المالي العربية")
print("="*60 + "\n")

checks = {
    "✓ Python 3.11+": lambda: sys.version_info >= (3, 11),
    "✓ قاعدة البيانات موجودة": lambda: Path("afi_data.db").exists(),
    "✓ مجلد afi موجود": lambda: Path("afi").is_dir(),
    "✓ ملف الإعدادات موجود": lambda: Path("config/.env").exists() or Path("config/.env.example").exists(),
    "✓ متطلبات مثبتة": lambda: _check_imports(),
}

def _check_imports():
    """التحقق من المتطلبات المثبتة."""
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        return True
    except ImportError:
        return False

passed = 0
failed = 0

for check, func in checks.items():
    try:
        result = func()
        if result:
            print(f"{check}")
            passed += 1
        else:
            print(f"✗ {check.replace('✓ ', '')}")
            failed += 1
    except Exception as e:
        print(f"✗ {check.replace('✓ ', '')} - خطأ: {e}")
        failed += 1

print(f"\n{passed} نجح, {failed} فشل\n")

if failed == 0:
    print("🎉 جميع الفحوصات نجحت!")
    print("\nيمكنك الآن تشغيل:")
    print("  python -m afi.server.main\n")
    sys.exit(0)
else:
    print("⚠️  توجد مشاكل تحتاج إلى حل")
    print("\nاتبع SETUP_AR.md للتثبيت الصحيح\n")
    sys.exit(1)

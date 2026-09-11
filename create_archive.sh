#!/bin/bash
# إنشاء ملف مضغوط للمشروع

echo "إنشاء ملف مضغوط..."
zip -r arabic-financial-intelligence.zip \
  afi/ \
  frontend/ \
  tests/ \
  config/ \
  docs/ \
  scripts/ \
  requirements.txt \
  pyproject.toml \
  README.md \
  SETUP_AR.md \
  FINAL_REPORT.md \
  LICENSE \
  .gitignore \
  -x "*.pyc" "__pycache__/*" "*.db" ".git/*" "venv/*" "node_modules/*"

echo "✓ تم إنشاء: arabic-financial-intelligence.zip"
echo "الحجم: $(du -h arabic-financial-intelligence.zip | cut -f1)"

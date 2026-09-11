@echo off
REM إنشاء ملف مضغوط للمشروع (Windows)

echo إنشاء ملف مضغوط...

REM استخدام PowerShell لإنشاء ملف مضغوط
powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::CreateFromDirectory('.', 'arabic-financial-intelligence.zip')"

echo ✓ تم إنشاء: arabic-financial-intelligence.zip
echo.
echo يمكنك الآن تحميل الملف من المستودع
pause

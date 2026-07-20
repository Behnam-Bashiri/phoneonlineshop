@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
python -m pip install -r requirements.txt
python src\run_all.py
echo.
echo Done. Open reports\Final_Report.md
pause

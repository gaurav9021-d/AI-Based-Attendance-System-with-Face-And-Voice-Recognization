@echo off
echo Starting SnapClass AI Attendance System...
cd /d "%~dp0ai-attendance-project-app-main" 2>nul || cd /d "%~dp0"
py -m streamlit run app.py
pause

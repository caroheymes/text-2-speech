@echo off
title Text2Speech - Lecteur vocal accessible
echo ========================================================
echo   Lancement de Text2Speech...
echo   Port dedie : 9001
echo ========================================================
echo.
cd /d "%~dp0"
set PYTHONPATH=%~dp0
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
.venv\Scripts\streamlit.exe run src\app.py --server.port 9001 --server.address 0.0.0.0 --server.headless true
pause

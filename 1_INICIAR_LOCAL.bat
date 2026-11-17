@echo off
chcp 65001 >nul
title [BLACK & WHITE STUDIO :8002] Servidor Local
color 0F

echo ================================================================================
echo   BLACK ^& WHITE STUDIO (BARBER · BEAUTY · ACADEMY) - PUERTO 8002
echo ================================================================================
echo.
echo   - Sistema Activo en:     http://localhost:8002
echo   - Documentación API:    http://localhost:8002/docs
echo   - Base de Datos MySQL:   blackandwhite_ecosystem
echo   - WhatsApp Conectado:    +52 1 56 1282 5970
echo.
echo ================================================================================
echo.

cd /d "%~dp0backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
pause

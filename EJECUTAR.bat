@echo off
REM Ejecutar Sistema de Inspeccion Electrica

title Sistema de Inspeccion Electrica
color 0B

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Iniciar servidor
echo.
echo ==========================================
echo   Sistema de Inspeccion Electrica
echo ==========================================
echo.
echo Iniciando servidor...
echo El navegador se abrira automaticamente
echo.
echo Para detener el servidor: Cierra esta ventana
echo.

python run_server.py

pause

@echo off
echo ========================================
echo Sistema de Inspección Eléctrica
echo ========================================
echo.

REM Verificar Python instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado
    echo Por favor instala Python 3.8+ desde python.org
    pause
    exit /b 1
)

REM Verificar/crear entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Verificando dependencias...
pip install -r requirements.txt -q

REM Verificar archivo .env
if not exist ".env" (
    echo Configurando variables de entorno...
    copy .env.example .env
    echo.
    echo IMPORTANTE: Edita el archivo .env y agrega tu GEMINI_API_KEY
    notepad .env
    pause
)

REM Iniciar servidor
echo.
echo Iniciando servidor...
python run_server.py

pause

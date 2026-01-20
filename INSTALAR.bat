@echo off
REM ========================================
REM Instalador Automatico - Sistema de Inspeccion Electrica
REM ========================================

title Instalador - Sistema de Inspeccion Electrica
color 0A

echo.
echo ==========================================
echo   Sistema de Inspeccion Electrica
echo   Instalador Automatico
echo ==========================================
echo.
echo Este instalador configurara todo automaticamente.
echo.
pause

REM Verificar Python
echo.
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo *** ERROR: Python no esta instalado ***
    echo.
    echo Por favor instala Python 3.11 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)
echo OK - Python encontrado

REM Crear entorno virtual
echo.
echo [2/5] Creando entorno virtual...
if exist venv (
    echo Ya existe, omitiendo...
) else (
    python -m venv venv
    echo OK - Entorno virtual creado
)

REM Activar entorno virtual
echo.
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo [4/5] Instalando dependencias...
echo Esto puede tardar 5-10 minutos...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo *** ERROR: Fallo la instalacion de dependencias ***
    pause
    exit /b 1
)
echo OK - Dependencias instaladas

REM Configurar API Key
echo.
echo [5/5] Configuracion de API Key...
if exist .env (
    echo Archivo .env ya existe
) else (
    echo.
    echo ==========================================
    echo   Configuracion de API Key
    echo ==========================================
    echo.
    echo Necesitas una API Key de Google Gemini para usar el sistema.
    echo.
    echo Si aun no tienes una:
    echo 1. Ve a: https://makersuite.google.com/app/apikey
    echo 2. Inicia sesion con tu cuenta de Google
    echo 3. Crea una nueva API Key
    echo 4. Copia la clave
    echo.
    set /p API_KEY="Pega tu API Key aqui: "
    
    echo GEMINI_API_KEY=%API_KEY%> .env
    echo PORT=8080>> .env
    echo DEBUG=False>> .env
    
    echo OK - Configuracion guardada
)

REM Crear acceso directo
echo.
echo Creando acceso directo en el escritorio...
set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\Sistema Inspeccion Electrica.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%EJECUTAR.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Sistema de Inspeccion Electrica" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs

echo.
echo ==========================================
echo   INSTALACION COMPLETADA!
echo ==========================================
echo.
echo Se ha creado un acceso directo en tu escritorio:
echo "Sistema Inspeccion Electrica"
echo.
echo Para usar el sistema:
echo 1. Doble clic en el acceso directo del escritorio
echo 2. El navegador se abrira automaticamente
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul

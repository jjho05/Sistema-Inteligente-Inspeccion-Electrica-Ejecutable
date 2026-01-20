@echo off
REM Script para compilar el ejecutable en Windows

echo ==========================================
echo Compilador de ELECTRICA para Windows
echo ==========================================
echo.

REM Verificar PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo Compilando ejecutable...
echo Esto puede tardar 10-20 minutos...
echo.

REM Limpiar builds anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Compilar
pyinstaller ELECTRICA.spec

if %errorlevel% == 0 (
    echo.
    echo ==========================================
    echo Compilacion exitosa!
    echo ==========================================
    echo.
    echo Ejecutable creado en: dist\ELECTRICA.exe
    echo.
    echo Para distribuir:
    echo 1. Copia el archivo dist\ELECTRICA.exe
    echo 2. Compartelo con los usuarios
    echo 3. Los usuarios solo hacen doble clic
    echo.
) else (
    echo.
    echo Error en la compilacion
    echo Revisa los errores arriba
)

pause

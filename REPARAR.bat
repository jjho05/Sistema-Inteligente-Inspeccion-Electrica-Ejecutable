@echo off
echo ==========================================
echo   REPARADOR DE INSTALACION (V4 - ESTABLE)
echo ==========================================

echo [1/4] Limpiando entorno previo...
if exist venv (
    RD /S /Q venv
)

echo [2/4] Creando nuevo entorno virtual...
python -m venv venv

echo [3/4] Actualizando instalador...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel

echo [4/4] Instalando dependencias (VERSION MEJORADA)...
:: Instalamos primero numpy y scikit-learn que son las bases
pip install numpy<2.0.0
pip install scikit-learn
pip install -r requirements.txt

echo.
echo ==========================================
echo   PROCESO TERMINADO!
echo ==========================================
echo Ya puedes iniciar el sistema con EJECUTAR.bat
pause

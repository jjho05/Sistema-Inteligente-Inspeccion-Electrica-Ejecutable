#!/bin/bash
# Instalador Automatico - Sistema de Inspeccion Electrica (Mac)

clear
echo "=========================================="
echo "  Sistema de Inspección Eléctrica"
echo "  Instalador Automático"
echo "=========================================="
echo ""
echo "Este instalador configurará todo automáticamente."
echo ""
read -p "Presiona Enter para continuar..."

# Verificar Python
echo ""
echo "[1/5] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "*** ERROR: Python no está instalado ***"
    echo ""
    echo "Por favor instala Python 3.11 o superior desde:"
    echo "https://www.python.org/downloads/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi
echo "✓ OK - Python encontrado"

# Crear entorno virtual
echo ""
echo "[2/5] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "Ya existe, omitiendo..."
else
    python3 -m venv venv
    echo "✓ OK - Entorno virtual creado"
fi

# Activar entorno virtual
echo ""
echo "[3/5] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo ""
echo "[4/5] Instalando dependencias..."
echo "Esto puede tardar 5-10 minutos..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo ""
    echo "*** ERROR: Falló la instalación de dependencias ***"
    read -p "Presiona Enter para salir..."
    exit 1
fi
echo "✓ OK - Dependencias instaladas"

# Configurar API Key
echo ""
echo "[5/5] Configuración de API Key..."
if [ -f ".env" ]; then
    echo "Archivo .env ya existe"
else
    echo ""
    echo "=========================================="
    echo "   Configuración de API Key"
    echo "=========================================="
    echo ""
    echo "Necesitas una API Key de Google Gemini para usar el sistema."
    echo ""
    echo "Si aún no tienes una:"
    echo "1. Ve a: https://makersuite.google.com/app/apikey"
    echo "2. Inicia sesión con tu cuenta de Google"
    echo "3. Crea una nueva API Key"
    echo "4. Copia la clave"
    echo ""
    read -p "Pega tu API Key aquí: " API_KEY
    
    echo "GEMINI_API_KEY=$API_KEY" > .env
    echo "PORT=8080" >> .env
    echo "DEBUG=False" >> .env
    
    echo "✓ OK - Configuración guardada"
fi

# Crear script de ejecución
echo ""
echo "Creando script de ejecución..."
cat > ejecutar.sh << 'EOF'
#!/bin/bash
clear
echo "=========================================="
echo "  Sistema de Inspección Eléctrica"
echo "=========================================="
echo ""
echo "Iniciando servidor..."
echo "El navegador se abrirá automáticamente"
echo ""
echo "Para detener: Presiona Ctrl+C"
echo ""

source venv/bin/activate
python run_server.py
EOF

chmod +x ejecutar.sh

echo ""
echo "=========================================="
echo "   INSTALACIÓN COMPLETADA!"
echo "=========================================="
echo ""
echo "Para usar el sistema:"
echo "1. Doble clic en 'ejecutar.sh'"
echo "2. El navegador se abrirá automáticamente"
echo ""
echo "O desde terminal:"
echo "./ejecutar.sh"
echo ""
read -p "Presiona Enter para cerrar..."

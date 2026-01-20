#!/bin/bash

echo "========================================"
echo "Sistema de Inspección Eléctrica"
echo "========================================"
echo ""

# Verificar Python instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.8+ desde python.org"
    exit 1
fi

# Verificar/crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Verificando dependencias..."
pip install -r requirements.txt -q

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "Configurando variables de entorno..."
    cp .env.example .env
    echo ""
    echo "IMPORTANTE: Edita el archivo .env y agrega tu GEMINI_API_KEY"
    open -e .env  # Mac
    read -p "Presiona Enter cuando hayas configurado la API key..."
fi

# Iniciar servidor
echo ""
echo "Iniciando servidor..."
python3 run_server.py

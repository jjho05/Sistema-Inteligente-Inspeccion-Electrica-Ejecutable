#!/bin/bash
# Script para compilar el ejecutable en Mac

echo "=========================================="
echo "Compilador de ELECTRICA para Mac"
echo "=========================================="
echo ""

# Verificar que PyInstaller esté instalado
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller no está instalado"
    echo "Instalando PyInstaller..."
    pip install pyinstaller
fi

echo "🔨 Compilando ejecutable..."
echo "⏰ Esto puede tardar 10-20 minutos..."
echo ""

# Limpiar builds anteriores
rm -rf build dist

# Compilar
pyinstaller ELECTRICA.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Compilación exitosa!"
    echo "=========================================="
    echo ""
    echo "📦 Ejecutable creado en: dist/ELECTRICA"
    echo ""
    echo "Para distribuir:"
    echo "1. Copia la carpeta 'dist/ELECTRICA'"
    echo "2. Compártela con los usuarios"
    echo "3. Los usuarios solo hacen doble clic en 'ELECTRICA'"
    echo ""
else
    echo ""
    echo "❌ Error en la compilación"
    echo "Revisa los errores arriba"
fi

# Sistema Inteligente de Inspección Eléctrica

Sistema automatizado basado en IA para análisis de instalaciones eléctricas conforme a la NOM-001-SEDE-2012.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🚀 Instalación

### Requisitos Previos

**Necesitas tener instalado:**
- Python 3.11 o superior
- Conexión a Internet

**¿No tienes Python?**
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11+
3. **Importante (Windows):** Marcar "Add Python to PATH"
4. Instalar y reiniciar PC

---

### Instalación Automática (Recomendada)

#### Windows
1. Descargar este proyecto
2. **Doble clic** en `INSTALAR.bat`
3. Esperar 5-10 minutos (instala todo automáticamente)
4. Ingresar API Key de Gemini cuando lo pida
5. ¡Listo! El navegador se abre automáticamente

#### Mac
1. Descargar este proyecto
2. **Doble clic** en `instalar.command`
3. Si dice "no se puede abrir": Click derecho → Abrir → Confirmar
4. Esperar 5-10 minutos
5. Ingresar API Key de Gemini
6. ¡Listo! El navegador se abre automáticamente

📖 [Guía Detallada de Instalación](INSTALACION_FACIL.md)

---

## 📋 Descripción

Sistema automatizado que analiza imágenes de instalaciones eléctricas y genera dictámenes técnicos profesionales en formato PDF y Word.

**Características:**
- ✅ Análisis visual con IA
- ✅ Detección automática de no conformidades
- ✅ Referencias a NOM-001-SEDE-2012
- ✅ Clasificación de riesgos (Crítico/Medio/Bajo)
- ✅ Dictámenes en PDF y Word
- ✅ Interfaz web fácil de usar

---

## 🎯 Uso del Sistema

### Primera Vez
1. Ejecutar instalador (ver arriba)
2. Ingresar API Key de Gemini
3. El navegador se abre automáticamente

### Siguientes Veces
- **Windows:** Doble clic en `EJECUTAR.bat`
- **Mac:** Doble clic en `ejecutar.command`

### Analizar una Instalación
1. Ingresar tu nombre
2. Cargar imagen (JPG/PNG, < 5 MB)
3. Clic en "Analizar" (30-60 seg)
4. Revisar resultados
5. Descargar dictamen (PDF o Word)

---

## 🔑 API Key de Gemini

**¿Qué es?** Clave gratuita de Google para usar IA

**Cómo obtenerla:**
1. Ir a https://makersuite.google.com/app/apikey
2. Iniciar sesión con Google
3. Clic en "Create API Key"
4. Copiar la clave
5. Pegarla cuando el instalador la pida

**Es gratis** y toma 2 minutos.

---

## 📖 Documentación

- [Instalación Fácil](INSTALACION_FACIL.md) - Paso a paso simple
- [Manual de Usuario](docs/USER_MANUAL.md) - Cómo usar el sistema
- [Manual de Instalación](docs/INSTALLATION.md) - Guía técnica detallada
- [Documentación Técnica](docs/TECHNICAL_DOCS.md) - Para desarrolladores

---

## 📊 ¿Qué Genera el Sistema?

### 1. Resumen en Pantalla
- Clasificación (Conforme/No Conforme)
- Lista de no conformidades por severidad
- Detalles expandibles

### 2. Dictamen PDF
- Documento profesional
- Para imprimir o compartir
- Formato inmutable

### 3. Dictamen Word
- Documento editable
- Para modificar o copiar/pegar
- Mantiene formato

**Cada dictamen incluye:**
- Análisis detallado
- Referencias a artículos NOM-001-SEDE-2012
- Clasificación de riesgos
- Recomendaciones de corrección
- Conclusiones técnicas

---

## 📁 Archivos del Proyecto

```
Sistema-Inteligente-Inspeccion-Electrica/
├── INSTALAR.bat          # Instalador Windows
├── EJECUTAR.bat          # Ejecutar Windows
├── instalar.command      # Instalador Mac
├── instalar.sh           # Instalador Mac (terminal)
├── backend/              # Código del servidor
├── frontend/             # Interfaz web
├── data/                 # Datos y archivos generados
└── docs/                 # Documentación
```

---

## � Compilar Ejecutable (Avanzado)

**Para usuarios que quieren crear un ejecutable sin Python:**

### Requisitos
- Python 3.11+ instalado
- PyInstaller
- Windows (para .exe) o Mac (para .app)

### Pasos

#### Windows
```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
cd Sistema-Inteligente-Inspeccion-Electrica
build_windows.bat

# Esperar 10-20 minutos
# Resultado: dist/ELECTRICA.exe (~200 MB)
```

#### Mac
```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
cd Sistema-Inteligente-Inspeccion-Electrica
./build_mac.sh

# Esperar 10-20 minutos
# Resultado: dist/ELECTRICA (~200 MB)
```

### Usar el Ejecutable

Una vez compilado:
1. El archivo está en `dist/ELECTRICA.exe` (o `dist/ELECTRICA`)
2. Puedes copiarlo a cualquier PC
3. Doble clic y funciona (sin necesidad de Python)
4. Primera vez pide API Key

**Ventaja:** Puedes compartir solo el `.exe` con otros usuarios que no tienen Python.

**Nota:** Solo puedes compilar para el sistema operativo donde estás. Para crear `.exe` necesitas Windows, para `.app` necesitas Mac.

---

## �📋 Requisitos

- **Python:** 3.11 o superior
- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Espacio:** 2 GB libre
- **Internet:** Conexión estable
- **API Key:** Google Gemini (gratis)

---

## 🛠️ Tecnologías

- Python 3.11, Flask
- Google Gemini AI
- ChromaDB (base de datos vectorial)
- ReportLab (PDF), python-docx (Word)
- HTML5, CSS3, JavaScript

---

## ⚠️ Notas Importantes

- ✅ Los dictámenes deben ser revisados por personal calificado
- ✅ La precisión depende de la calidad de las imágenes
- ✅ Requiere conexión a Internet
- ✅ Archivos se eliminan después de 120 días
- ✅ Cada usuario usa su propia API Key

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Abre Pull Request

---

## 📞 Soporte

¿Problemas? Abre un [Issue](../../issues)

---

## 📝 Licencia

Licencia MIT

---

## 🎓 Créditos

Desarrollado como herramienta de apoyo para inspectores eléctricos profesionales en México.

---

**Nota:** Este sistema es una herramienta de apoyo. La validación final debe ser realizada por personal técnico calificado.

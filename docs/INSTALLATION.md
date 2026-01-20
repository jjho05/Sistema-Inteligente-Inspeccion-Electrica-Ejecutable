# Manual de Instalación

Guía completa para instalar y configurar el Sistema de Inspección Eléctrica.

## 📋 Requisitos del Sistema

### Hardware Mínimo
- **Procesador:** Dual-core 2.0 GHz o superior
- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Almacenamiento:** 2 GB de espacio libre
- **Conexión:** Internet estable

### Software Requerido
- **Python:** 3.11 o superior
- **pip:** Gestor de paquetes de Python
- **Navegador:** Chrome, Firefox, Safari o Edge (versión reciente)

### Cuenta de Google Cloud
- Cuenta activa de Google Cloud
- API de Gemini habilitada
- API Key generada

---

## 🔧 Instalación Paso a Paso

### 1. Obtener API Key de Gemini

1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Iniciar sesión con cuenta de Google
3. Crear nueva API Key
4. Copiar la clave generada

### 2. Descargar el Proyecto

**Opción A: Clonar repositorio (recomendado)**
```bash
git clone <repository-url>
cd ELECTRICA
```

**Opción B: Descargar ZIP**
1. Descargar archivo ZIP del repositorio
2. Extraer en ubicación deseada
3. Abrir terminal en la carpeta extraída

### 3. Configurar Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota:** La instalación puede tardar 5-10 minutos dependiendo de la conexión.

### 5. Configurar Variables de Entorno

1. **Copiar archivo de ejemplo:**
```bash
cp .env.example .env
```

2. **Editar archivo `.env`:**
```env
# API Key de Google Gemini (REQUERIDO)
GEMINI_API_KEY=tu_api_key_aqui

# Puerto del servidor (opcional, default: 8080)
PORT=8080

# Modo debug (opcional, default: False)
DEBUG=False
```

3. **Guardar cambios**

### 6. Preparar Base de Conocimiento

El sistema requiere los PDFs de la NOM-001-SEDE-2012:

1. Crear carpeta si no existe:
```bash
mkdir -p data/noms
```

2. Colocar archivos PDF de la norma en `data/noms/`

**Archivos esperados:**
- `NOM-001-SEDE-2012.pdf` (o similar)

### 7. Iniciar el Sistema

**Windows:**
```bash
iniciar.bat
```

**Mac/Linux:**
```bash
chmod +x iniciar.sh
./iniciar.sh
```

El sistema:
1. Verificará la configuración
2. Inicializará la base de conocimiento
3. Limpiará archivos antiguos (>120 días)
4. Abrirá el navegador automáticamente en `http://localhost:8080`

---

## ✅ Verificación de Instalación

### Prueba Básica

1. **Verificar que el servidor inició:**
```
✓ Sistema de Inspección Eléctrica
✓ Configuration validated
✓ Initializing system...
✓ Server starting on http://localhost:8080
```

2. **Abrir navegador en:** `http://localhost:8080`

3. **Verificar interfaz:**
   - ✅ Selector de tipo de instalación visible
   - ✅ Campo de nombre del inspector
   - ✅ Área de carga de imagen
   - ✅ Sin errores en consola del navegador

### Prueba de Análisis

1. Seleccionar tipo: "Residencial"
2. Ingresar nombre: "Inspector Prueba"
3. Cargar imagen de prueba
4. Hacer clic en "Analizar Instalación"
5. Verificar que aparezcan resultados

---

## 🔍 Solución de Problemas

### Error: "GEMINI_API_KEY not found"

**Causa:** API Key no configurada  
**Solución:**
```bash
# Verificar archivo .env
cat .env

# Debe contener:
GEMINI_API_KEY=tu_clave_real_aqui
```

### Error: "ModuleNotFoundError"

**Causa:** Dependencias no instaladas  
**Solución:**
```bash
pip install -r requirements.txt --upgrade
```

### Error: "Port 8080 already in use"

**Causa:** Puerto ocupado  
**Solución:**
```bash
# Opción 1: Cambiar puerto en .env
PORT=8081

# Opción 2: Liberar puerto 8080
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8080 | xargs kill -9
```

### Error: "Permission denied" (Mac/Linux)

**Causa:** Script sin permisos de ejecución  
**Solución:**
```bash
chmod +x iniciar.sh
./iniciar.sh
```

### El navegador no se abre automáticamente

**Solución:**
```bash
# Iniciar sin abrir navegador
python run_server.py --no-browser

# Luego abrir manualmente:
# http://localhost:8080
```

### Análisis muy lento

**Causas posibles:**
- Conexión lenta a Internet
- Imagen muy grande
- Primera ejecución (carga modelos)

**Soluciones:**
- Reducir tamaño de imagen (< 5MB)
- Verificar conexión a Internet
- Esperar en primera ejecución (~2 min)

---

## 🔄 Actualización del Sistema

### Actualizar Código

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Actualizar Dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Limpiar Caché

```bash
# Eliminar archivos temporales
rm -rf __pycache__
rm -rf backend/__pycache__
rm -rf backend/*/__pycache__

# Eliminar base de datos vectorial (se regenerará)
rm -rf data/chroma_db
```

---

## 🗑️ Desinstalación

### Desactivar Entorno Virtual

```bash
deactivate
```

### Eliminar Archivos

```bash
# Eliminar entorno virtual
rm -rf venv

# Eliminar archivos generados
rm -rf data/generated/*
rm -rf data/chroma_db

# Eliminar proyecto completo
cd ..
rm -rf ELECTRICA
```

---

## 📞 Soporte Técnico

Si encuentras problemas durante la instalación:

1. Verificar que cumples con todos los requisitos
2. Revisar logs de error en la terminal
3. Consultar sección de solución de problemas
4. Reportar issue en GitHub con:
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir

---

## ✨ Próximos Pasos

Una vez instalado correctamente:

1. Leer [Manual de Usuario](USER_MANUAL.md)
2. Realizar análisis de prueba
3. Revisar [Documentación Técnica](TECHNICAL_DOCS.md) (opcional)

---

**Nota:** La primera ejecución puede tardar más tiempo debido a la descarga de modelos de IA.

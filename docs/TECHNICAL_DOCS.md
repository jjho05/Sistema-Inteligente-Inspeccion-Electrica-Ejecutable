# Documentación Técnica

Documentación técnica completa del Sistema de Inspección Eléctrica.

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Componentes Principales](#componentes-principales)
3. [Flujo de Datos](#flujo-de-datos)
4. [APIs y Endpoints](#apis-y-endpoints)
5. [Base de Datos y Almacenamiento](#base-de-datos-y-almacenamiento)
6. [Configuración Avanzada](#configuración-avanzada)
7. [Desarrollo y Contribución](#desarrollo-y-contribución)

---

## 🏗️ Arquitectura del Sistema

### Visión General

```
┌─────────────────────────────────────────┐
│         FRONTEND (Web UI)               │
│  - HTML/CSS/JavaScript                  │
│  - Interfaz de usuario                  │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
┌──────────────▼──────────────────────────┐
│         BACKEND (Flask Server)          │
│  ┌────────────────────────────────────┐ │
│  │  API Endpoints                     │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Agents (IA Processing)            │ │
│  │  - VisionAgent                     │ │
│  │  - NormativeAgent                  │ │
│  │  - IntegratorAgent                 │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  RAG System                        │ │
│  │  - Vector Store (ChromaDB)         │ │
│  │  - Embeddings                      │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Document Generators               │ │
│  │  - PDF Generator                   │ │
│  │  - Word Generator                  │ │
│  └────────────────────────────────────┘ │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     EXTERNAL SERVICES                   │
│  - Google Gemini API                    │
│  - Sentence Transformers                │
└─────────────────────────────────────────┘
```

### Capas del Sistema

1. **Capa de Presentación** (Frontend)
   - Interfaz web responsive
   - Manejo de eventos de usuario
   - Visualización de resultados

2. **Capa de Aplicación** (Backend)
   - API REST con Flask
   - Orquestación de agentes
   - Lógica de negocio

3. **Capa de IA** (Agents + RAG)
   - Procesamiento de imágenes
   - Análisis normativo
   - Generación de contenido

4. **Capa de Datos**
   - Almacenamiento vectorial
   - Archivos generados
   - Caché de embeddings

---

## 🔧 Componentes Principales

### Backend

#### 1. Agentes de IA (`backend/agents/`)

**VisionAgent** (`vision_agent.py`)
- Analiza imágenes con Gemini Vision
- Detecta elementos de instalación
- Identifica no conformidades
- Genera descripciones detalladas

```python
class VisionAgent:
    def analyze_image(self, image_path: str, installation_type: str) -> Dict
    def _build_prompt(self, installation_type: str) -> str
```

**NormativeAgent** (`normative_agent.py`)
- Busca artículos aplicables en la NOM
- Valida referencias normativas
- Proporciona contexto legal

```python
class NormativeAgent:
    def find_applicable_articles(self, non_conformity: str) -> List[str]
    def get_article_context(self, article: str) -> str
```

**IntegratorAgent** (`integrator_agent.py`)
- Integra resultados de otros agentes
- Clasifica no conformidades por severidad
- Genera dictamen final

```python
class IntegratorAgent:
    def integrate_analysis(self, vision_data: Dict, normative_data: Dict) -> Dict
    def classify_severity(self, non_conformity: Dict) -> str
    def generate_dictamen_data(self, analysis: Dict) -> Dict
```

#### 2. Sistema RAG (`backend/rag/`)

**VectorStore** (`vector_store.py`)
- Gestiona base de datos vectorial (ChromaDB)
- Búsqueda semántica de artículos
- Indexación de documentos

```python
class VectorStore:
    def add_documents(self, documents: List[str])
    def search(self, query: str, k: int = 5) -> List[Dict]
    def get_or_create_collection(self) -> Collection
```

**PDFProcessor** (`pdf_processor.py`)
- Extrae texto de PDFs de normas
- Divide en chunks para embeddings
- Preprocesa contenido

```python
class PDFProcessor:
    def process_pdf(self, pdf_path: str) -> List[str]
    def chunk_text(self, text: str, chunk_size: int) -> List[str]
```

**Embeddings** (`embeddings.py`)
- Genera embeddings con Sentence Transformers
- Caché de embeddings para eficiencia
- Modelo: `all-MiniLM-L6-v2`

#### 3. Generadores de Documentos (`backend/utils/`)

**PDFGenerator** (`pdf_generator.py`)
- Genera PDFs con reportlab
- Formato profesional
- Estilos personalizados

```python
class PDFGenerator:
    def generate_dictamen(self, data: Dict) -> str
    def _create_styles(self) -> Dict
    def _add_header(self, story: List, data: Dict)
```

**WordGenerator** (`word_generator.py`)
- Genera documentos Word (.docx)
- Formato editable
- Mantiene estructura del PDF

```python
class WordGenerator:
    def generate_dictamen(self, data: Dict) -> str
    def _add_section(self, doc: Document, title: str, content: str)
```

#### 4. Utilidades (`backend/utils/`)

**FileCleanup** (`file_cleanup.py`)
- Limpieza automática de archivos antiguos
- Retención de 120 días
- Ejecución en inicio del servidor

```python
def cleanup_old_files(directory: str, days: int = 120)
```

**Config** (`config.py`)
- Configuración del sistema
- Variables de entorno
- Validación de configuración

```python
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8080))
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

### Frontend

#### Estructura (`frontend/`)

**index.html**
- Interfaz principal
- Formulario de análisis
- Visualización de resultados

**styles.css** (`css/styles.css`)
- Estilos modernos
- Diseño responsive
- Animaciones

**app.js** (`js/app.js`)
- Lógica de interacción
- Llamadas a API
- Manejo de eventos

```javascript
async function analyzeImage()
async function downloadDictamen()
async function downloadDictamenWord()
function displayResults(data)
```

---

## 🔄 Flujo de Datos

### Análisis de Imagen

```
1. Usuario carga imagen
   ↓
2. Frontend envía POST /api/analyze
   {
     image: base64,
     installation_type: "residential",
     inspector_name: "Juan Pérez"
   }
   ↓
3. Backend procesa:
   a. VisionAgent analiza imagen
   b. DetectionParser extrae NCs
   c. NormativeAgent busca artículos
   d. IntegratorAgent integra resultados
   ↓
4. Backend responde JSON:
   {
     success: true,
     analysis: {
       classification: {...},
       non_conformities: [...],
       conformities: [...],
       summary: "..."
     }
   }
   ↓
5. Frontend muestra resultados
```

### Generación de Dictamen

```
1. Usuario hace clic en "Descargar PDF/Word"
   ↓
2. Frontend envía POST /api/generate-dictamen
   {
     analysis: {...},
     inspection_data: {
       inspector_name: "...",
       folio: "...",
       fecha: "..."
     }
   }
   ↓
3. Backend genera documento:
   a. IntegratorAgent prepara datos
   b. PDFGenerator/WordGenerator crea archivo
   c. Archivo se guarda en data/generated/
   ↓
4. Backend responde:
   {
     success: true,
     filename: "Dictamen_AUTO_..."
   }
   ↓
5. Frontend descarga archivo
   GET /api/download/{filename}
```

---

## 🌐 APIs y Endpoints

### Endpoints Disponibles

#### `GET /`
Sirve la interfaz web principal.

**Response:** HTML

#### `POST /api/analyze`
Analiza una imagen de instalación eléctrica.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "installation_type": "residential|commercial|industrial"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "installation_name": "Instalación Residencial",
    "classification": {
      "status": "NO CONFORME",
      "justification": "..."
    },
    "non_conformities": [
      {
        "description": "...",
        "article": "300-4(B)(1)",
        "severity": "high|medium|low"
      }
    ],
    "conformities": ["..."],
    "summary": "...",
    "recommendations": ["..."]
  }
}
```

#### `POST /api/generate-dictamen`
Genera dictamen en formato PDF.

**Request:**
```json
{
  "analysis": {...},
  "inspection_data": {
    "inspector_name": "Juan Pérez",
    "folio": "AUTO-123456",
    "fecha": "19/01/2026"
  }
}
```

**Response:**
```json
{
  "success": true,
  "document_path": "/path/to/file.pdf",
  "filename": "Dictamen_AUTO_....pdf"
}
```

#### `POST /api/generate-dictamen-word`
Genera dictamen en formato Word.

**Request:** Igual que `/api/generate-dictamen`

**Response:**
```json
{
  "success": true,
  "document_path": "/path/to/file.docx",
  "filename": "Dictamen_AUTO_....docx"
}
```

#### `GET /api/download/<filename>`
Descarga archivo generado.

**Response:** Archivo binario (PDF o DOCX)

---

## 💾 Base de Datos y Almacenamiento

### ChromaDB (Vector Store)

**Ubicación:** `data/chroma_db/`

**Colección:** `nom_articles`

**Estructura:**
```python
{
  "documents": ["Texto del artículo..."],
  "metadatas": [{"article": "300-4", "source": "NOM-001-SEDE-2012"}],
  "ids": ["art_300_4"]
}
```

### Archivos Generados

**Ubicación:** `data/generated/`

**Retención:** 120 días

**Limpieza:** Automática al iniciar servidor

**Nomenclatura:**
```
Dictamen_AUTO-{timestamp}_{fecha}.{ext}
```

### Caché de Embeddings

**Ubicación:** `data/embeddings_cache/`

**Propósito:** Acelerar búsquedas repetidas

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

```env
# API Keys
GEMINI_API_KEY=your_key_here

# Server
HOST=localhost
PORT=8080
DEBUG=False

# RAG
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# File Retention
FILE_RETENTION_DAYS=120
```

### Personalización de Prompts

Editar `backend/vision/prompt_templates.py`:

```python
ANALYSIS_PROMPT = """
Analiza la siguiente imagen de una instalación eléctrica {installation_type}.
...
"""
```

### Ajuste de Modelos

Cambiar modelo de embeddings en `backend/rag/embeddings.py`:

```python
MODEL_NAME = "all-MiniLM-L6-v2"  # Cambiar aquí
```

---

## 👨‍💻 Desarrollo y Contribución

### Configurar Entorno de Desarrollo

```bash
# Clonar repositorio
git clone <repo-url>
cd ELECTRICA

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe

# Configurar pre-commit hooks
pre-commit install
```

### Estructura de Código

```
backend/
├── agents/          # Agentes de IA
├── api/             # Clientes de API externa
├── knowledge/       # Base de conocimiento
├── rag/             # Sistema RAG
├── utils/           # Utilidades
└── vision/          # Procesamiento de visión

frontend/
├── css/             # Estilos
├── js/              # JavaScript
└── index.html       # Página principal

data/
├── noms/            # PDFs de normas
├── generated/       # Archivos generados
└── chroma_db/       # Base vectorial

docs/
├── INSTALLATION.md
├── USER_MANUAL.md
└── TECHNICAL_DOCS.md
```

### Agregar Nuevo Agente

1. Crear archivo en `backend/agents/new_agent.py`
2. Implementar clase con métodos necesarios
3. Registrar en `backend/agents/__init__.py`
4. Integrar en `IntegratorAgent`

### Agregar Nuevo Endpoint

1. Editar `run_server.py`
2. Agregar ruta con decorador `@app.route()`
3. Implementar lógica
4. Documentar en este archivo

### Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=backend tests/

# Test específico
pytest tests/test_vision_agent.py
```

### Estilo de Código

- **Python:** PEP 8
- **JavaScript:** ES6+
- **Docstrings:** Google Style

```python
def function_name(param1: str, param2: int) -> Dict:
    """
    Brief description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

---

## 📊 Métricas y Monitoreo

### Logs

Los logs se imprimen en la terminal:

```
✓ Configuration validated
✓ Initializing system...
🧹 Cleaning up files older than 120 days...
✓ Server starting on http://localhost:8080
```

### Métricas Disponibles

- Tiempo de análisis por imagen
- Número de NCs detectadas
- Artículos más referenciados
- Tipos de instalación analizados

---

## 🔒 Seguridad

### API Keys

- Nunca commitear `.env` al repositorio
- Usar `.env.example` como plantilla
- Rotar keys periódicamente

### Validación de Entrada

- Validar tipo de archivo (solo imágenes)
- Limitar tamaño de archivo (< 10MB)
- Sanitizar nombres de archivo

### CORS

Configurado en `run_server.py`:

```python
CORS(app)  # Permitir todos los orígenes en desarrollo
```

Para producción, restringir orígenes:

```python
CORS(app, origins=["https://tu-dominio.com"])
```

---

## 📝 Notas de Versión

### v1.0.0 (Actual)
- ✅ Análisis automatizado con Gemini Vision
- ✅ Sistema RAG con NOM-001-SEDE-2012
- ✅ Generación de PDF y Word
- ✅ Interfaz web responsive
- ✅ Limpieza automática de archivos

### Roadmap

**v1.1.0 (Planeado)**
- Análisis de múltiples imágenes
- Exportar a Excel
- Historial de análisis

**v2.0.0 (Futuro)**
- Aplicación móvil
- Integración con otras normas
- Dashboard de métricas

---

**Última actualización:** Enero 2026

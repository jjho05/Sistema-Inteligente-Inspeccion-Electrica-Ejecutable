# Documentación Técnica: Sistema de Inspección Eléctrica MAS-RAG

Este documento proporciona una visión técnica detallada de los componentes principales del sistema, incluyendo la lógica de orquestación, los prompts de los agentes, el esquema de la base de datos vectorial y una muestra representativa de los datos.

---

## 1. Esquema de la Base de Datos Vectorial (RAG)

El sistema utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** para consultar la normativa **NOM-001-SEDE-2012**. La base de datos vectorial almacena fragmentos de la norma convertidos en vectores matemáticos (embeddings).

### Arquitectura del Vector Store
- **Tipo de Almacenamiento:** Vector Store local persistente.
- **Modelo de Embeddings:** `text-embedding-004` (Google Gemini).
- **Proceso de Indexación:**
  1. Los archivos PDF de la norma se procesan y limpian.
  2. Se dividen en fragmentos (chunks) de ~1000 caracteres con un traslape de 200 para mantener el contexto.
  3. Cada fragmento se convierte en un vector de alta dimensionalidad.
- **Métrica de Búsqueda:** Similitud de Coseno (Cosine Similarity).

### Estructura de Metadatos (Schema)
Cada entrada en la base de datos contiene:
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | String | Identificador único del fragmento (ej: `NOM-001_chunk_42`) |
| `content` | String | Texto crudo del fragmento de la norma |
| `norm_id` | String | Identificador del documento original (NOM-001-SEDE-2012) |
| `filename` | String | Nombre del archivo fuente |
| `chunk_index`| Integer| Posición secuencial del fragmento |

---

## 2. Muestra Representativa de la Base de Datos (Anónima)

A continuación, se presentan tres fragmentos típicos almacenados en la base de datos vectorial:

| ID | Contenido (Fragmento de Norma) | Referencia |
| :--- | :--- | :--- |
| `NC_408_01` | "Los tableros de distribución deben tener un espacio de trabajo frontal mínimo de 1 metro. No se deben almacenar materiales combustibles sobre el tablero." | Art. 408.1 |
| `NC_110_14` | "Conexiones eléctricas: Los terminales deben estar identificados y las conexiones deben ser firmes para evitar el sobrecalentamiento por resistencia." | Art. 110.14 |
| `NC_250_06` | "Identificación de conductores: El conductor puesto a tierra (neutro) debe identificarse mediante un acabado exterior blanco o gris." | Art. 200.6 |

---

## 3. Lógica Central de Orquestación (MAS-RAG)

La orquestación del sistema sigue un patrón de **Multi-Agent System (MAS)** coordinado por un **Integrator Agent**.

### Ciclo de Vida del Análisis:
1. **Ingesta:** El usuario carga una imagen y selecciona el tipo de instalación.
2. **Visión (Vision Agent):** Procesa la imagen usando Gemini Vision Pro. Genera una lista preliminar de elementos, conformidades y no conformidades.
3. **Validación Normativa (RAG Agent):** Toma las no conformidades detectadas por visión y busca en la base de datos vectorial los artículos específicos que sustentan la falla.
4. **Integración:** El `Integrator Agent` unifica los resultados, asigna niveles de severidad y genera el dictamen final.

### Fragmento del Código de Orquestación:
```python
def generate_complete_analysis(self, image_paths, installation_type, language='es'):
    # Paso 1: Análisis Visual (IA Generativa con Visión)
    vision_results = self.vision_agent.analyze_image(image_paths, installation_type)
    
    # Paso 2: Verificación Normativa (RAG)
    # El sistema busca en la DB vectorial los artículos que validan las fallas
    non_conformities = vision_results.get('non_conformities', [])
    
    # Paso 3: Clasificación y Dictamen
    classification = self._classify_installation(non_conformities)
    
    return {
        'classification': classification,
        'vision_analysis': vision_results,
        'normative_support': self.normative_agent.get_support(non_conformities)
    }
```

---

## 4. Prompts de los Agentes (Instrucciones de Especialidad)

Los agentes operan bajo "System Prompts" diseñados para maximizar la precisión técnica.

### Ejemplo: Prompt del Inspector de Tableros
> "Eres un inspector eléctrico experto certificado. Analiza esta imagen de un tablero de distribución con MÁXIMA RIGUROSIDAD.
> 
> **ELEMENTOS A VERIFICAR:**
> 1. Identificación clara de circuitos.
> 2. Espacio de trabajo frontal (mínimo 1 metro).
> 3. Conexión a tierra visible.
> 4. Ausencia de conductores expuestos.
> 
> **INSTRUCCIONES:**
> - Describe detalladamente lo que observas.
> - Si detectas una falla, cita el artículo específico de la NOM-001-SEDE-2012.
> - PRIORIZA LA SEGURIDAD sobre cualquier otro criterio."

### Ejemplo: Directiva de Bilingüismo
> "IMPORTANT: You MUST write your ENTIRE response in ENGLISH if the user selects it. Replace CONFORME with COMPLIANT and NO CONFORME with NON-COMPLIANT."

---

## 5. Esquema de Clasificación de Severidad

| Nivel | Condición | Acción Requerida |
| :--- | :--- | :--- |
| **ALTO** | Riesgo inminente de incendio o electrocución. | Corrección inmediata y paro de equipo. |
| **MEDIO** | Desviación de la norma que afecta la eficiencia o seguridad a largo plazo. | Corrección programada. |
| **BAJO** | Falta de etiquetas o limpieza sin riesgo eléctrico directo. | Mantenimiento preventivo. |

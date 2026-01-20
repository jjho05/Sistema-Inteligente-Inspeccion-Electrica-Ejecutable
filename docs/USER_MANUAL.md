# Manual de Usuario

Guía completa para usar el Sistema de Inspección Eléctrica.

## 📖 Índice

1. [Introducción](#introducción)
2. [Inicio del Sistema](#inicio-del-sistema)
3. [Realizar un Análisis](#realizar-un-análisis)
4. [Interpretar Resultados](#interpretar-resultados)
5. [Descargar Dictámenes](#descargar-dictámenes)
6. [Mejores Prácticas](#mejores-prácticas)
7. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 Introducción

El Sistema de Inspección Eléctrica es una herramienta automatizada que analiza imágenes de instalaciones eléctricas y genera dictámenes técnicos conforme a la NOM-001-SEDE-2012.

### ¿Qué hace el sistema?

- ✅ Analiza imágenes de instalaciones eléctricas
- ✅ Detecta no conformidades
- ✅ Clasifica riesgos (Crítico, Medio, Bajo)
- ✅ Genera dictámenes profesionales en PDF y Word
- ✅ Proporciona referencias normativas específicas

### ¿Qué NO hace el sistema?

- ❌ No reemplaza la inspección física
- ❌ No valida cálculos eléctricos
- ❌ No certifica instalaciones oficialmente
- ❌ No sustituye el juicio profesional

---

## 🚀 Inicio del Sistema

### Iniciar el Servidor

**Windows:**
```bash
iniciar.bat
```

**Mac/Linux:**
```bash
./iniciar.sh
```

### Verificar que Inició Correctamente

Deberías ver en la terminal:

```
============================================================
Sistema de Inspección Eléctrica
============================================================
✓ Configuration validated
✓ Initializing system...
✓ Server starting on http://localhost:8080
```

El navegador se abrirá automáticamente en `http://localhost:8080`

### Detener el Sistema

Presionar `Ctrl+C` en la terminal donde está corriendo el servidor.

---

## 📸 Realizar un Análisis

### Paso 1: Seleccionar Tipo de Instalación

En la interfaz web, selecciona el tipo de instalación:

- **🏠 Residencial:** Casas, departamentos
- **🏢 Comercial:** Oficinas, locales comerciales
- **🏭 Industrial:** Fábricas, plantas industriales

**Tip:** Seleccionar el tipo correcto mejora la precisión del análisis.

### Paso 2: Ingresar Nombre del Inspector

Escribe tu nombre completo en el campo "Nombre del Inspector".

**Ejemplo:** `Ing. Juan Pérez López`

Este nombre aparecerá en el dictamen generado en la sección "Elaborado por:".

### Paso 3: Cargar Imagen

**Opción A: Arrastrar y soltar**
1. Arrastra la imagen desde tu explorador de archivos
2. Suéltala en el área de carga

**Opción B: Seleccionar archivo**
1. Haz clic en "Seleccionar Imagen"
2. Navega a la ubicación de la imagen
3. Selecciona el archivo

**Formatos soportados:**
- JPG/JPEG
- PNG
- WebP

**Tamaño recomendado:** < 5 MB

### Paso 4: Analizar

1. Verifica que la imagen se muestre correctamente
2. Haz clic en el botón **"Analizar Instalación"**
3. Espera mientras el sistema procesa (30-60 segundos)

**Durante el análisis verás:**
```
✓ Imagen recibida
⏳ Analizando con IA...
⏳ Verificando normativa...
⏳ Generando resumen...
✓ Análisis completado
```

---

## 📊 Interpretar Resultados

### Resumen en Pantalla

Una vez completado el análisis, verás:

#### 1. **Clasificación General**

```
CLASIFICACIÓN: NO CONFORME
```

- **CONFORME:** ✅ Cumple con la norma
- **NO CONFORME:** ❌ Presenta deficiencias

#### 2. **Resumen Ejecutivo**

Descripción general de los hallazgos principales.

#### 3. **No Conformidades por Severidad**

**🔴 CRÍTICAS (Riesgo Alto)**
- Requieren acción inmediata
- Peligro para personas o propiedad
- Ejemplo: Conductores sin protección en bordes metálicos

**🟡 MEDIA (Riesgo Medio)**
- Requieren atención prioritaria
- Pueden causar fallas o sobrecalentamiento
- Ejemplo: Agrupamiento excesivo de conductores

**🟢 BAJA (Riesgo Bajo)**
- Requieren corrección programada
- Afectan eficiencia a largo plazo
- Ejemplo: Organización del cableado

#### 4. **Pestañas de Información**

**Detalles:**
- Lista completa de no conformidades
- Descripción detallada de cada hallazgo
- Referencias a artículos de la NOM

**Acciones Sugeridas:**
- Recomendaciones específicas de corrección
- Pasos a seguir para subsanar deficiencias

**Observaciones Adicionales:**
- Comentarios generales
- Aspectos que requieren verificación adicional

---

## 💾 Descargar Dictámenes

### Generar Dictamen

Después del análisis, verás dos botones:

1. **📄 Descargar Dictamen (PDF)**
2. **📝 Descargar Dictamen (Word)**

### Dictamen PDF

**Características:**
- Formato profesional e inmutable
- Ideal para compartir y archivar
- No editable

**Cuándo usar:**
- Enviar por correo electrónico
- Imprimir para archivo físico
- Presentaciones oficiales
- Cuando no se requieren modificaciones

**Cómo descargar:**
1. Clic en "📄 Descargar Dictamen (PDF)"
2. El archivo se descargará automáticamente
3. Ubicación: Carpeta de Descargas

### Dictamen Word

**Características:**
- Completamente editable
- Permite copiar/pegar con formato
- Modificable según necesidades

**Cuándo usar:**
- Necesitas editar el contenido
- Copiar secciones a otros documentos
- Personalizar formato o agregar información
- Crear versiones adaptadas

**Cómo descargar:**
1. Clic en "📝 Descargar Dictamen (Word)"
2. El archivo se descargará automáticamente
3. Ubicación: Carpeta de Descargas

### Estructura del Dictamen

Ambos formatos contienen:

1. **Encabezado**
   - Título del dictamen
   - Fecha
   - Referencia
   - Normativa aplicable

2. **1. Introducción**
   - Objetivo del análisis
   - Alcance
   - Metodología

3. **2. Análisis Detallado**
   - 2.1. Aspectos que cumplen (✓)
   - 2.2. Aspectos que NO cumplen (✗)
     - Observación
     - Riesgo
     - Normativa Aplicable

4. **3. Recomendaciones**
   - Acciones correctivas específicas
   - Prioridades

5. **4. Conclusión**
   - Resumen ejecutivo
   - Estado general

6. **Pie de Documento**
   - Elaborado por: [Tu nombre]
   - Referencias de NOMs

### Nomenclatura de Archivos

```
Dictamen_AUTO-1737329400000_20260119_184320.pdf
```

- `AUTO`: Generado automáticamente
- `1737329400000`: Timestamp único
- `20260119_184320`: Fecha y hora (YYYYMMDD_HHMMSS)

---

## ✨ Mejores Prácticas

### Calidad de Imágenes

**✅ Buenas prácticas:**
- Imagen clara y enfocada
- Buena iluminación
- Vista completa del elemento a analizar
- Resolución mínima: 800x600 px
- Tamaño: 1-5 MB

**❌ Evitar:**
- Imágenes borrosas o desenfocadas
- Iluminación insuficiente o excesiva
- Elementos parcialmente visibles
- Imágenes muy pesadas (>10 MB)
- Capturas de pantalla de baja calidad

### Tipos de Instalaciones

**Qué fotografiar:**
- Tableros eléctricos (interior)
- Centros de carga
- Distribución de conductores
- Conexiones y empalmes
- Protecciones y dispositivos
- Puestas a tierra

**Qué NO fotografiar:**
- Planos o diagramas
- Documentación
- Equipos sin contexto
- Vistas muy alejadas

### Validación de Resultados

**Siempre:**
1. ✅ Revisar el dictamen generado
2. ✅ Verificar que las no conformidades sean correctas
3. ✅ Validar referencias normativas
4. ✅ Confirmar clasificación de riesgos
5. ✅ Agregar observaciones adicionales si es necesario

**Recuerda:**
- El sistema es una herramienta de apoyo
- La validación final debe ser realizada por personal calificado
- Los dictámenes deben ser revisados antes de uso oficial

---

## ❓ Preguntas Frecuentes

### General

**P: ¿Puedo analizar múltiples imágenes a la vez?**  
R: Actualmente el sistema analiza una imagen por vez. Para múltiples imágenes, realiza análisis separados.

**P: ¿Cuánto tiempo tarda un análisis?**  
R: Entre 30-60 segundos, dependiendo de la conexión a Internet y complejidad de la imagen.

**P: ¿Los dictámenes tienen validez oficial?**  
R: Los dictámenes son documentos de apoyo. Deben ser revisados y validados por personal calificado para uso oficial.

### Técnicas

**P: ¿Qué hago si el análisis falla?**  
R: 
1. Verifica tu conexión a Internet
2. Intenta con una imagen más pequeña
3. Reinicia el servidor
4. Revisa los logs en la terminal

**P: ¿Puedo editar el dictamen después de generarlo?**  
R: Sí, descarga el formato Word (.docx) que es completamente editable.

**P: ¿Dónde se guardan los archivos generados?**  
R: En tu carpeta de Descargas. En el servidor se guardan temporalmente en `data/generated/` por 120 días.

**P: ¿Puedo cambiar el nombre del inspector después?**  
R: Sí, si descargas el Word puedes editar el campo "Elaborado por:".

### Resultados

**P: ¿Por qué no detectó todas las no conformidades?**  
R: El sistema analiza elementos visibles en la imagen. Aspectos no visibles o que requieren mediciones no pueden ser detectados.

**P: ¿Puedo confiar 100% en los resultados?**  
R: Los resultados son una guía automatizada. Siempre deben ser validados por un inspector calificado.

**P: ¿Qué significa "Sin referencia" en los artículos?**  
R: El sistema no pudo identificar un artículo específico de la NOM para esa no conformidad. Requiere revisión manual.

---

## 🔄 Nuevo Análisis

Para realizar un nuevo análisis:

1. Haz clic en el botón **"🔄 Nuevo Análisis"**
2. La página se reiniciará
3. Repite el proceso desde el Paso 1

---

## 📞 Soporte

Si necesitas ayuda:

1. Consulta la sección de [Solución de Problemas](INSTALLATION.md#solución-de-problemas)
2. Revisa los logs en la terminal
3. Reporta el problema con detalles específicos

---

**Nota:** Este manual asume que el sistema ya está instalado y configurado correctamente. Si no es así, consulta el [Manual de Instalación](INSTALLATION.md).

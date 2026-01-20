# Guía de Despliegue en Render

## Paso 1: Preparar el Proyecto ✅

Ya hemos preparado el proyecto con:
- ✅ `render.yaml` - Configuración de Render
- ✅ `run_server.py` modificado para puerto dinámico
- ✅ Código listo para la nube

## Paso 2: Subir Cambios a GitHub

```bash
cd "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Inteligente-Inspeccion-Electrica-Ejecutable"

git add .
git commit -m "Preparar para despliegue en Render"
git push
```

## Paso 3: Crear Cuenta en Render

1. Ir a https://render.com
2. Clic en "Get Started for Free"
3. Registrarse con GitHub (recomendado)
4. Autorizar Render a acceder a tus repositorios

## Paso 4: Crear Nuevo Web Service

1. En el dashboard de Render, clic en "New +"
2. Seleccionar "Web Service"
3. Conectar tu repositorio:
   - Buscar: `Sistema-Inteligente-Inspeccion-Electrica-Ejecutable`
   - Clic en "Connect"

## Paso 5: Configurar el Servicio

Render detectará automáticamente la configuración de `render.yaml`, pero verifica:

**Name:** `inspeccion-electrica` (o el que prefieras)

**Environment:** Python 3

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python run_server.py --no-browser
```

**Plan:** Free

## Paso 6: Configurar Variables de Entorno

⚠️ **MUY IMPORTANTE**

1. En la configuración del servicio, ir a "Environment"
2. Agregar variable:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Tu API Key de Gemini
   - Clic en "Add"

3. (Opcional) Agregar:
   - **Key:** `DEBUG`
   - **Value:** `False`

## Paso 7: Desplegar

1. Clic en "Create Web Service"
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias (~5-10 min)
   - Iniciar el servidor

3. Verás logs en tiempo real

## Paso 8: Obtener URL

Una vez desplegado:
- Tu URL será: `https://inspeccion-electrica.onrender.com`
- O similar, según el nombre que elegiste

## Paso 9: Probar

1. Abrir la URL en tu navegador
2. Debería aparecer la interfaz del sistema
3. Probar un análisis

## ⚠️ Consideraciones Importantes

### Plan Gratuito de Render

**Limitaciones:**
- Se "duerme" después de 15 minutos sin uso
- Primera petición después de dormir tarda ~30 segundos
- 750 horas/mes gratis

**Para evitar que se duerma:**
- Upgrade a plan pagado ($7/mes)
- O usar servicio como UptimeRobot para hacer ping cada 10 min

### API Key

**Problema:** Todos los usuarios usarán TU API Key

**Soluciones:**

1. **Límites de uso** (implementar después)
2. **Autenticación** (implementar después)
3. **Cada usuario ingresa su key** (implementar después)

Por ahora, está bien para pruebas.

### Archivos Generados

Los dictámenes se guardan en el servidor temporalmente.
- Se eliminan después de 120 días
- En plan gratuito, se pierden al reiniciar

## Troubleshooting

### Error: "Build failed"
- Revisar logs de build
- Verificar que `requirements.txt` esté completo
- Verificar versión de Python

### Error: "Application failed to respond"
- Verificar que el puerto sea dinámico (ya lo arreglamos ✅)
- Revisar logs de runtime

### Error: "GEMINI_API_KEY not found"
- Verificar que agregaste la variable de entorno
- Verificar que no tenga espacios extra

## Actualizar el Sitio

Para actualizar después de cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

Render detectará el push y redesplegará automáticamente.

## Costos Estimados

**Plan Gratuito:**
- Hosting: $0/mes
- API Gemini: ~$0.001 por análisis

**Plan Starter ($7/mes):**
- Sin dormirse
- Respuesta instantánea
- API Gemini: mismo costo

## Próximos Pasos (Opcional)

1. **Dominio personalizado:** Conectar tu propio dominio
2. **Autenticación:** Agregar sistema de login
3. **Límites:** Implementar límites de uso
4. **Monitoreo:** Configurar alertas

---

¿Listo para desplegar? Sigue los pasos arriba! 🚀

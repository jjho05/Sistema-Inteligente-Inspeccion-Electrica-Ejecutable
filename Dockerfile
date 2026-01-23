# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Evitar que Python genere archivos .pyc y use buffer para logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para OpenCV y otras librerías
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/vector_db data/generated data/normas data/templates

# Exponer el puerto que usará Flask (Hugging Face usa el 7860 por defecto)
ENV PORT=7860
EXPOSE 7860

# Comando para ejecutar la aplicación
# Hugging Face Spaces requiere escuchar en 0.0.0.0
CMD ["python", "run_server.py", "--host", "0.0.0.0", "--port", "7860", "--no-browser"]

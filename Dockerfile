# ==============================================
# Resume Videos - Dockerfile
# ==============================================

# Stage 1: Base con dependencias del sistema
FROM python:3.10-slim as base

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Instalación de dependencias Python
FROM base as dependencies

WORKDIR /app

# Copiar solo requirements para aprovechar cache de Docker
COPY config/requirements.txt /app/config/requirements.txt

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r config/requirements.txt

# Stage 3: Aplicación final
FROM dependencies as app

WORKDIR /app

# Copiar código de la aplicación
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# Crear directorios necesarios
RUN mkdir -p /app/outputs /app/videos /app/database /app/logs

# Exponer puertos
# 5000: API REST (Flask)
# 7860: Web UI (Gradio)
EXPOSE 5000 7860

# Healthcheck para API
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Comando por defecto (se puede sobrescribir en docker-compose)
CMD ["python", "scripts/main.py", "api"]

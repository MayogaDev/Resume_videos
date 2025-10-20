# Resume Videos - Guía Docker

Guía completa para ejecutar Resume Videos usando Docker y Docker Compose.

## Prerequisitos

- Docker >= 20.10
- Docker Compose >= 2.0
- 8GB RAM mínimo (16GB recomendado)
- 10GB espacio en disco (para modelos y cache)

## Estructura de Servicios

El proyecto incluye dos servicios:

1. **API REST** (Flask) - Puerto 5000
   - Endpoints para procesamiento de videos
   - Health check en `/api/health`

2. **Web UI** (Gradio) - Puerto 7860
   - Interfaz web para procesar videos
   - Visualización de resultados

## Configuración Inicial

### 1. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar según tus necesidades
# Por defecto usa google/mt5-small y whisper tiny
```

### 2. Crear directorios locales

```bash
mkdir -p database outputs videos logs
```

## Ejecución

### Opción 1: Modo Producción

```bash
# Construir imágenes y levantar servicios
docker-compose up --build

# En segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api
docker-compose logs -f web
```

### Opción 2: Modo Desarrollo

```bash
# Usar configuración de desarrollo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Esto monta el código fuente para hot-reload
```

## Uso de los Servicios

### API REST (Puerto 5000)

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Procesar video:**
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "/app/videos/mi_video.mp4",
    "whisper_model": "tiny",
    "max_summary_length": 150
  }'
```

**Listar videos procesados:**
```bash
curl http://localhost:5000/api/videos
```

### Web UI (Puerto 7860)

Abrir en el navegador:
```
http://localhost:7860
```

## Gestión de Contenedores

### Ver servicios activos
```bash
docker-compose ps
```

### Detener servicios
```bash
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Reiniciar un servicio
```bash
docker-compose restart api
docker-compose restart web
```

### Ejecutar comandos dentro del contenedor
```bash
# Bash interactivo
docker-compose exec api bash

# Ejecutar pytest
docker-compose exec api pytest -v

# Ver estadísticas de base de datos
docker-compose exec api python scripts/main.py stats
```

## Volúmenes y Persistencia

El proyecto usa los siguientes volúmenes:

| Volumen Local | Contenedor | Propósito |
|---------------|------------|-----------|
| `./database` | `/app/database` | Base de datos SQLite |
| `./outputs` | `/app/outputs` | Transcripciones y resúmenes |
| `./videos` | `/app/videos` | Videos de entrada |
| `./logs` | `/app/logs` | Logs de la aplicación |
| `huggingface_cache` | `/root/.cache/huggingface` | Cache de modelos |

### Gestionar el cache de modelos

```bash
# Ver tamaño del volumen
docker volume inspect resume_videos_huggingface_cache

# Limpiar cache (eliminará modelos descargados)
docker volume rm resume_videos_huggingface_cache
```

## Comandos Útiles

### Reconstruir imagen sin cache
```bash
docker-compose build --no-cache
```

### Ver uso de recursos
```bash
docker stats
```

### Limpiar recursos no usados
```bash
# Limpiar contenedores detenidos, redes no usadas, etc.
docker system prune

# Limpiar todo (incluyendo imágenes)
docker system prune -a
```

### Exportar/Importar base de datos
```bash
# Exportar
docker-compose exec api sqlite3 /app/database/resume_videos.db .dump > backup.sql

# Importar
cat backup.sql | docker-compose exec -T api sqlite3 /app/database/resume_videos.db
```

## Actualización

```bash
# Obtener cambios
git pull

# Reconstruir y reiniciar
docker-compose up --build -d

# Ver logs para verificar
docker-compose logs -f
```

## Troubleshooting

### Error: Puerto ya en uso

```bash
# Cambiar puertos en .env
API_PORT=5001
WEB_PORT=7861

# O detener el proceso que usa el puerto
# Windows:
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux/Mac:
lsof -i :5000
kill -9 <pid>
```

### Error: Falta memoria

```bash
# Aumentar memoria de Docker
# Docker Desktop -> Settings -> Resources -> Memory

# O usar modelo más pequeño
MODEL_PATH=google/mt5-small
WHISPER_MODEL=tiny
```

### Error: Modelos no se descargan

```bash
# Verificar conectividad
docker-compose exec api ping -c 3 huggingface.co

# Ver logs detallados
docker-compose logs -f api

# Descargar manualmente
docker-compose exec api python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('google/mt5-small')"
```

### Error: No se encuentra FFmpeg

```bash
# Verificar instalación en contenedor
docker-compose exec api ffmpeg -version

# Reconstruir imagen
docker-compose build --no-cache api
```

### Ver logs de errores

```bash
# Logs completos
docker-compose logs

# Solo errores
docker-compose logs | grep -i error

# Logs del contenedor
docker-compose exec api cat /app/logs/app.log
```

## Producción

Para despliegue en producción:

1. Usar `docker-compose.prod.yml` (crear según necesidades)
2. Configurar reverse proxy (nginx)
3. Usar variables de entorno seguras
4. Configurar backups automáticos de la base de datos
5. Monitorear recursos con herramientas como Prometheus

```bash
# Ejemplo con nginx
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Seguridad

- No exponer puertos directamente en producción (usar reverse proxy)
- Cambiar credenciales por defecto si aplica
- Mantener Docker y las imágenes actualizadas
- Limitar recursos de contenedores si es necesario

```yaml
# Limitar recursos en docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

## Soporte

Para problemas o preguntas:
- Revisar logs: `docker-compose logs -f`
- Verificar health checks: `docker-compose ps`
- Consultar documentación del proyecto

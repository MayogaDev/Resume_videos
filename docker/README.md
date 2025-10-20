# Scripts de Docker - Resume Videos

Scripts de utilidad para gestionar los servicios Docker del proyecto.

## Scripts Disponibles

### 1. start.sh - Iniciar Servicios

Inicia los servicios Docker de Resume Videos.

**Uso:**
```bash
# Modo producción (foreground)
./docker/start.sh

# Modo producción (background)
./docker/start.sh daemon
./docker/start.sh d

# Modo desarrollo (con hot-reload)
./docker/start.sh dev

# Solo construir imágenes
./docker/start.sh build
```

**Modos:**
- `prod` (default): Modo producción en foreground
- `daemon` / `d`: Modo producción en background
- `dev`: Modo desarrollo con hot-reload
- `build`: Solo construir imágenes sin iniciar

### 2. stop.sh - Detener Servicios

Detiene los servicios Docker.

**Uso:**
```bash
# Detener servicios (mantiene volúmenes)
./docker/stop.sh

# Detener y eliminar volúmenes
./docker/stop.sh clean

# Detener y limpiar sistema
./docker/stop.sh prune
```

**Modos:**
- `normal` (default): Solo detiene los contenedores
- `clean`: Detiene y elimina volúmenes (perderás modelos descargados)
- `prune`: Detiene y limpia recursos no usados

### 3. logs.sh - Ver Logs

Muestra logs de los servicios.

**Uso:**
```bash
# Logs de todos los servicios
./docker/logs.sh

# Logs solo de API
./docker/logs.sh api

# Logs solo de Web
./docker/logs.sh web

# Logs de todos (explícito)
./docker/logs.sh all
```

### 4. test.sh - Ejecutar Tests

Ejecuta los tests dentro del contenedor Docker.

**Uso:**
```bash
# Ejecutar todos los tests
./docker/test.sh

# Solo tests unitarios
./docker/test.sh unit

# Solo tests de integración
./docker/test.sh integration

# Tests con cobertura
./docker/test.sh all --coverage
./docker/test.sh unit -c
```

**Tipos de tests:**
- `all`: Todos los tests
- `unit`: Tests unitarios
- `integration`: Tests de integración
- `api`: Tests de API
- `database`: Tests de base de datos

### 5. clean.sh - Limpiar Recursos

Limpia recursos de Docker (imágenes, contenedores, volúmenes).

**Uso:**
```bash
# Limpieza básica (contenedores detenidos, redes)
./docker/clean.sh

# Limpieza completa (imágenes, cache)
./docker/clean.sh full

# Eliminar volúmenes (modelos descargados)
./docker/clean.sh volumes

# Limpieza total (TODO)
./docker/clean.sh all
```

**Niveles:**
- `basic` (default): Contenedores detenidos, redes
- `full`: + Imágenes sin usar, cache de build
- `volumes`: + Volúmenes (perderás modelos)
- `all`: TODO (requiere confirmación)

## Flujo de Trabajo Típico

### Primera vez (Setup inicial)

```bash
# 1. Copiar configuración
cp .env.example .env

# 2. Construir e iniciar
./docker/start.sh daemon

# 3. Verificar logs
./docker/logs.sh

# 4. Acceder a los servicios
# API:    http://localhost:5000/api/health
# Web UI: http://localhost:7860
```

### Desarrollo diario

```bash
# Iniciar en modo desarrollo
./docker/start.sh dev

# Ver logs en tiempo real
./docker/logs.sh

# Ejecutar tests
./docker/test.sh unit

# Detener cuando termines
./docker/stop.sh
```

### Troubleshooting

```bash
# Ver logs de errores
./docker/logs.sh api

# Reiniciar servicios
./docker/stop.sh
./docker/start.sh

# Limpiar y reconstruir
./docker/clean.sh full
./docker/start.sh build
```

### Antes de commit

```bash
# Ejecutar todos los tests
./docker/test.sh all --coverage

# Verificar que todo funciona
curl http://localhost:5000/api/health
```

### Mantenimiento

```bash
# Limpiar recursos no usados (semanal)
./docker/clean.sh basic

# Limpieza profunda (mensual)
./docker/clean.sh full
```

## Variables de Entorno

Edita `.env` para configurar:

```env
# Puertos
API_PORT=5000
WEB_PORT=7860

# Modelos
MODEL_PATH=google/mt5-small
WHISPER_MODEL=tiny

# Flask
FLASK_ENV=production
FLASK_DEBUG=0
```

## Comandos Docker Directos

Si prefieres usar Docker directamente:

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down

# Exec
docker-compose exec api bash
```

## Permisos (Linux/Mac)

Si tienes problemas de permisos:

```bash
# Dar permisos de ejecución
chmod +x docker/*.sh

# O ejecutar con bash
bash docker/start.sh
```

## Notas

- Los scripts están optimizados para Linux/Mac/Git Bash (Windows)
- En Windows (sin Git Bash), usa `docker-compose` directamente
- Los volúmenes persisten entre reinicios
- Cache de modelos se comparte entre contenedores
- Logs se guardan en `./logs/`

## Soporte

Si encuentras problemas:

1. Verifica que Docker esté corriendo: `docker info`
2. Revisa los logs: `./docker/logs.sh`
3. Prueba limpiar y reconstruir: `./docker/clean.sh && ./docker/start.sh build`
4. Verifica las variables en `.env`

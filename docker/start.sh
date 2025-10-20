#!/bin/bash

# ==============================================
# Resume Videos - Start Docker Services
# ==============================================

set -e

echo "=========================================="
echo "  Resume Videos - Starting Services"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker no está corriendo"
    exit 1
fi

# Verificar si existe .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}Advertencia: No existe .env${NC}"
    echo "Copiando .env.example -> .env"
    cp .env.example .env
fi

# Crear directorios necesarios
mkdir -p database outputs videos logs

# Modo de ejecución
MODE=${1:-prod}

if [ "$MODE" = "dev" ]; then
    echo -e "${YELLOW}Modo: DESARROLLO${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
elif [ "$MODE" = "build" ]; then
    echo -e "${YELLOW}Construyendo imágenes...${NC}"
    docker-compose build --no-cache
elif [ "$MODE" = "daemon" ] || [ "$MODE" = "d" ]; then
    echo -e "${YELLOW}Modo: PRODUCCIÓN (Background)${NC}"
    docker-compose up -d --build
else
    echo -e "${YELLOW}Modo: PRODUCCIÓN${NC}"
    docker-compose up --build
fi

# Si se ejecutó en background, mostrar estado
if [ "$MODE" = "daemon" ] || [ "$MODE" = "d" ]; then
    echo ""
    echo -e "${GREEN}Servicios iniciados:${NC}"
    docker-compose ps
    echo ""
    echo "Accede a:"
    echo "  - API:    http://localhost:5000/api/health"
    echo "  - Web UI: http://localhost:7860"
    echo ""
    echo "Ver logs: docker-compose logs -f"
    echo "Detener:  docker-compose down"
fi

#!/bin/bash

# ==============================================
# Resume Videos - Stop Docker Services
# ==============================================

set -e

echo "=========================================="
echo "  Resume Videos - Stopping Services"
echo "=========================================="

# Colores
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Modo de detención
MODE=${1:-normal}

if [ "$MODE" = "clean" ]; then
    echo -e "${RED}Deteniendo servicios y eliminando volúmenes...${NC}"
    docker-compose down -v
    echo -e "${YELLOW}Advertencia: Cache de modelos eliminada${NC}"
elif [ "$MODE" = "prune" ]; then
    echo -e "${RED}Deteniendo servicios y limpiando sistema...${NC}"
    docker-compose down
    docker system prune -f
else
    echo -e "${YELLOW}Deteniendo servicios...${NC}"
    docker-compose down
fi

echo ""
echo "Servicios detenidos"

# Mostrar estado
docker-compose ps

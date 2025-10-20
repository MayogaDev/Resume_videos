#!/bin/bash

# ==============================================
# Resume Videos - Clean Docker Resources
# ==============================================

set -e

echo "=========================================="
echo "  Resume Videos - Clean Resources"
echo "=========================================="

# Colores
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Nivel de limpieza
LEVEL=${1:-basic}

echo -e "${YELLOW}Nivel de limpieza: $LEVEL${NC}"
echo ""

if [ "$LEVEL" = "basic" ]; then
    echo "Limpieza básica:"
    echo "  - Contenedores detenidos"
    echo "  - Redes no usadas"
    echo "  - Imágenes dangling"
    echo ""
    docker-compose down
    docker system prune -f
    echo -e "${GREEN}Limpieza básica completada${NC}"

elif [ "$LEVEL" = "full" ]; then
    echo -e "${RED}Limpieza completa:${NC}"
    echo "  - Contenedores detenidos"
    echo "  - Redes no usadas"
    echo "  - Todas las imágenes sin usar"
    echo "  - Cache de build"
    echo ""
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down
        docker system prune -a -f
        echo -e "${GREEN}Limpieza completa completada${NC}"
    else
        echo "Cancelado"
        exit 0
    fi

elif [ "$LEVEL" = "volumes" ]; then
    echo -e "${RED}Limpieza de volúmenes:${NC}"
    echo "  - Todos los volúmenes del proyecto"
    echo "  - Cache de modelos HuggingFace (se volverá a descargar)"
    echo ""
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        echo -e "${GREEN}Volúmenes eliminados${NC}"
    else
        echo "Cancelado"
        exit 0
    fi

elif [ "$LEVEL" = "all" ]; then
    echo -e "${RED}LIMPIEZA TOTAL:${NC}"
    echo "  - Contenedores"
    echo "  - Imágenes"
    echo "  - Volúmenes"
    echo "  - Redes"
    echo "  - Cache de build"
    echo ""
    echo -e "${YELLOW}¡ADVERTENCIA! Esto eliminará TODO${NC}"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        docker system prune -a --volumes -f
        echo -e "${GREEN}Limpieza total completada${NC}"
    else
        echo "Cancelado"
        exit 0
    fi

else
    echo "Nivel de limpieza no válido: $LEVEL"
    echo ""
    echo "Opciones:"
    echo "  basic   - Limpieza básica (por defecto)"
    echo "  full    - Limpieza completa (imágenes y cache)"
    echo "  volumes - Eliminar volúmenes (perderás modelos descargados)"
    echo "  all     - Limpieza total (TODO)"
    echo ""
    echo "Uso: ./clean.sh [basic|full|volumes|all]"
    exit 1
fi

echo ""
echo "Estado actual:"
docker system df

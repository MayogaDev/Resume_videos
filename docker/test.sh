#!/bin/bash

# ==============================================
# Resume Videos - Run Tests in Docker
# ==============================================

set -e

echo "=========================================="
echo "  Resume Videos - Running Tests"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Tipo de test
TEST_TYPE=${1:-all}
COVERAGE=${2:-}

# Verificar si los servicios están corriendo
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Los servicios no están corriendo${NC}"
    echo "Iniciando contenedor temporal para tests..."

    # Ejecutar tests en contenedor temporal
    docker-compose run --rm api pytest -v -m "$TEST_TYPE"
else
    echo -e "${GREEN}Ejecutando tests en contenedor activo...${NC}"

    # Construir comando
    CMD="pytest -v"

    if [ "$TEST_TYPE" != "all" ]; then
        CMD="$CMD -m $TEST_TYPE"
    fi

    if [ "$COVERAGE" = "--coverage" ] || [ "$COVERAGE" = "-c" ]; then
        CMD="$CMD --cov=backend --cov-report=html --cov-report=term"
        echo -e "${YELLOW}Con reporte de cobertura${NC}"
    fi

    echo "Comando: $CMD"
    echo ""

    # Ejecutar tests
    docker-compose exec api $CMD
fi

echo ""
echo -e "${GREEN}Tests completados${NC}"

# Si se generó reporte de cobertura, indicar dónde está
if [ "$COVERAGE" = "--coverage" ] || [ "$COVERAGE" = "-c" ]; then
    echo "Reporte de cobertura: htmlcov/index.html"
fi

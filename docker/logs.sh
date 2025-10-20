#!/bin/bash

# ==============================================
# Resume Videos - View Logs
# ==============================================

echo "=========================================="
echo "  Resume Videos - Logs"
echo "=========================================="

# Servicio a ver logs
SERVICE=${1:-}

if [ -z "$SERVICE" ]; then
    echo "Mostrando logs de todos los servicios..."
    echo "Uso: ./logs.sh [api|web|all]"
    echo ""
    docker-compose logs -f
elif [ "$SERVICE" = "all" ]; then
    docker-compose logs -f
elif [ "$SERVICE" = "api" ] || [ "$SERVICE" = "web" ]; then
    echo "Mostrando logs de: $SERVICE"
    docker-compose logs -f "$SERVICE"
else
    echo "Servicio no válido: $SERVICE"
    echo "Opciones: api, web, all"
    exit 1
fi

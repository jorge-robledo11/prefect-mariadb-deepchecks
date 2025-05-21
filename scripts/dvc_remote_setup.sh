#!/bin/bash
set -euo pipefail

# Cargar variables de entorno
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "Error: No se encontró el archivo .env en $(pwd)"
    exit 1
fi

: "${DVC_REMOTE_PATH:?Debe definir DVC_REMOTE_PATH en .env}"
: "${DVC_REMOTE_NAME:?Debe definir DVC_REMOTE_NAME en .env}"

if ! uv run dvc remote list | grep -q "$DVC_REMOTE_NAME"; then
    echo "No hay remoto '$DVC_REMOTE_NAME' configurado. Configurando en $DVC_REMOTE_PATH ..."
    uv run dvc remote add -d "$DVC_REMOTE_NAME" "$DVC_REMOTE_PATH"
    git add .dvc/config
    git commit -m "Configura DVC remote $DVC_REMOTE_NAME en $DVC_REMOTE_PATH" || true
else
    echo "Remoto DVC '$DVC_REMOTE_NAME' ya está configurado."
fi

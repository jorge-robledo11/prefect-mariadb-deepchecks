#!/bin/bash
set -euo pipefail

# --- Cargar variables de entorno desde .env ---
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "Error: No se encontró el archivo .env en $(pwd)"
    exit 1
fi

DVC_TRACKED_CSV_DIR="data/raw"
RAW_CSV_FILE_NAME="dataset_raw.csv"
DVC_TRACKED_CSV_FILE_PATH="$DVC_TRACKED_CSV_DIR/$RAW_CSV_FILE_NAME"
COMMIT_MESSAGE="Update raw CSV data in DVC ($(date +'%Y-%m-%d %H:%M:%S'))"

# --- Versionar el archivo CSV con DVC ---
echo "Versionando archivo de datos CSV con DVC..."
uv run dvc add "$DVC_TRACKED_CSV_FILE_PATH"

# --- Confirmar los cambios del archivo .dvc en Git ---
echo "Añadiendo y confirmando '$DVC_TRACKED_CSV_FILE_PATH.dvc' en Git..."
git add "$DVC_TRACKED_CSV_FILE_PATH.dvc"

if git diff --staged --quiet; then
    echo "No hay cambios en el archivo .dvc para confirmar en Git."
else
    echo "Confirmando cambios de archivo .dvc en Git..."
    git commit -m "$COMMIT_MESSAGE"
    echo "Cambios confirmados en Git."
fi

# --- Subir los datos al almacenamiento remoto de DVC ---
echo "Subiendo datos CSV al almacenamiento remoto de DVC..."
uv run dvc push "$DVC_TRACKED_CSV_FILE_PATH.dvc"

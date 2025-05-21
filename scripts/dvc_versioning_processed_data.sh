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

PROCESSED_DIR="data/processed"
COMMIT_MESSAGE="Update processed data in DVC ($(date +'%Y-%m-%d %H:%M:%S'))"

# --- Versionar todos los archivos Parquet en processed/ ---
for parquet_file in "$PROCESSED_DIR"/*.parquet; do
    if [ -f "$parquet_file" ]; then
        echo "Versionando $parquet_file con DVC..."
        uv run dvc add "$parquet_file"

        echo "Añadiendo y confirmando '$parquet_file.dvc' en Git..."
        git add "$parquet_file.dvc"

        if git diff --staged --quiet; then
            echo "No hay cambios en $parquet_file.dvc para confirmar en Git."
        else
            echo "Confirmando cambios de $parquet_file.dvc en Git..."
            git commit -m "$COMMIT_MESSAGE"
            echo "Cambios confirmados en Git."
        fi

        echo "Subiendo $parquet_file.dvc al remoto de DVC..."
        uv run dvc push "$parquet_file.dvc"
    else
        echo "No se encontró ningún archivo .parquet en $PROCESSED_DIR"
    fi
done

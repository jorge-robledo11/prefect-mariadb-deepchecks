#!/bin/bash
set -euo pipefail

GENERATE_DATA_SCRIPT_PATH="src/generate_data.py"
DVC_TRACKED_CSV_DIR="data/raw"
RAW_CSV_FILE_NAME="dataset_raw.csv"
DVC_TRACKED_CSV_FILE_PATH="$DVC_TRACKED_CSV_DIR/$RAW_CSV_FILE_NAME"

echo "Generando datos crudos con $GENERATE_DATA_SCRIPT_PATH"
python "$GENERATE_DATA_SCRIPT_PATH"

if [ ! -f "$DVC_TRACKED_CSV_FILE_PATH" ]; then
    echo "Error: No se generó el archivo $DVC_TRACKED_CSV_FILE_PATH"
    exit 1
fi
echo "Archivo CSV generado/actualizado en $DVC_TRACKED_CSV_FILE_PATH"

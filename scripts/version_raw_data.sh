#!/bin/bash
set -e
set -u
set -o pipefail

# --- Configuración ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT"
echo "Ejecutando en el directorio: $(pwd)"

# --- Cargar variables de entorno desde .env ---
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "Advertencia: No se encontró el archivo .env en $(pwd)"
fi

# --- Rutas y Nombres de Archivo ---
DVC_TRACKED_CSV_DIR="data/raw"
RAW_CSV_FILE_NAME="dataset_raw.csv"
DVC_TRACKED_CSV_FILE_PATH="$DVC_TRACKED_CSV_DIR/$RAW_CSV_FILE_NAME"
GENERATE_DATA_SCRIPT_PATH="src/generate_data.py"
COMMIT_MESSAGE="Update raw CSV data in DVC ($(date +'%Y-%m-%d %H:%M:%S'))"

# --- Configuración del remoto DVC ---
DVC_REMOTE_PATH="${DVC_REMOTE_PATH:-/home/lynn/Documentos/development/repositorio-dvc-remoto/}"
DVC_REMOTE_NAME="${DVC_REMOTE_NAME:-localremote}"

if ! uv run dvc remote list | grep -q "$DVC_REMOTE_NAME"; then
    echo "No hay remoto '$DVC_REMOTE_NAME' configurado. Configurando en $DVC_REMOTE_PATH ..."
    uv run dvc remote add -d "$DVC_REMOTE_NAME" "$DVC_REMOTE_PATH"
    git add .dvc/config
    git commit -m "Configura DVC remote $DVC_REMOTE_NAME en $DVC_REMOTE_PATH" || true
else
    echo "Remoto DVC '$DVC_REMOTE_NAME' ya está configurado."
fi

# --- Verificaciones Previas ---
if [ ! -f "$GENERATE_DATA_SCRIPT_PATH" ]; then
    echo "Advertencia: El script de generación de datos '$GENERATE_DATA_SCRIPT_PATH' no fue encontrado."
fi

if [ ! -d ".dvc" ]; then
    echo "Error: Este no parece ser un repositorio DVC inicializado (falta el directorio .dvc)."
    echo "Asegúrate de haber ejecutado 'dvc init'."
    exit 1
fi

# --- 1. Generar/Actualizar los Datos Crudos ---
echo "Paso 1: Asegurar que los datos crudos CSV ('$DVC_TRACKED_CSV_FILE_PATH') están actualizados."
echo "Ejecutando el script de generación de datos: python $GENERATE_DATA_SCRIPT_PATH"
python "$GENERATE_DATA_SCRIPT_PATH"

if [ ! -f "$DVC_TRACKED_CSV_FILE_PATH" ]; then
    echo "Error: El script '$GENERATE_DATA_SCRIPT_PATH' no generó el archivo CSV '$DVC_TRACKED_CSV_FILE_PATH'."
    exit 1
fi
echo "Archivo CSV '$DVC_TRACKED_CSV_FILE_PATH' generado/actualizado."

TARGET_FILE_TO_VERSION="$DVC_TRACKED_CSV_FILE_PATH"

# --- 2. Versionar el archivo CSV con DVC ---
echo "Paso 2: Versionando archivo de datos CSV ('$TARGET_FILE_TO_VERSION') con DVC..."
uv run dvc add "$TARGET_FILE_TO_VERSION"

# --- 3. Confirmar los cambios del archivo .dvc en Git ---
echo "Paso 3: Añadiendo y confirmando '$TARGET_FILE_TO_VERSION.dvc' en Git..."
git add "$TARGET_FILE_TO_VERSION.dvc"

if git diff --staged --quiet; then
    echo "No hay cambios en el archivo .dvc para confirmar en Git."
else
    echo "Confirmando cambios de archivo .dvc en Git con el mensaje: '$COMMIT_MESSAGE'..."
    git commit -m "$COMMIT_MESSAGE"
    echo "Cambios confirmados en Git."
fi

# --- 4. Subir los datos al almacenamiento remoto de DVC ---
echo "Paso 4: Subiendo datos CSV al almacenamiento remoto de DVC (dvc push)..."
uv run dvc push "$TARGET_FILE_TO_VERSION.dvc"

# --- 5. Subir los cambios de Git al repositorio remoto (Opcional) ---
echo "Paso 5: Subiendo commits de Git al repositorio remoto (git push)..."

echo "-------------------------------------------------------------"
echo "Proceso de actualización y versionado de datos crudos CSV completado."
echo "DVC ahora gestiona: '$TARGET_FILE_TO_VERSION'."
echo "Su metarchivo .dvc ('$TARGET_FILE_TO_VERSION.dvc') ha sido confirmado en Git."
echo "Terraform está configurado para usar este archivo CSV directamente desde su ubicación."
echo "Si trabajas en un nuevo entorno, ejecuta 'dvc pull $TARGET_FILE_TO_VERSION.dvc' ANTES de 'terraform apply'."
echo "Recuerda ejecutar 'git push' si no se hizo automáticamente para subir los commits de Git."
echo "-------------------------------------------------------------"

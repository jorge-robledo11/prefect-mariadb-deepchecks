#!/bin/bash

# Salir inmediatamente si un comando falla
set -e
# Tratar las referencias a variables no establecidas como un error
set -u
# El estado de salida de una tubería es el del último comando que falló, o cero si todos tuvieron éxito
set -o pipefail

# --- Configuración ---
# Obtener la ruta absoluta del directorio donde se encuentra este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Asumir que la raíz del proyecto está un nivel arriba del directorio 'scripts'
PROJECT_ROOT="$SCRIPT_DIR/.."

# Navegar a la raíz del proyecto
cd "$PROJECT_ROOT"
echo "Ejecutando en el directorio: $(pwd)"

# --- Rutas y Nombres de Archivo ---
# Ubicación canónica del archivo CSV crudo, gestionado por DVC.
# Este es el archivo que generate_data.py crea.
DVC_TRACKED_CSV_DIR="data/raw"
RAW_CSV_FILE_NAME="dataset_raw.csv"
DVC_TRACKED_CSV_FILE_PATH="$DVC_TRACKED_CSV_DIR/$RAW_CSV_FILE_NAME"

# Script que genera los datos crudos (opcional, pero bueno tenerlo como referencia)
GENERATE_DATA_SCRIPT_PATH="src/generate_data.py"

# Mensaje de commit para Git
COMMIT_MESSAGE="Update raw CSV data in DVC ($(date +'%Y-%m-%d %H:%M:%S'))"

# --- Verificaciones Previas ---
# 1. Verificar que el script de generación de datos exista (opcional)
if [ ! -f "$GENERATE_DATA_SCRIPT_PATH" ]; then
    echo "Advertencia: El script de generación de datos '$GENERATE_DATA_SCRIPT_PATH' no fue encontrado."
    # Decide si esto debe ser un error fatal o solo una advertencia
fi

# 2. Verificar que el directorio .dvc exista
if [ ! -d ".dvc" ]; then
    echo "Error: Este no parece ser un repositorio DVC inicializado (falta el directorio .dvc)."
    echo "Asegúrate de haber ejecutado 'dvc init'."
    exit 1
fi

# --- 1. Generar/Actualizar los Datos Crudos ---
echo "Paso 1: Asegurar que los datos crudos CSV ('$DVC_TRACKED_CSV_FILE_PATH') están actualizados."
echo "Ejecutando el script de generación de datos: python $GENERATE_DATA_SCRIPT_PATH"
python "$GENERATE_DATA_SCRIPT_PATH" # Esto creará/actualizará data/raw/dataset_raw.csv

# Verificar que el archivo CSV fue creado/actualizado por el script de Python
if [ ! -f "$DVC_TRACKED_CSV_FILE_PATH" ]; then
    echo "Error: El script '$GENERATE_DATA_SCRIPT_PATH' no generó el archivo CSV '$DVC_TRACKED_CSV_FILE_PATH'."
    exit 1
fi
echo "Archivo CSV '$DVC_TRACKED_CSV_FILE_PATH' generado/actualizado."

# El archivo que DVC versionará es el que está en la ubicación canónica de DVC
TARGET_FILE_TO_VERSION="$DVC_TRACKED_CSV_FILE_PATH"

# --- 2. Versionar el archivo CSV con DVC ---
# Asegúrate de que data/raw/dataset_raw.csv está en tu .gitignore
echo "Paso 2: Versionando archivo de datos CSV ('$TARGET_FILE_TO_VERSION') con DVC..."
dvc add "$TARGET_FILE_TO_VERSION"
# Esto creará/actualizará el archivo data/raw/dataset_raw.csv.dvc

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

# --- 4. Subir los datos al almacenamiento remoto de DVC (Opcional pero recomendado) ---
echo "Paso 4: Subiendo datos CSV al almacenamiento remoto de DVC (dvc push)..."
dvc push "$TARGET_FILE_TO_VERSION.dvc"

# --- 5. Subir los cambios de Git al repositorio remoto (Opcional pero recomendado) ---
echo "Paso 5: Subiendo commits de Git al repositorio remoto (git push)..."
# git push # Descomenta si quieres que este script también haga git push

echo "-------------------------------------------------------------"
echo "Proceso de actualización y versionado de datos crudos CSV completado."
echo "DVC ahora gestiona: '$TARGET_FILE_TO_VERSION'."
echo "Su metarchivo .dvc ('$TARGET_FILE_TO_VERSION.dvc') ha sido confirmado en Git."
echo "Terraform está configurado para usar este archivo CSV directamente desde su ubicación."
echo "Si trabajas en un nuevo entorno, ejecuta 'dvc pull $TARGET_FILE_TO_VERSION.dvc' ANTES de 'terraform apply'."
echo "Recuerda ejecutar 'git push' si no se hizo automáticamente para subir los commits de Git."
echo "-------------------------------------------------------------"

#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT"

# Dar permisos de ejecución a todos los .sh de la carpeta scripts
chmod +x ./scripts/*.sh

./scripts/dvc_remote_setup.sh
./scripts/data_generation.sh
./scripts/dvc_versioning_raw_data.sh
./scripts/dvc_versioning_processed_data.sh

echo "--------------------------------------------------------------------"
echo "Flujo completo de versionado y subida de datos ejecutado con éxito."
echo "--------------------------------------------------------------------"

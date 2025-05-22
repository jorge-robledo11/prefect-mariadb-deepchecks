#!/bin/bash
# Script para ejecutar los tests del proyecto usando uv y pytest
set -e

export PREFECT_LOGGING_LEVEL=CRITICAL

# Ejecutar los tests con uv y pytest
uv run pytest -W ignore tests

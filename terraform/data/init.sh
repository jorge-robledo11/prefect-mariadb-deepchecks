#!/usr/bin/env bash
set -e

# Directorio donde están dataset.csv e init.sh
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 0) Comprobar que dataset.csv existe
if [ ! -f "${BASE_DIR}/dataset.csv" ]; then
  echo "Error: no encontré ${BASE_DIR}/dataset.csv. Primero convierte tu Parquet a CSV en el host."
  exit 1
fi

# 1) Crear la base de datos y la tabla
mariadb -uroot -p"$MYSQL_ROOT_PASSWORD" -e "
CREATE DATABASE IF NOT EXISTS dataset_db;
USE dataset_db;
CREATE TABLE IF NOT EXISTS mi_tabla (
  id CHAR(12) PRIMARY KEY,
  cat1 CHAR(1),
  cat2 CHAR(1),
  cont1 DECIMAL(10,4),
  cont2 DECIMAL(10,4),
  cont3 DECIMAL(10,4),
  cont4 DECIMAL(10,4),
  disc1 TINYINT,
  disc2 TINYINT
);
"

# 2) Cargar el CSV con LOAD DATA LOCAL INFILE
mariadb -uroot -p"$MYSQL_ROOT_PASSWORD" --local-infile=1 -e "
USE dataset_db;
LOAD DATA LOCAL INFILE '${BASE_DIR}/dataset.csv'
INTO TABLE mi_tabla
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
IGNORE 1 LINES;
"

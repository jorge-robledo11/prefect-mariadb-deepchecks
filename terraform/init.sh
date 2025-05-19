#!/usr/bin/env bash
set -e

# El CSV ahora está montado en /data_source/dataset_raw.csv dentro del contenedor
DATASET_PATH="/data_source/dataset_raw.csv"

# 0) Comprobar que dataset_raw.csv existe
if [ ! -f "${DATASET_PATH}" ]; then
  echo "Error: no encontré ${DATASET_PATH}."
  echo "Asegúrate de que 'data/raw/dataset_raw.csv' exista en el host y esté correctamente montado."
  echo "Ejecuta 'dvc pull data/raw/dataset_raw.csv.dvc' si es necesario."
  exit 1
fi

# 1) Crear la base de datos y la tabla
mariadb -uroot -p"${MYSQL_ROOT_PASSWORD}" -e "
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE:-dataset_db};
USE ${MYSQL_DATABASE:-dataset_db};
CREATE TABLE IF NOT EXISTS mi_tabla (
  id CHAR(12) PRIMARY KEY,
  cat1 CHAR(1),
  cat2 CHAR(1),
  cont1 DECIMAL(10,4),
  cont2 DECIMAL(10,4),
  cont3 DECIMAL(10,4),
  cont4 DECIMAL(10,4),
  disc1 TINYINT,
  disc2 TINYINT,
  target TINYINT
);
"

# 2) Cargar el CSV
mariadb -uroot -p"${MYSQL_ROOT_PASSWORD}" --local-infile=1 -D "${MYSQL_DATABASE:-dataset_db}" -e "
LOAD DATA LOCAL INFILE '${DATASET_PATH}'
INTO TABLE mi_tabla
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
IGNORE 1 LINES;
"

echo "Base de datos inicializada y datos cargados desde ${DATASET_PATH}."

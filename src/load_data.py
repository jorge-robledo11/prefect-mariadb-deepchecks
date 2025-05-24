"""Módulo para cargar datos desde una base de datos MySQL."""

import os

import pandas as pd
from dotenv import load_dotenv
from prefect import task
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


@task(name='Cargar datos iniciales', retries=3)
def load_data() -> pd.DataFrame:
    """
    Carga datos desde una base de datos MySQL.

    Lee las credenciales de variables de entorno, establece una conexión
    y carga los datos de la tabla especificada.

    Returns
    -------
        pd.DataFrame: Datos cargados.

    Raises
    ------
        RuntimeError: Si faltan variables de entorno.
        SQLAlchemyError: Si hay errores de conexión.
    """
    # 1) Carga las vars del .env
    if not load_dotenv():
        raise RuntimeError('No se pudo cargar el archivo .env')

    # Obtener variables de entorno con validación
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    table_name = os.environ.get('TABLE_NAME')

    # Validar variables
    required_vars = {
        'DB_USER': user,
        'DB_PASSWORD': password,
        'DB_HOST': host,
        'DB_PORT': port,
        'DB_NAME': db_name,
        'TABLE_NAME': table_name,
    }
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise RuntimeError(f'Variables de entorno faltantes: {", ".join(missing)}')

    # 2) Crea la URL de conexión
    try:
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
        )

        # Construye la consulta de forma segura
        query = f'SELECT * FROM `{table_name}`'  # nosec
        return pd.read_sql(query, con=engine)

    except SQLAlchemyError as e:
        raise SQLAlchemyError(f'Error de conexión a la base de datos: {str(e)}') from e

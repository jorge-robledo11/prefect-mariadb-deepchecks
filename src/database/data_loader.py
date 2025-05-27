"""Cargador de datos desde base de datos."""

import os

from connection import DatabaseConnection
from pandas import DataFrame
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def load_table_data(
    connection: DatabaseConnection, table_name: str | None = None
) -> DataFrame:
    """
    Carga datos de una tabla específica.

    Args:
        connection: Instancia de conexión a la base de datos
        table_name: Nombre de la tabla (opcional, se obtiene de env si no se proporciona)

    Returns:
        pd.DataFrame: Datos cargados de la tabla

    Raises:
        RuntimeError: Si falta el nombre de la tabla
        SQLAlchemyError: Si hay errores de conexión o consulta
    """
    if table_name is None:
        table_name = os.environ.get('TABLE_NAME')
        if not table_name:
            raise RuntimeError(
                'TABLE_NAME no especificado ni en parámetros ni en variables de entorno'
            )

    try:
        query = text(f'SELECT * FROM `{table_name}`')

        with connection.engine.connect() as conn:
            result = conn.execute(query)
            # Usar nombre descriptivo en lugar de 'df' y return directo
            return DataFrame(result.fetchall(), columns=result.keys())

    except SQLAlchemyError as e:
        raise SQLAlchemyError(
            f'Error ejecutando consulta en tabla {table_name}: {str(e)}'
        ) from e

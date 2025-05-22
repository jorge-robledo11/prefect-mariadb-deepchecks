import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from prefect import task


@task(name='Cargar datos iniciales', retries=3)
def load_data() -> pd.DataFrame:
    """
    Esta función lee las credenciales de conexión desde un archivo .env,
    establece una conexión a la base de datos y carga los datos de la tabla
    especificada en la variable de entorno TABLE_NAME.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados desde la base de datos.

    Raises:
        ValueError: Si faltan variables de entorno requeridas.
        SQLAlchemyError: Si hay problemas de conexión con la base de datos.
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
        'TABLE_NAME': table_name
    }
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise RuntimeError(f"Variables de entorno faltantes: {', '.join(missing)}")

    # 2) Crea la URL de conexión
    try:
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
        )

        # 3) Lee la tabla especificada
        data = pd.read_sql(f'SELECT * FROM {table_name};', con=engine)
        return data
        
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f'Error de conexión a la base de datos: {str(e)}')

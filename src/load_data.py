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
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')
    table_name = os.getenv('TABLE_NAME')

    # Verificar que todas las variables necesarias estén definidas
    if not user:
        raise ValueError('Variable de entorno DB_USER no definida')
    if not password:
        raise ValueError('Variable de entorno DB_PASSWORD no definida')
    if not host:
        raise ValueError('Variable de entorno DB_HOST no definida')
    if not port:
        raise ValueError('Variable de entorno DB_PORT no definida')
    if not db:
        raise ValueError('Variable de entorno DB_NAME no definida')
    if not table_name:
        raise ValueError('Variable de entorno TABLE_NAME no definida')

    # 2) Crea la URL de conexión
    try:
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
        )

        # 3) Lee la tabla especificada
        data = pd.read_sql(f'SELECT * FROM {table_name};', con=engine)
        
        # Verificar que el DataFrame no esté vacío
        if data.empty:
            raise ValueError(f'La tabla {table_name} no contiene datos')
            
        return data
        
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f'Error de conexión a la base de datos: {str(e)}')

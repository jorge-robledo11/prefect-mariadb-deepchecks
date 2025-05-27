"""Script de diagnóstico detallado para conexión MariaDB."""

import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def main() -> None:
    """Función principal para diagnóstico de conexión a base de datos."""
    print('🔄 Diagnóstico detallado de conexión...')

    # Mostrar todas las variables
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    print(f'DB_HOST: {host}')
    print(f'DB_PORT: {port}')
    print(f'DB_USER: {user}')
    print(f'DB_NAME: {db_name}')

    # Construir connection string con timeouts
    connection_string = (
        f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
        f'?connect_timeout=30&read_timeout=30'
    )

    print(f'🔗 Connection string: mysql+pymysql://{user}:***@{host}:{port}/{db_name}')

    try:
        print('📡 Creando engine...')
        engine = create_engine(connection_string, echo=True)

        print('🔌 Intentando conectar...')
        with engine.connect() as conn:
            print('✅ Conexión establecida!')
            result = conn.execute(text('SELECT 1 as test'))
            row = result.fetchone()
            print(f'✅ Query exitosa: {row}')

    except SQLAlchemyError as e:
        print(f'❌ Error SQLAlchemy: {str(e)}')
        print(f'❌ Tipo: {type(e).__name__}')

        # Mostrar detalles específicos del error
        if hasattr(e, 'orig'):
            print(f'❌ Error original: {e.orig}')

    except Exception as e:
        print(f'❌ Error general: {str(e)}')
        print(f'❌ Tipo: {type(e).__name__}')


if __name__ == '__main__':
    main()

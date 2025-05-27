"""Módulo para gestión de conexiones a base de datos."""

import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class DatabaseConnection:
    """Gestiona conexiones a la base de datos MariaDB."""

    def __init__(self, load_env: bool = True):
        """
        Inicializa la conexión a la base de datos.

        Args:
            load_env: Si debe cargar variables del archivo .env
        """
        if load_env:
            load_dotenv()

        self._engine: Engine | None = None
        self._connection_string = self.build_connection_string()

    def build_connection_string(self) -> str:
        """Construye la cadena de conexión desde variables de entorno."""
        required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
        config = {}

        for var in required_vars:
            value = os.environ.get(var)
            if not value:
                raise RuntimeError(f'Variable de entorno faltante: {var}')
            config[var.lower()] = value

        return (
            f'mysql+pymysql://{config["db_user"]}:{config["db_password"]}'
            f'@{config["db_host"]}:{config["db_port"]}/{config["db_name"]}'
            f'?connect_timeout=30&read_timeout=30&charset=utf8mb4'
        )

    @property
    def engine(self) -> Engine:
        """Obtiene o crea el engine de SQLAlchemy."""
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self._connection_string,
                    pool_size=5,  # Reducido para contenedores
                    max_overflow=10,  # Reducido para contenedores
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    echo=False,  # Cambiar a True para debug
                )
            except SQLAlchemyError as e:
                raise SQLAlchemyError(f'Error creando engine: {str(e)}') from e

        return self._engine

    def test_connection(self) -> bool:
        """Prueba la conexión a la base de datos."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('SELECT 1'))
                # Verificar explícitamente que retorna 1
                row = result.fetchone()
                return bool(row and row[0] == 1)  # Conversión explícita a bool
        except SQLAlchemyError as e:
            print(f'Error SQLAlchemy: {str(e)}')
            return False
        except Exception as e:
            print(f'Error inesperado: {str(e)}')
            return False

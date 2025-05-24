"""Configuración de fixtures para testing con Prefect."""

import os
from collections.abc import Generator

import pytest
from prefect.settings import temporary_settings
from prefect.testing.utilities import prefect_test_harness

# Configurar variable de entorno antes de importar Prefect
os.environ['PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW'] = 'ignore'
os.environ['PREFECT_SERVER_EPHEMERAL_STARTUP_TIMEOUT_SECONDS'] = '90'


@pytest.fixture(autouse=True, scope='session')
def prefect_test_fixture() -> Generator[None, None, None]:
    """
    Configura un entorno de testing temporal para Prefect.

    Esta fixture se ejecuta automáticamente para toda la sesión de testing,
    configurando las variables de entorno necesarias y el test harness de Prefect.

    Yields
    ------
        None: Control del flujo de testing.
    """
    # Combinar múltiples context managers en una sola declaración with
    with (
        temporary_settings(
            updates={'PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW': 'ignore'}
        ),
        prefect_test_harness(),
    ):
        yield

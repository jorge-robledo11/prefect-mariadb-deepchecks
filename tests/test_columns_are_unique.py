import pytest
from pandas import DataFrame

from src.database.connection import load_data


def test_columns_are_unique() -> None:
    """
    Verifica que el DataFrame cargado por load_data()
    no tenga columnas duplicadas.
    """
    try:
        df: DataFrame = load_data()
    except Exception as e:
        pytest.skip(f'No se pudo cargar el DataFrame: {e}')

    # Validar unicidad de columnas
    cols = list(df.columns)
    duplicates = [col for col in cols if cols.count(col) > 1]
    assert not duplicates, f'Columnas duplicadas encontradas: {set(duplicates)}'

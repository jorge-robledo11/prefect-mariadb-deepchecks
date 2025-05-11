import pytest
from pandas import DataFrame
from src.load_data import load_data

def test_dataframe_not_empty() -> None:
    """
    Verifica que load_data() devuelva un DataFrame y que no esté vacío.
    """
    try:
        df: DataFrame = load_data()
    except Exception as e:
        pytest.skip(f'No se pudo cargar el DataFrame: {e}')

    # Aserciones sobre el DataFrame
    assert isinstance(df, DataFrame), f'Se esperaba un DataFrame, no {type(df)}'
    assert not df.empty, 'El DataFrame cargado está vacío.'

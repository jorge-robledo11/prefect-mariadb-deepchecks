import pytest
from pathlib import Path
from pandas import DataFrame
from sqlalchemy.exc import SQLAlchemyError
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity
from src.load_data import load_data
import warnings
warnings.filterwarnings('ignore')


def test_data_integrity_suite(target: str='target') -> None:
    """
    Ejecuta la suite de integridad de Deepchecks sobre los datos cargados
    por load_data(), genera un reporte HTML si no existe y aserta que todos
    los checks pasen.
    """

    # 1) Carga el DataFrame
    try:
        df: DataFrame = load_data()
    except (ValueError, RuntimeError, SQLAlchemyError) as e:
        pytest.skip(f'No fue posible cargar datos: {e}')

    # 2) Asegurar que las columnas categóricas son del tipo adecuado
    cat_features = ['cat1', 'cat2', 'disc1', 'disc2']
    df[cat_features] = df[cat_features].astype('category')

    # 3) Construye y ejecuta la suite de integridad
    dataset = Dataset(df, label=target, cat_features=cat_features)
    result = data_integrity().run(dataset)

    # 4) Genera directorio de reportes en la raíz del proyecto si no existe
    root_dir = Path(__file__).parent.parent
    reports_dir = root_dir / 'reports'
    if not reports_dir.exists():
        reports_dir.mkdir()

    # 5) Escribe el informe en HTML
    report_path = reports_dir / 'data_integrity_report.md'
    result.save_as_cml_markdown(file=str(report_path), attach_html_report=False)

    # 6) Aserta que todos los checks pasen
    assert result.passed(), f'Suite de integridad falló. Consulta el reporte HTML'

import pytest
from pathlib import Path
import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import train_test_validation


def test_split_validation(
    train_path: Path | str | None = None,
    test_path: Path | str | None = None,
    label: str = 'target',
    categorical_features: list[str] = ['cat1', 'cat2', 'disc1', 'disc2']
) -> None:
    """
    Ejecuta la suite de validación train-test de Deepchecks y genera un reporte HTML.
    
    Args:
        train_path: Ruta al archivo parquet de entrenamiento. Si es None, usa 'data/train.parquet'
        test_path: Ruta al archivo parquet de prueba. Si es None, usa 'data/test.parquet'
        label: Nombre de la columna objetivo
        categorical_features: Lista de nombres de columnas categóricas
    
    Raises:
        AssertionError: Si la suite de validación falla
    """
    # 1) Determinar rutas de archivos
    root_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
    data_dir = root_dir / 'data' / 'processed'
    
    if train_path is None:
        train_path = data_dir / 'train.parquet'
    elif isinstance(train_path, str):
        train_path = Path(train_path)
        
    if test_path is None:
        test_path = data_dir / 'test.parquet'
    elif isinstance(test_path, str):
        test_path = Path(test_path)
    
    # 2) Verificar que los archivos existen
    if not train_path.exists():
        pytest.skip(f'Archivo de entrenamiento no encontrado: {train_path}')
    
    if not test_path.exists():
        pytest.skip(f'Archivo de prueba no encontrado: {test_path}')
    
    # 3) Cargar los datos
    try:
        train_df = pd.read_parquet(train_path)
        test_df = pd.read_parquet(test_path)
    except Exception as e:
        pytest.fail(f'Error al cargar los archivos parquet: {str(e)}')
    
    # 4) Verificar que las columnas necesarias existen
    required_columns = [label] + categorical_features
    missing_in_train = [col for col in required_columns if col not in train_df.columns]
    missing_in_test = [col for col in required_columns if col not in test_df.columns]
    
    if missing_in_train:
        pytest.fail(f'Columnas faltantes en datos de entrenamiento: {', '.join(missing_in_train)}')
    
    if missing_in_test:
        pytest.fail(f'Columnas faltantes en datos de prueba: {', '.join(missing_in_test)}')
    
    # 5) Crear datasets de Deepchecks
    train_ds = Dataset(
        train_df, 
        label=label,
        cat_features=categorical_features
    )
    
    test_ds = Dataset(
        test_df, 
        label=label,
        cat_features=categorical_features
    )
    
    # 6) Ejecutar la suite de validación
    validation_suite = train_test_validation()
    suite_result = validation_suite.run(train_ds, test_ds)
    
    # 7) Guardar el resultado como HTML
    reports_dir = root_dir / 'reports'
    if not reports_dir.exists():
        reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 8) Guardar también como markdown para CI/CD
    reports_path = reports_dir / 'train_test_validation_report.md'
    suite_result.save_as_cml_markdown(str(reports_path), attach_html_report=False)
    
    # 9) Verificar que la suite pasó
    assert suite_result.passed(), f'La suite de validación train-test falló. Consulta el reporte HTML'

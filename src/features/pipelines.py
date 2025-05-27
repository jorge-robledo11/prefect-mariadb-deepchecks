"""
Módulo para ingeniería de características y transformación de datos.

Contiene funciones para cargar, ajustar y transformar datos usando pipelines de scikit-learn.
"""

from pathlib import Path

import joblib
from pandas import DataFrame, Series
from sklearn.pipeline import Pipeline


def feature_engineering(
    X_train: DataFrame, y_train: Series, X_test: DataFrame
) -> tuple[DataFrame, DataFrame]:
    """
    Carga un pipeline de scikit-learn pre-guardado, lo ajusta y transforma los datos.

    Args:
    ----
        X_train (DataFrame): Características del conjunto de entrenamiento.
        y_train (Series): Variable objetivo del conjunto de entrenamiento.
        X_test (DataFrame): Características del conjunto de prueba.

    Returns:
    -------
        tuple[DataFrame, DataFrame]: DataFrames de entrenamiento y prueba transformados.
            Nota: El pipeline podría devolver np.ndarray en lugar de DataFrame.
    """
    # 1) Determina el directorio raíz del proyecto y el subdirectorio de pipelines.
    root_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
    pipelines_dir = root_dir / 'pipelines'

    # 2) Crea el directorio 'pipelines/' si no existe.
    pipelines_dir.mkdir(parents=True, exist_ok=True)
    if not pipelines_dir.exists():
        print(f'📁 Directorio de pipelines creado en: {pipelines_dir}')

    # 3) Carga el pipeline serializado (asume que se llama 'best_pipeline.pkl').
    best_pipeline: Pipeline = joblib.load(pipelines_dir / 'best_pipeline.pkl')

    # 4) Ajusta el pipeline a los datos de entrenamiento y los transforma.
    X_train_transformed = best_pipeline.fit_transform(X_train, y_train)

    # 5) Transforma los datos de prueba usando el pipeline ya ajustado.
    X_test_transformed = best_pipeline.transform(X_test)

    return X_train_transformed, X_test_transformed

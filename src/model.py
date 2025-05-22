
"""
Módulo para entrenamiento, guardado y evaluación de modelos de Machine Learning.

Contiene funciones para entrenar modelos Random Forest, guardarlos en disco y evaluar su rendimiento.
"""

from pathlib import Path

import joblib
from pandas import DataFrame, Series
from prefect import task
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


@task(name='Entrenar el modelo', retries=3)
def train_model(X_train: DataFrame, y_train: Series) -> RandomForestClassifier:
    """
    Entrena un modelo Random Forest.
    
    Args:
        X_train (DataFrame): Características de entrenamiento.
        y_train (Series): Variable objetivo de entrenamiento.

    Returns:
        RandomForestClassifier: Modelo entrenado.
    """
    try:
        # Inicializar y entrenar modelo
        model = RandomForestClassifier(random_state=42, n_jobs=-1)

        model.fit(X_train, y_train)
        return model

    except Exception as e:
        print(f'Error durante el entrenamiento: {str(e)}')


@task(name='Guardar el modelo', retries=3)
def save_model(model: RandomForestClassifier) -> None:
    """
    Crea automáticamente el directorio de modelos si no existe.
    
    Guarda el modelo entrenado en formato .pkl.

    Args:
        model (RandomForestClassifier): Modelo entrenado a guardar

    Returns:
        Path: Ruta absoluta donde se guardó el modelo
    """
    try:
        root_dir = (
            Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
        )
        models_dir = root_dir / 'models'
        model_path = models_dir / f'{type(model).__name__}.pkl'

        # Si el directorio no existe, créalo
        if not models_dir.mkdir(parents=True, exist_ok=True):
            print(f'📁 Directorio de modelos creado en: {models_dir}')

        joblib.dump(model, model_path)
        print(f'Modelo guardado en: {model_path.resolve()}')

    except Exception as e:
        print(f'Error guardando modelo: {str(e)}')


task(name='Evaluar modelo (ROC-AUC)', log_prints=True)
def evaluate_model(
    model: RandomForestClassifier,
    X_train: DataFrame,
    y_train: Series,
    X_test: DataFrame,
    y_test: Series,
) -> dict:
    """
    Evalúa el modelo usando la métrica ROC-AUC en train y test.

    Args:
        model: Modelo entrenado
        X_train: Datos de entrenamiento
        y_train: Etiquetas de entrenamiento
        X_test: Datos de prueba
        y_test: Etiquetas de prueba

    Returns:
        dict: {'roc_auc_train': float, 'roc_auc_test': float}
    """
    try:
        # Verifica que el modelo tenga predict_proba
        if not hasattr(model, 'predict_proba'):
            raise ValueError(
                'El modelo no tiene método predict_proba necesario para ROC-AUC'
            )

        # Probabilidades para clase positiva
        y_train_proba = model.predict_proba(X_train)[:, 1]
        y_test_proba = model.predict_proba(X_test)[:, 1]

        # Cálculo de ROC-AUC
        roc_auc_train = roc_auc_score(y_train, y_train_proba)
        roc_auc_test = roc_auc_score(y_test, y_test_proba)

        return {'roc_auc_train': roc_auc_train, 'roc_auc_test': roc_auc_test}

    except Exception as e:
        raise RuntimeError(f'Error en evaluación ROC-AUC: {str(e)}') from e

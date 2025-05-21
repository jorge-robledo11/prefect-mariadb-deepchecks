# src/train_rf_model.py
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path


def train_model(X_train: DataFrame, y_train: Series) -> RandomForestClassifier:
    """
    Entrena un modelo Random Forest
    """
    try:
        
        # Inicializar y entrenar modelo
        model = RandomForestClassifier(
            seed=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        return model
    
    except Exception as e:
        print(f'Error durante el entrenamiento: {str(e)}')


def save_model(model: RandomForestClassifier) -> Path:
    """
    Guarda el modelo entrenado en formato .pkl.
    Crea automáticamente el directorio de modelos si no existe.
    
    Args:
        model (RandomForestClassifier): Modelo entrenado a guardar
            
    Returns:
        Path: Ruta absoluta donde se guardó el modelo
    """
    try:
        root_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
        models_dir = root_dir / 'models'
        model_path = models_dir / f'{type(model).__name__}.pkl'

        # Si el directorio no existe, créalo
        if not models_dir.mkdir(parents=True, exist_ok=True):
            print(f'📁 Directorio de modelos creado en: {models_dir}')

        joblib.dump(model, model_path)
        print(f'Modelo guardado en: {model_path.resolve()}')
        return model_path

    except Exception as e:
        print(f'Error guardando modelo: {str(e)}')

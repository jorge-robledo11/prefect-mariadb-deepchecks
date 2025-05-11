from pandas import DataFrame
from sklearn.model_selection import train_test_split
from pathlib import Path


def split_dataset(data: DataFrame, target: str, seed: int=42) -> tuple[DataFrame, DataFrame]:
    """
    Divide un dataset en conjuntos de entrenamiento y prueba, y guarda los archivos en formato Parquet.
    
    Args:
        data: DataFrame con los datos a dividir
        target: Nombre de la columna objetivo (usado para estratificación)
        seed: Semilla para reproducibilidad
        
    Returns:
        Tupla con (train_data, test_data)
    """
    
    # 1) Determina root_dir
    root_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
    data_dir = root_dir / 'data'
    
    # 2) Crea 'data/' si no existe
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f'📁 Directorio de datos creado en: {data_dir}')
    
    # 3) Dividir el conjunto original en entrenamiento y prueba
    train_data, test_data = train_test_split(
        data,
        test_size=0.3,
        random_state=seed,
        stratify=data[target]
    )
    
    # 4) Rutas de salida Parquet
    train_path = data_dir / 'train.parquet'
    test_path = data_dir / 'test.parquet'

    # 5) Guarda los archivos
    train_data.to_parquet(train_path, index=False)
    test_data.to_parquet(test_path, index=False)
    
    return train_data, test_data

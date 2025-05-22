"""
Módulo para dividir datasets en conjuntos de entrenamiento y prueba, y para separar características y variable objetivo.

Contiene funciones para realizar la división estratificada del dataset y guardar los resultados en formato Parquet, así como para separar las características y el target para modelado.
"""

from pathlib import Path

from pandas import DataFrame
from prefect import task
from sklearn.model_selection import train_test_split


@task(name='Separar el dataset y guardarlos', retries=3)
def split_dataset(
    data: DataFrame, target: str, seed: int = 42
) -> tuple[DataFrame, DataFrame]:
    """
    Divide un dataset en conjuntos de entrenamiento y prueba, y guarda los archivos en formato Parquet.

    Args:
    ----
        data: DataFrame con los datos a dividir
        target: Nombre de la columna objetivo (usado para estratificación)
        seed: Semilla para reproducibilidad

    Returns:
    -------
        Tupla con (train_data, test_data)
    """
    # 1) Determina root_dir
    root_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
    data_dir = root_dir / 'data' / 'processed'

    # 2) Crea 'data/' si no existe
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f'📁 Directorio de datos creado en: {data_dir}')

    # 3) Dividir el conjunto original en entrenamiento y prueba
    train_data, test_data = train_test_split(
        data, test_size=0.3, random_state=seed, stratify=data[target]
    )

    # Definir grupos de variables
    discrete_vars = ['disc1', 'disc2']
    categorical_vars = ['cat1', 'cat2']

    # Convertir tipos correctamente
    for dataset in [train_data, test_data]:
        dataset[discrete_vars] = dataset[discrete_vars].astype('object')
        dataset[categorical_vars] = dataset[categorical_vars].astype('object')

    # 4) Rutas de salida Parquet
    train_path = data_dir / 'train.parquet'
    test_path = data_dir / 'test.parquet'

    # 5) Guarda los archivos
    train_data.to_parquet(train_path, index=False)
    test_data.to_parquet(test_path, index=False)

    return train_data, test_data


@task(name='Separar características y target', retries=3)
def split_features_and_target(
    train_set: DataFrame, test_set: DataFrame
) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Separa las características (features) y la variable objetivo (target) de los conjuntos de datos de entrenamiento y prueba.

    Parámetros:
    -----------
    train_set : DataFrame
        Conjunto de datos de entrenamiento que incluye las columnas 'id' y 'target'.
    test_set : DataFrame
        Conjunto de datos de prueba que incluye las columnas 'id' y 'target'.

    Retorna:
    --------
    X_train : DataFrame
        DataFrame con las características de entrenamiento (excluye 'id' y 'target').
    y_train : Series
        Serie con la variable objetivo de entrenamiento.
    X_test : DataFrame
        DataFrame con las características de prueba (excluye 'id' y 'target').
    y_test : Series
        Serie con la variable objetivo de prueba.
    """
    # Selección de características y target en entrenamiento
    X_train = train_set.loc[
        :, [var for var in train_set.columns if var not in ['id', 'target']]
    ]
    y_train = train_set['target']

    # Selección de características y target en prueba
    X_test = test_set.loc[
        :, [var for var in test_set.columns if var not in ['id', 'target']]
    ]
    y_test = test_set['target']

    return X_train, y_train, X_test, y_test

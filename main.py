from src.load_data import load_data
from src.split_dataset import split_dataset

import warnings
warnings.simplefilter('ignore')


# --------------------------------------------------------------------------------
#                               FLUJO DEL PROYECTO
# --------------------------------------------------------------------------------
def main() -> None:
    """
    Función principal que ejecuta la carga y preprocesamiento de datos.
    """
    # 1) Cargar los datos
    data = load_data()

    # 2) Separar el dataset en train y test
    train_set, test_set = split_dataset(
        data=data, 
        target='target'
    )

if __name__ == '__main__':
    main()
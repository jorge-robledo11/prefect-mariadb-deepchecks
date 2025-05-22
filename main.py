"""Módulo principal que define el flujo de ML usando Prefect."""

import warnings

from prefect import flow

from src.load_data import load_data
from src.model import evaluate_model, save_model, train_model
from src.pipelines import feature_engineering
from src.split_dataset import split_dataset, split_features_and_target

warnings.simplefilter('ignore')


# --------------------------------------------------------------------------------
#                               FLUJO DEL PROYECTO
# --------------------------------------------------------------------------------
@flow(name='Flujo de ML', log_prints=True)
def main(target: str) -> None:
    """Función principal que ejecuta la carga y preprocesamiento de datos."""
    # 1) Cargar los datos
    data = load_data()

    # 2) Separar el dataset en train y test
    train_set, test_set = split_dataset(data=data, target=target)

    X_train, y_train, X_test, y_test = split_features_and_target(
        train_set=train_set, test_set=test_set
    )

    X_train, X_test = feature_engineering(
        X_train=X_train, y_train=y_train, X_test=X_test
    )

    model = train_model(X_train=X_train, y_train=y_train)

    save_model(model=model)

    resultados = evaluate_model(
        model=model, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
    )

    print(f'ROC-AUC (Train): {resultados["roc_auc_train"]:.2f}')
    print(f'ROC-AUC (Test):  {resultados["roc_auc_test"]:.2f}')


if __name__ == '__main__':
    main(target='target')
    # deployment_name = 'ml-pipeline-interval-deployment'
    # main.serve(
    #     name=deployment_name,
    #     interval=300 # Intervalo en segundos
    # )

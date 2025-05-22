"""
Genera un dataset sintético para pruebas de modelado predictivo.

Este script crea datos simulados con variables categóricas, continuas, discretas
y una variable target binaria, guardándolos en un archivo CSV en la carpeta `data/raw`.
"""

import uuid
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit

# 1) Parámetros
N = 250_000
np.random.seed(42)
cats1 = ['A', 'B', 'C', 'D', 'E']
cats2 = ['X', 'Y', 'Z']

# 2) Generación del DataFrame
df = pd.DataFrame(
    {
        # Genera un UUID4 distinto para cada fila, lo convertimos a string
        'id': [str(uuid.uuid4().hex)[:12] for _ in range(N)],
        'cat1': np.random.choice(cats1, size=N),
        'cat2': np.random.choice(cats2, size=N),
        'cont1': np.random.normal(loc=0.0, scale=1.0, size=N),
        'cont2': np.random.uniform(low=0.0, high=1.0, size=N),
        'cont3': np.random.exponential(scale=1.0, size=N),
        'cont4': np.random.gamma(shape=2.0, scale=2.0, size=N),
        'disc1': np.random.randint(0, 4, size=N),
        'disc2': np.random.randint(1, 6, size=N),
    }
)

# 3) Cast a categorías
for c in ['cat1', 'cat2', 'disc1', 'disc2']:
    df[c] = df[c].astype('category')

# 4) Clipping de continuas y redondeo a 4 decimales
for col in ['cont1', 'cont2', 'cont3', 'cont4']:
    lo, hi = df[col].quantile([0.001, 0.999])
    df[col] = df[col].clip(lo, hi).round(4)

# 5) Construcción del target
noise = np.random.normal(scale=0.5, size=N)
logit = (
    -0.2
    + 0.4 * df['cont1']
    - 0.3 * df['cont2']
    + 0.5 * df['cont3']
    - 0.2 * df['cont4']
    + noise
)
logit = np.clip(logit, -10, 10)
prob = expit(logit)
df['target'] = (prob > 0.5).astype('int8')

# 6) Guardar en CSV con validación y creación de la carpeta 'raw'
base_data_dir = Path().cwd() / 'data'

# Definir la ruta completa a la carpeta 'raw' dentro del directorio base
raw_data_dir = base_data_dir / 'raw'

# Validar si la carpeta 'raw' existe; si no, crearla
if not raw_data_dir.exists():
    print(f'La carpeta {raw_data_dir.resolve()} no existe. Creándola...')
    raw_data_dir.mkdir(parents=True, exist_ok=True)
else:
    print(f'La carpeta {raw_data_dir.resolve()} ya existe.')

# Definir la ruta completa del archivo CSV dentro de la carpeta 'raw'
file_name = 'dataset_raw.csv'
file_path = raw_data_dir / file_name

# Guardar el DataFrame en el archivo CSV
df.to_csv(file_path, index=False)

print(f'DataFrame guardado exitosamente en: {file_path.resolve()}')

import numpy as np
import pandas as pd
from pathlib import Path
from scipy.special import expit
import uuid

# 1) Parámetros
N = 250_000
np.random.seed(42)
cats1 = ['A', 'B', 'C', 'D', 'E']
cats2 = ['X', 'Y', 'Z']

# 2) Generación del DataFrame
df = pd.DataFrame({
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
})

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

# 6) Guardar en Parquet
data_dir = Path('../terraform/data')
data_dir.mkdir(parents=True, exist_ok=True)
parquet_path = data_dir / 'dataset.parquet'
df.to_parquet(parquet_path, index=False)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Pitch, Sbopen

print("Calculando Modelo de Peligro Esperado (xT)...")

# 1. Matriz estándar de xT (Rejilla 8x12 basada en la probabilidad de gol por zona)
xt_grid = np.array([
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.012,
        0.014,
        0.019,
        0.024,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.009,
        0.011,
        0.014,
        0.018,
        0.025,
        0.038,
    ],
    [
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.012,
        0.015,
        0.021,
        0.030,
        0.052,
        0.084,
    ],
    [
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.013,
        0.016,
        0.022,
        0.034,
        0.056,
        0.108,
        0.257,
    ],
    [
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.013,
        0.016,
        0.022,
        0.034,
        0.056,
        0.108,
        0.257,
    ],
    [
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.010,
        0.012,
        0.015,
        0.021,
        0.030,
        0.052,
        0.084,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.008,
        0.009,
        0.011,
        0.014,
        0.018,
        0.025,
        0.038,
    ],
    [
        0.003,
        0.003,
        0.004,
        0.005,
        0.006,
        0.007,
        0.008,
        0.009,
        0.012,
        0.014,
        0.019,
        0.024,
    ],
])


# Función para transformar coordenadas StatsBomb (120x80) a celdas de la rejilla xT (12x8)
def get_grid_cell(x, y):
  x_bin = min(int(x / 10), 11)
  y_bin = min(int((80 - y) / 10), 7)
  return y_bin, x_bin


# 2. Cargar eventos de un partido (Final Mundial 2022)
parser = Sbopen()
events, _, _, _ = parser.event(3869685)

# 3. Filtrar pases completados
passes = events[
    (events['type_name'] == 'Pass') & (events['outcome_name'].isnull())
].copy()

# 4. Calcular xT acumulado usando 'end_x' y 'end_y'
xt_values = []
for _, row in passes.iterrows():
  y_start, x_start = get_grid_cell(row['x'], row['y'])
  y_end, x_end = get_grid_cell(row['end_x'], row['end_y'])

  val_start = xt_grid[y_start, x_start]
  val_end = xt_grid[y_end, x_end]

  xt_gain = val_end - val_start
  xt_values.append(xt_gain)

passes['xT'] = xt_values

# 5. Ranking de jugadores con mayor impacto xT
top_xt = (
    passes.groupby('player_name')['xT']
    .sum()
    .reset_index()
    .sort_values(by='xT', ascending=False)
)
print('\n--- TOP 5 JUGADORES CON MÁS xT GENERADO EN EL PARTIDO ---')
print(top_xt.head(5))

# 6. Representación visual: Rejilla xT + Pases de Messi
pitch = Pitch(
    pitch_type='statsbomb', pitch_color='#101010', line_color='#444444'
)
fig, ax = pitch.draw(figsize=(12, 8))

# Dibujar la matriz espacial de fondo
ax.imshow(
    xt_grid,
    extent=[0, 120, 0, 80],
    origin='upper',
    cmap='OrRd',
    alpha=0.5,
    aspect='auto',
)

# Filtrar pases de mayor peligro de Messi
messi_top = passes[
    (passes['player_name'] == 'Lionel Andrés Messi Cuccittini')
    & (passes['xT'] > 0.015)
]

pitch.arrows(
    messi_top.x,
    messi_top.y,
    messi_top.end_x,
    messi_top.end_y,
    color='#00e5ff',
    ax=ax,
    width=2,
    headwidth=4,
)

plt.title(
    'Modelo de Peligro Esperado (xT - Expected Threat)\nMatriz de Valoración'
    ' Espacial y Pases Clave de Messi',
    fontsize=13,
    pad=15,
)
plt.savefig('modelo_xt.png', dpi=300, bbox_inches='tight')
print("\n¡ÉXITO! Gráfico guardado como 'modelo_xt.png'.")
plt.show()
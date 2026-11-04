import matplotlib.pyplot as plt
from mplsoccer import Radar

# 1. Definir los parámetros (métricas) a evaluar
params = [
    "Goles s/p",
    "xG s/p",
    "Tiros /90",
    "Pases Clave /90",
    "Regates Éxito /90",
    "Acciones en Área",
    "Pases Progresivos",
]

# 2. Rangos mínimo y máximo para escalar la gráfica
low = [0.0, 0.0, 1.0, 0.5, 0.5, 1.0, 2.0]
high = [1.0, 1.0, 4.5, 3.5, 4.5, 8.0, 9.0]

# 3. Valores reales del jugador
valores_jugador = [0.65, 0.58, 3.80, 2.90, 3.60, 6.50, 7.20]

# 4. Crear el objeto Radar
radar = Radar(
    params,
    low,
    high,
    round_int=[False] * len(params),
    num_rings=4,
    ring_width=1,
    center_circle_radius=1,
)

# 5. Configurar lienzo y ejes
fig, ax = radar.setup_axis()

# 6. Dibujar anillos de fondo
rings_inner = radar.draw_circles(
    ax=ax, facecolor='#111111', edgecolor='#333333'
)

# 7. Dibujar el radar (usando *rings para desempaquetar correctamente todos los retornos)
radar_poly, *rings = radar.draw_radar(
    values=valores_jugador,
    ax=ax,
    kwargs_radar={'facecolor': '#00e5ff', 'alpha': 0.6, 'linewidth': 2},
    kwargs_rings={'facecolor': '#00e5ff', 'alpha': 0.2},
)

# 8. Etiquetas de rangos y métricas
range_labels = radar.draw_range_labels(
    ax=ax, fontsize=9, color='#888888', zorder=2
)
param_labels = radar.draw_param_labels(
    ax=ax, fontsize=10, color='black', fontweight='bold'
)

plt.title(
    "Perfil de Scouting Multidimensional (Radar Chart)", fontsize=14, pad=25
)
plt.show()
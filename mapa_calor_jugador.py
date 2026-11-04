import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

print("Cargando eventos de la Final del Mundial 2022...")

# 1. Cargar eventos del partido
parser = Sbopen()
events, related, freeze, players = parser.event(3869685)

# 2. Filtrar todas las acciones con balón de Messi que tengan coordenadas X e Y
messi_events = events[
    (events['player_name'] == 'Lionel Andrés Messi Cuccittini')
    & (events['x'].notnull())
]

# 3. Crear el lienzo con un campo oscuro estilo profesional
pitch = Pitch(
    pitch_type='statsbomb', pitch_color='#101010', line_color='#444444'
)
fig, ax = pitch.draw(figsize=(12, 8))

# 4. Generar la densidad del mapa de calor (KDE)
kde = pitch.kdeplot(
    messi_events.x,
    messi_events.y,
    ax=ax,
    cmap='hot',  # Mapeo de color estilo 'fuego' (negro/rojo/amarillo/blanco)
    fill=True,
    thresh=0.05,
    n_levels=100,
    alpha=0.8,
)

# 5. Añadir título y ajustar estilo
plt.title(
    "Mapa de Calor: Zonas de Influencia de Leo Messi\nFinal Mundial 2022"
    " (Argentina vs Francia)",
    fontsize=14,
    pad=12,
    color='black',
)

plt.show()
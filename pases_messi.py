import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

# 1. Conectar con los datos abiertos de StatsBomb
parser = Sbopen()

# 2. Descargar los eventos de la Final del Mundial 2022 (ID de partido: 3869685)
events, related, freeze, players = parser.event(3869685)

# 3. Filtrar los pases realizados por Messi
messi_passes = events[(events['player_name'] == 'Lionel Andrés Messi Cuccittini') & (events['type_name'] == 'Pass')]
# Pases completados (outcome_name es nulo)
pases_completados = messi_passes[messi_passes['outcome_name'].isnull()]

# Pases incompletos
pases_fallados = messi_passes[messi_passes['outcome_name'].notnull()]
# 4. Diseñar el campo
pitch = Pitch(pitch_type='statsbomb', pitch_color='#1b4332', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

# 5. Dibujar cada pase como una flecha (desde x, y hasta end_x, end_y)

pitch.arrows(pases_completados.x, pases_completados.y, pases_completados.end_x, pases_completados.end_y,
             color='#2ec4b6', ax=ax, width=2, headwidth=3, label='Completados')

pitch.arrows(pases_fallados.x, pases_fallados.y, pases_fallados.end_x, pases_fallados.end_y,
             color='#e71d36', ax=ax, width=2, headwidth=3, label='Fallados')
plt.title("Pases de Leo Messi - Final Mundial 2022 (Argentina vs Francia)", fontsize=14, pad=12)
plt.show()

import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

# 1. Conectar con StatsBomb y cargar los eventos de la final
parser = Sbopen()
events, related, freeze, players = parser.event(3869685)

# 2. Filtrar solo los disparos
shots = events[events['type_name'] == 'Shot'].copy()

# Separar goles de tiros fallados/detenidos
goals = shots[shots['outcome_name'] == 'Goal']
non_goals = shots[shots['outcome_name'] != 'Goal']

# 3. Diseñar el medio campo ofensivo / campo entero
pitch = Pitch(pitch_type='statsbomb', pitch_color='#1b4332', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

# 4. Dibujar tiros no convertidos (círculos rojos)
# El tamaño 's' se multiplica por el xG para que a mayor xG, mayor sea el punto
pitch.scatter(non_goals.x, non_goals.y,
              s=(non_goals.shot_statsbomb_xg * 700) + 40,
              c='#e71d36', alpha=0.6, edgecolors='white',
              linewidth=1, ax=ax, label='Tiro (Sin gol)')

# 5. Dibujar goles (estrellas/puntos verdes brillantes)
pitch.scatter(goals.x, goals.y,
              s=(goals.shot_statsbomb_xg * 700) + 100,
              c='#2ec4b6', alpha=0.9, edgecolors='black',
              marker='*', linewidth=1, ax=ax, label='Gol')

# 6. Añadir leyenda y título
ax.legend(loc='upper left', fontsize=11, facecolor='#1b4332', labelcolor='white')
plt.title("Mapa de Tiros y xG (Expected Goals) - Final Mundial 2022", fontsize=14, pad=12)

plt.show()